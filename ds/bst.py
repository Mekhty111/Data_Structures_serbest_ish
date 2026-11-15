# Mövzu 5: binary search tree. Sıralanmış verilənlərin ağaca təsiri.
import math
import random
import sys
from time import perf_counter

from .common import micro, print_table, print_title

# Sıralı girişdə ağac 2000 səviyyə dərinliyində ola bilər, rekursiya üçün limit artırılır.
sys.setrecursionlimit(10000)


class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = TreeNode(key)
            return
        current = self.root
        while True:
            if key == current.key:
                return                          # dublikat əlavə olunmur
            if key < current.key:
                if current.left is None:
                    current.left = TreeNode(key)
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = TreeNode(key)
                    return
                current = current.right

    def search(self, key):
        """Tapıldı ya yox və keçilən yol."""
        path = []
        current = self.root
        while current is not None:
            path.append(current.key)
            if key == current.key:
                return True, path
            if key < current.key:
                current = current.left
            else:
                current = current.right
        return False, path

    def delete(self, key):
        # 1) silinəcək node-u və onun valideynini tapırıq
        parent = None
        current = self.root
        while current is not None and current.key != key:
            parent = current
            if key < current.key:
                current = current.left
            else:
                current = current.right
        if current is None:
            return False

        # 2) iki uşaq varsa: sağ alt ağacın ən kiçiyini (successor) tapıb
        #    onun açarını bura yazırıq, sonra successor-u silirik
        if current.left is not None and current.right is not None:
            successor_parent = current
            successor = current.right
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left
            current.key = successor.key
            parent = successor_parent
            current = successor

        # 3) indi node-un ən çox bir uşağı var, onu valideynə bağlayırıq
        if current.left is not None:
            child = current.left
        else:
            child = current.right

        if parent is None:
            self.root = child
        elif parent.left == current:
            parent.left = child
        else:
            parent.right = child
        return True

    def inorder(self, node, result):            # sol, kök, sağ: sıralı çıxır
        if node is not None:
            self.inorder(node.left, result)
            result.append(node.key)
            self.inorder(node.right, result)
        return result

    def preorder(self, node, result):           # kök, sol, sağ
        if node is not None:
            result.append(node.key)
            self.preorder(node.left, result)
            self.preorder(node.right, result)
        return result

    def postorder(self, node, result):          # sol, sağ, kök
        if node is not None:
            self.postorder(node.left, result)
            self.postorder(node.right, result)
            result.append(node.key)
        return result

    def height(self, node):
        if node is None:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))

    def draw(self, node, prefix, is_left, lines):
        """Ağacı yan tərəfə çevrilmiş şəkildə çəkir: sağ alt ağac yuxarıda."""
        if node is None:
            return
        if is_left:
            self.draw(node.right, prefix + "|   ", False, lines)
            lines.append(prefix + "\\-- " + str(node.key))
            self.draw(node.left, prefix + "    ", True, lines)
        else:
            self.draw(node.right, prefix + "    ", False, lines)
            lines.append(prefix + "/-- " + str(node.key))
            self.draw(node.left, prefix + "|   ", True, lines)

    def show(self):
        if self.root is None:
            print("    (boş ağac)")
            return
        lines = []
        self.draw(self.root.right, "", False, lines)
        lines.append(str(self.root.key))
        self.draw(self.root.left, "", True, lines)
        for line in lines:
            print("    " + line)


def build(keys):
    tree = BST()
    for key in keys:
        tree.insert(key)
    return tree


def shape_benchmark():
    """Eyni açarlar sıralı və təsadüfi ardıcıllıqla: hündürlük və vaxt."""
    rows = []
    for n in [100, 500, 1000, 2000]:
        sorted_keys = list(range(n))
        random_keys = list(range(n))
        random.Random(n).shuffle(random_keys)

        start = perf_counter()
        sorted_tree = build(sorted_keys)
        build_sorted = round(micro(start, 1) / 1000, 2)       # ms

        start = perf_counter()
        random_tree = build(random_keys)
        build_random = round(micro(start, 1) / 1000, 2)

        start = perf_counter()
        for i in range(50):
            sorted_tree.search(n - 1)
        search_sorted = micro(start, 50)

        start = perf_counter()
        for i in range(50):
            random_tree.search(n - 1)
        search_random = micro(start, 50)

        rows.append([n, math.ceil(math.log2(n + 1)),
                     sorted_tree.height(sorted_tree.root), random_tree.height(random_tree.root),
                     build_sorted, build_random, search_sorted, search_random])
    return rows


def demo():
    print_title("5. Binary Search Tree")

    keys = [50, 30, 70, 20, 40, 60, 80, 35, 45, 65]
    t = build(keys)
    print("\nƏlavə sırası:", keys)
    t.show()
    print("  search(65):", t.search(65))
    print("  search(99):", t.search(99))
    print("  inorder:  ", t.inorder(t.root, []), " (həmişə sıralı çıxır)")
    print("  preorder: ", t.preorder(t.root, []))
    print("  postorder:", t.postorder(t.root, []))

    print("\ndelete(20): yarpaq, sadəcə kəsilir")
    print("delete(70): iki uşaq var, yerinə sağ alt ağacın ən kiçiyi yazılır")
    t.delete(20)
    t.delete(70)
    t.show()

    print("\n1..7 sıralı əlavə olunanda")
    chain = build([1, 2, 3, 4, 5, 6, 7])
    chain.show()
    print("  hündürlük =", chain.height(chain.root))

    print("\nEyni ədədlər 4, 2, 6, 1, 3, 5, 7 sırası ilə")
    balanced = build([4, 2, 6, 1, 3, 5, 7])
    balanced.show()
    print("  hündürlük =", balanced.height(balanced.root))

    print("\nSıralı və təsadüfi əlavə: hündürlük və vaxt")
    print_table(["n", "ideal hündürlük", "sıralı: h", "təsadüfi: h", "sıralı: qurma ms",
                 "təsadüfi: qurma ms", "sıralı: axtarış µs", "təsadüfi: axtarış µs"], shape_benchmark())

    print("\nİzah")
    print("  Hər yeni açar əvvəlkilərdən böyükdürsə, həmişə sağa gedir. Ağac xəttə çevrilir (linked list kimi).")
    print("  Hündürlük log2(n) əvəzinə n olur, ona görə axtarış və əlavə O(log n)-dən O(n)-ə düşür.")
    print("  Sıralı n açarı əlavə etmək cəmi O(n^2) çəkir, təsadüfi sırada orta hesabla O(n log n).")
    print("  Həll: açarları qarışdırmaq və ya özü balanslaşan ağac (AVL, Red-Black) istifadə etmək.")
