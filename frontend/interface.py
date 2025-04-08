import tkinter as tk
import math
from backend.logic_clock import Clock

class ClockFrontend:
    def __init__(self, root):
        self.root = root
        self.clock = Clock()
        self.canvas_size = 400
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="#101820")
        self.canvas.pack()
        self.center = self.canvas_size // 2
        self.radio = 150
        self.dragging_hand = None

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.refresh()

    def draw_clock(self, hour, minute, second):
        self.canvas.delete("all")

        self.canvas.create_oval(
            self.center - self.radio, self.center - self.radio,
            self.center + self.radio, self.center + self.radio,
            fill="#FEE715", outline="#FEE715"
        )

        for i in range(60):
            angle = math.radians(i * 6)
            inner = self.radio - 5 if i % 5 != 0 else self.radio - 15
            x_start = self.center + math.cos(angle) * inner
            y_start = self.center + math.sin(angle) * inner
            x_end = self.center + math.cos(angle) * self.radio
            y_end = self.center + math.sin(angle) * self.radio
            color = "#000000" if i % 5 == 0 else "#555555"
            self.canvas.create_line(x_start, y_start, x_end, y_end, fill=color, width=1)

        for i in range(12):
            angle = math.radians(i * 30 - 60)
            x = self.center + math.cos(angle) * (self.radio - 30)
            y = self.center + math.sin(angle) * (self.radio - 30)
            self.canvas.create_text(x, y, text=str(i + 1), font=("Arial", 12, "bold"), fill="#000000")

        self.hand_coords = {}
        self.draw_hand((hour % 12) * 30, self.radio * 0.5, width=6, color="#000000", label="hour")
        self.draw_hand(minute * 6, self.radio * 0.7, width=4, color="#000000", label="minute")
        self.draw_hand(second * 6, self.radio * 0.9, width=2, color="red", label="second")

        self.canvas.create_oval(self.center - 5, self.center - 5, self.center + 5, self.center + 5, fill="#000000")

    def draw_hand(self, angle_deg, length, width=2, color="black", label=None):
        angle_rad = math.radians(angle_deg - 90)
        x = self.center + length * math.cos(angle_rad)
        y = self.center + length * math.sin(angle_rad)
        self.canvas.create_line(self.center, self.center, x, y, width=width, fill=color)

        if label:
            self.hand_coords[label] = (x, y)

    def refresh(self):
        if not self.dragging_hand:  # no actualiza automaticamente si se esta manipulando
            self.clock.tic()
        hour, minute, second = self.clock.get_time()
        self.draw_clock(hour, minute, second)
        self.root.after(1000, self.refresh)

    def on_click(self, event):
        x, y = event.x, event.y
        for hand, (hx, hy) in self.hand_coords.items():
            if (x - hx) ** 2 + (y - hy) ** 2 <= 100:  # rango de seleccion
                self.dragging_hand = hand
                break

    def on_drag(self, event):
        if self.dragging_hand:
            angle = math.degrees(math.atan2(event.y - self.center, event.x - self.center)) + 90
            angle %= 360

            if self.dragging_hand == "second":
                new_val = int(angle / 6)
                self.clock.ptr_seg = self._move_to_value(self.clock.seconds, new_val)
            elif self.dragging_hand == "minute":
                new_val = int(angle / 6)
                self.clock.ptr_min = self._move_to_value(self.clock.minutes, new_val)
            elif self.dragging_hand == "hour":
                new_val = int(angle / 30)
                self.clock.ptr_hor = self._move_to_value(self.clock.hours, new_val + 1)

            self.draw_clock(*self.clock.get_time())

    def on_release(self, event):
        self.dragging_hand = None

    def _move_to_value(self, circular_list, value):
        ptr = circular_list.head
        while ptr.data != value:
            ptr = ptr.next
        return ptr
