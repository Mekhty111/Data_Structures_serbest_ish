# Mövzu 2: singly və doubly linked list, onların müqayisəsi.
import sys
from time import perf_counter

from .common import micro, print_table, print_title


class Node:
    __slots__ = ("value", "next")             # yaddaş: yalnız bu iki sahə saxlanır

    def __init__(self, value):
        self.value = value
        self.next = None


class DNode:
    __slots__ = ("value", "prev", "next")

    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def push_front(self, value):              # O(1)
        node = Node(value)
        node.next = self.head
        self.head = node
        if self.tail is None:
            self.tail = node
        self.size += 1

    def append(self, value):                  # O(1), çünki tail saxlayırıq
        node = Node(value)
        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self.size += 1

    def pop_front(self):                      # O(1)
        if self.head is None:
            raise IndexError("siyahı boşdur")
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return value

    def pop_back(self):                       # O(n)
        if self.head is None:
            raise IndexError("siyahı boşdur")
        if self.head == self.tail:
            return self.pop_front()
        # tail-dən əvvəlki node-u tapmaq üçün başdan getməliyik
        current = self.head
        while current.next != self.tail:
            current = current.next
        value = self.tail.value
        current.next = None
        self.tail = current
        self.size -= 1
        return value

    def find(self, value):                    # O(n)
        """Tapılan indeks (və ya -1) və keçilən node sayı."""
        current = self.head
        index = 0
        while current is not None:
            if current.value == value:
                return index, index + 1
            current = current.next
            index += 1
        return -1, index

    def delete(self, value):                  # O(n)
        previous = None
        current = self.head
        while current is not None and current.value != value:
            previous = current
            current = current.next
        if current is None:
            return False
        if previous is None:
            self.head = current.next
        else:
            previous.next = current.next
        if current == self.tail:
            self.tail = previous
        self.size -= 1
        return True

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    def show(self):
        text = "head"
        for value in self.to_list():
            text += " -> " + str(value)
        return text + " -> None"


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def push_front(self, value):              # O(1)
        node = DNode(value)
        node.next = self.head
        if self.head is None:
            self.tail = node
        else:
            self.head.prev = node
        self.head = node
        self.size += 1

    def append(self, value):                  # O(1)
        node = DNode(value)
        node.prev = self.tail
        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self.size += 1

    def unlink(self, node):                   # O(1), çünki prev məlumdur
        if node.prev is None:
            self.head = node.next
        else:
            node.prev.next = node.next
        if node.next is None:
            self.tail = node.prev
        else:
            node.next.prev = node.prev
        self.size -= 1
        return node.value

    def pop_front(self):                      # O(1)
        if self.head is None:
            raise IndexError("siyahı boşdur")
        return self.unlink(self.head)

    def pop_back(self):                       # O(1)
        if self.tail is None:
            raise IndexError("siyahı boşdur")
        return self.unlink(self.tail)

    def find(self, value):                    # O(n)
        current = self.head
        index = 0
        while current is not None:
            if current.value == value:
                return index, index + 1
            current = current.next
            index += 1
        return -1, index

    def delete(self, value):                  # O(n)
        current = self.head
        while current is not None:
            if current.value == value:
                self.unlink(current)
                return True
            current = current.next
        return False

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    def to_list_backward(self):
        result = []
        current = self.tail
        while current is not None:
            result.append(current.value)
            current = current.prev
        return result

    def show(self):
        text = "None"
        for value in self.to_list():
            text += " <-> " + str(value)
        return text + " <-> None"


def measure(lst):
    """5 əməliyyatın vaxtı (µs). Singly və doubly-də metodların adları eynidir."""
    start = perf_counter()
    for i in range(1000):
        lst.push_front(0)
    add_front = micro(start, 1000)

    start = perf_counter()
    for i in range(1000):
        lst.append(0)
    add_end = micro(start, 1000)

    start = perf_counter()
    for i in range(1000):
        lst.pop_front()
    delete_front = micro(start, 1000)

    start = perf_counter()
    for i in range(20):
        lst.pop_back()
    delete_end = micro(start, 20)

    start = perf_counter()
    for i in range(20):
        lst.find(-1)
    search = micro(start, 20)

    return [add_front, add_end, delete_front, delete_end, search]


HEADER = ["n", "struktur", "başa əlavə", "sona əlavə", "başdan silmə", "sondan silmə", "axtarış"]


def benchmark():
    rows = []
    for n in [1_000, 10_000, 50_000]:
        singly = SinglyLinkedList()
        doubly = DoublyLinkedList()
        for i in range(n):
            singly.append(i)
            doubly.append(i)
        rows.append([n, "Singly"] + measure(singly))
        rows.append([n, "Doubly"] + measure(doubly))
    return rows


def demo():
    print_title("2. Singly və Doubly Linked List")

    print("\nSingly linked list")
    s = SinglyLinkedList()
    for x in [10, 20, 30]:
        s.append(x)
    print("  başlanğıc:     ", s.show())
    s.push_front(5)
    print("  push_front(5): ", s.show())
    s.append(40)
    print("  append(40):    ", s.show())
    print("  find(30):       indeks və addım", s.find(30))
    s.delete(20)
    print("  delete(20):    ", s.show())
    s.pop_back()
    print("  pop_back():    ", s.show(), " (başdan sona qədər getdi)")

    print("\nDoubly linked list")
    d = DoublyLinkedList()
    for x in [10, 20, 30]:
        d.append(x)
    print("  başlanğıc:     ", d.show())
    d.push_front(5)
    print("  push_front(5): ", d.show())
    d.append(40)
    print("  append(40):    ", d.show())
    d.delete(20)
    print("  delete(20):    ", d.show())
    d.pop_back()
    print("  pop_back():    ", d.show(), " (tail.prev ilə birbaşa)")
    print("  geriyə keçid:  ", d.to_list_backward())

    print("\nBir node-un yaddaşı")
    print("  Singly node (value, next):      ", sys.getsizeof(Node(0)), "bayt")
    print("  Doubly node (value, prev, next):", sys.getsizeof(DNode(0)), "bayt")

    print("\nVaxt ölçümü, µs / bir əməliyyat")
    print_table(HEADER, benchmark())

    print("\nNəticə")
    print("  Başa/sona əlavə və başdan silmə: hər ikisində O(1).")
    print("  Sondan silmə: singly-də O(n), doubly-də O(1). Fərq n böyüdükcə artır.")
    print("  Axtarış: hər ikisində O(n), çünki indeks yoxdur.")
    print("  Doubly hər node-da bir göstərici artıq saxlayır, yəni daha çox yaddaş tutur.")
