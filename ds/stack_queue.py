# Mövzu 3: stack, queue və deque sadə brauzerin funksiyalarında.
#   stack - "geri" və "irəli" düymələri (son açılan səhifə birinci qayıdır, LIFO)
#   queue - yükləmələr növbəsi (birinci əlavə olunan birinci yüklənir, FIFO)
#   deque - son baxılan 5 səhifə (hər iki ucdan O(1), maxlen köhnəni özü atır)
from collections import deque
from time import perf_counter

from .common import micro, print_table, print_title
from .linked_lists import Node


class Stack:
    """Python list üzərində stack: append və pop sondan işləyir, O(1)."""

    def __init__(self):
        self.items = []

    def push(self, value):
        self.items.append(value)

    def pop(self):
        if len(self.items) == 0:
            raise IndexError("stack boşdur")
        return self.items.pop()

    def is_empty(self):
        return len(self.items) == 0


class LinkedQueue:
    """Linked list üzərində queue: sona əlavə, başdan götürmə, ikisi də O(1)."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, value):
        node = Node(value)
        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self.size += 1

    def dequeue(self):
        if self.head is None:
            raise IndexError("növbə boşdur")
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return value

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result


class Browser:
    def __init__(self):
        self.current = "home.az"
        self.back_stack = Stack()
        self.forward_stack = Stack()
        self.downloads = LinkedQueue()
        self.recent = deque(["home.az"], maxlen=5)

    def remember(self, url):
        # eyni səhifə təkrar olmasın, ən yenisi solda dursun
        if url in self.recent:
            self.recent.remove(url)
        self.recent.appendleft(url)

    def open(self, url):
        self.back_stack.push(self.current)
        self.forward_stack = Stack()        # yeni səhifə açılanda "irəli" tarixçəsi silinir
        self.current = url
        self.remember(url)

    def back(self):
        if self.back_stack.is_empty():
            raise IndexError("geri qayıtmaq üçün səhifə yoxdur")
        self.forward_stack.push(self.current)
        self.current = self.back_stack.pop()
        self.remember(self.current)

    def forward(self):
        if self.forward_stack.is_empty():
            raise IndexError("irəli getmək üçün səhifə yoxdur")
        self.back_stack.push(self.current)
        self.current = self.forward_stack.pop()
        self.remember(self.current)

    def add_download(self, file_name):
        self.downloads.enqueue(file_name)

    def next_download(self):
        return self.downloads.dequeue()

    def show(self):
        print("  cari səhifə:     ", self.current)
        print("  geri stack:      ", self.back_stack.items)
        print("  irəli stack:     ", self.forward_stack.items)
        print("  yükləmə növbəsi: ", self.downloads.to_list())
        print("  son baxılanlar:  ", list(self.recent))


def queue_benchmark():
    """Növbədən bir elementi götürmək: list.pop(0), deque.popleft(), LinkedQueue.dequeue()."""
    rows = []
    for n in [1_000, 10_000, 50_000]:
        python_list = list(range(n))
        dq = deque(range(n))
        lq = LinkedQueue()
        for i in range(n):
            lq.enqueue(i)

        start = perf_counter()
        for i in range(500):
            python_list.pop(0)
        list_time = micro(start, 500)

        start = perf_counter()
        for i in range(500):
            dq.popleft()
        deque_time = micro(start, 500)

        start = perf_counter()
        for i in range(500):
            lq.dequeue()
        linked_time = micro(start, 500)

        rows.append([n, list_time, deque_time, linked_time])
    return rows


def demo():
    print_title("3. Stack, Queue və Deque: sadə brauzer")

    print("\nHansı struktur nə üçün")
    print("  Stack: geri / irəli düymələri. Ən son açılan səhifəyə birinci qayıdırıq (LIFO).")
    print("  Queue: yükləmələr. Faylı kim birinci əlavə edibsə, o birinci yüklənir (FIFO).")
    print("  Deque(maxlen=5): son baxılanlar. Yenisi əvvələ əlavə olunur, köhnəsi sondan özü düşür.")

    b = Browser()
    print("\nopen aztu.edu.az, open koica.go.kr, open github.com")
    b.open("aztu.edu.az")
    b.open("koica.go.kr")
    b.open("github.com")
    b.show()

    print("\nback, back, forward")
    b.back()
    b.back()
    b.forward()
    b.show()

    print("\ndownload lecture1.pdf, lab2.zip, video.mp4 və bir faylı yüklə")
    b.add_download("lecture1.pdf")
    b.add_download("lab2.zip")
    b.add_download("video.mp4")
    print("  yükləndi:", b.next_download())
    b.show()

    print("\nDaha 4 səhifə açırıq: son baxılanlarda yalnız 5 səhifə qalır")
    for url in ["a.az", "b.az", "c.az", "d.az"]:
        b.open(url)
    print("  son baxılanlar:", list(b.recent))

    print("\nNövbədən bir elementi götürmək, µs")
    print_table(["n", "list.pop(0)", "deque.popleft()", "LinkedQueue.dequeue()"], queue_benchmark())

    print("\nNəticə")
    print("  list.pop(0) bütün elementləri sola sürüşdürür (O(n)), ona görə növbə üçün")
    print("  deque və ya linked list əsaslı queue seçilir (O(1)).")
