# Mövzu 1: sabit array və dynamic array.
# Əlavə, silmə və axtarışın vaxtı müxtəlif ölçülərdə ölçülür.
from time import perf_counter

from .common import micro, print_table, print_title


class FixedArray:
    """Sabit tutumlu array: yaddaş bir dəfə ayrılır, sonra böyümür."""

    def __init__(self, capacity):
        self.capacity = capacity
        self.data = [None] * capacity
        self.size = 0

    def check_index(self, index, limit):
        if index < 0 or index > limit:
            raise IndexError("belə indeks yoxdur")

    def make_room(self):
        if self.size == self.capacity:
            raise OverflowError("array doludur")

    def get(self, index):                       # O(1)
        self.check_index(index, self.size - 1)
        return self.data[index]

    def append(self, value):                    # O(1)
        self.make_room()
        self.data[self.size] = value
        self.size += 1

    def insert(self, index, value):             # O(n)
        self.check_index(index, self.size)
        self.make_room()
        # index-dən sağdakı elementləri bir addım sağa sürüşdürürük
        i = self.size
        while i > index:
            self.data[i] = self.data[i - 1]
            i -= 1
        self.data[index] = value
        self.size += 1
        return self.size - 1 - index            # neçə element sürüşdü

    def delete(self, index):                    # O(n)
        self.check_index(index, self.size - 1)
        # index-dən sağdakı elementləri bir addım sola sürüşdürürük
        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]
        self.size -= 1
        self.data[self.size] = None
        return self.size - index

    def find(self, value):                      # O(n), linear search
        for i in range(self.size):
            if self.data[i] == value:
                return i
        return -1

    def show(self):
        cells = []
        for x in self.data:
            if x is None:
                cells.append("_")
            else:
                cells.append(str(x))
        return "[" + ", ".join(cells) + "]"


class DynamicArray(FixedArray):
    """Dolanda tutumu 2 dəfə artırır. Qalan metodlar FixedArray ilə eynidir."""

    def __init__(self):
        super().__init__(1)
        self.resizes = 0

    def make_room(self):
        if self.size == self.capacity:
            new_data = [None] * (self.capacity * 2)
            for i in range(self.size):
                new_data[i] = self.data[i]
            self.data = new_data
            self.capacity = self.capacity * 2
            self.resizes += 1


def measure_my_array(arr, repeat):
    """Öz array-imiz üçün 5 əməliyyatın vaxtı (µs)."""
    start = perf_counter()
    for i in range(1000):
        arr.append(0)
    add_end = micro(start, 1000)

    start = perf_counter()
    for i in range(repeat):
        arr.insert(0, 0)
    add_front = micro(start, repeat)

    start = perf_counter()
    for i in range(1000):
        arr.delete(arr.size - 1)
    delete_end = micro(start, 1000)

    start = perf_counter()
    for i in range(repeat):
        arr.delete(0)
    delete_front = micro(start, repeat)

    start = perf_counter()
    for i in range(repeat):
        arr.find(-1)                            # olmayan element: hamısı yoxlanır
    search = micro(start, repeat)

    return [add_end, add_front, delete_end, delete_front, search]


def measure_python_list(a, repeat):
    """Eyni 5 əməliyyat Python list üçün."""
    start = perf_counter()
    for i in range(1000):
        a.append(0)
    add_end = micro(start, 1000)

    start = perf_counter()
    for i in range(repeat):
        a.insert(0, 0)
    add_front = micro(start, repeat)

    start = perf_counter()
    for i in range(1000):
        a.pop()
    delete_end = micro(start, 1000)

    start = perf_counter()
    for i in range(repeat):
        a.pop(0)
    delete_front = micro(start, repeat)

    start = perf_counter()
    for i in range(repeat):
        found = -1 in a
    search = micro(start, repeat)

    return [add_end, add_front, delete_end, delete_front, search]


HEADER = ["n", "struktur", "sona əlavə", "başa əlavə", "sondan silmə", "başdan silmə", "axtarış"]


def benchmark():
    rows = []
    for n in [1_000, 10_000, 50_000]:
        fixed = FixedArray(n + 2000)
        dynamic = DynamicArray()
        for i in range(n):
            fixed.append(i)
            dynamic.append(i)
        python_list = list(range(n))

        rows.append([n, "FixedArray"] + measure_my_array(fixed, 20))
        rows.append([n, "DynamicArray"] + measure_my_array(dynamic, 20))
        rows.append([n, "Python list"] + measure_python_list(python_list, 200))
    return rows


def demo():
    print_title("1. Array və Dynamic Array")

    print("\nSabit array (tutum 8)")
    arr = FixedArray(8)
    for x in [10, 20, 30, 40]:
        arr.append(x)
    print("  append 10, 20, 30, 40 ->", arr.show())
    moved = arr.insert(1, 15)
    print("  insert(1, 15)         ->", arr.show(), " sürüşdü:", moved)
    moved = arr.delete(0)
    print("  delete(0)             ->", arr.show(), " sürüşdü:", moved)
    print("  find(30) =", arr.find(30), "  find(99) =", arr.find(99))

    print("\nDynamic array: tutum necə artır")
    dyn = DynamicArray()
    for x in range(1, 34):
        old = dyn.capacity
        dyn.append(x)
        if dyn.capacity != old:
            print(f"  append #{x}: tutum {old} -> {dyn.capacity}, {old} element köçürüldü")

    print("\nVaxt ölçümü, µs / bir əməliyyat")
    print_table(HEADER, benchmark())

    print("\nNəticə")
    print("  Sona əlavə və sondan silmə: hər üç strukturda O(1), n-dən asılı deyil.")
    print("  Başa əlavə/silmə və axtarış: O(n), n 10 dəfə artanda vaxt da təxminən 10 dəfə artır.")
    print("  Python list eyni alqoritmdir, sadəcə C-də yazılıb, ona görə daha sürətlidir.")
