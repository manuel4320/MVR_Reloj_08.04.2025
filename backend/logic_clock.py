from backend.circular_list import CircularDoublyLinkedList

class Clock:
    def __init__(self):
        self.seconds = CircularDoublyLinkedList()
        self.minutes = CircularDoublyLinkedList()
        self.hours = CircularDoublyLinkedList()

        for i in range(60):
            self.seconds.insert_at_end(i)
            self.minutes.insert_at_end(i)
        for i in range(12):
            self.hours.insert_at_end(i + 1)

        self.ptr_seg = self.seconds.head
        self.ptr_min = self.minutes.head
        self.ptr_hor = self.hours.head

    def tic(self):
        self.ptr_seg = self.ptr_seg.next
        if self.ptr_seg.data == 0:
            self.ptr_min = self.ptr_min.next
            if self.ptr_min.data == 0:
                self.ptr_hor = self.ptr_hor.next

    def get_time(self):
        return (self.ptr_hor.data, self.ptr_min.data, self.ptr_seg.data)
