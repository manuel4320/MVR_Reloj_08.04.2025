import tkinter as tk
from frontend.interface import ClockFrontend

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Analog Clock!")
    app = ClockFrontend(root)
    root.mainloop()
