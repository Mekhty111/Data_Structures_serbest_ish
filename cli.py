# Data Structures konsol tətbiqi. İşə salmaq: python cli.py
import sys

from ds import arrays, bst, hash_table, linked_lists, stack_queue
from ds.arrays import DynamicArray, FixedArray
from ds.bst import BST
from ds.hash_table import HashTable, poly_hash, simple_hash
from ds.linked_lists import DoublyLinkedList, SinglyLinkedList
from ds.stack_queue import Browser

sys.stdout.reconfigure(encoding="utf-8")


def read_command():
    """İstifadəçinin yazdığı sətri əmrə və arqumentlərə bölür."""
    parts = input("> ").split()
    if len(parts) == 0:
        return "", []
    return parts[0], parts[1:]


# 1. Array və Dynamic Array

def array_menu():
    print("\n=== 1. Array və Dynamic Array ===")
    print("  new fixed 8      yeni sabit array (tutum 8)")
    print("  new dynamic      yeni dynamic array")
    print("  add 1 2 3        sona əlavə et")
    print("  ins 0 9          0-cı yerə 9 əlavə et")
    print("  del 0            0-cı elementi sil")
    print("  find 9           dəyərə görə axtar")
    print("  bench            vaxt ölçümü")
    print("  q                menyuya qayıt")

    arr = FixedArray(8)
    while True:
        print(f"  {arr.show()}  size={arr.size} capacity={arr.capacity}")
        cmd, args = read_command()
        try:
            if cmd == "q":
                return
            elif cmd == "new" and len(args) > 0 and args[0] == "dynamic":
                arr = DynamicArray()
            elif cmd == "new":
                arr = FixedArray(int(args[1]))
            elif cmd == "add":
                for x in args:
                    arr.append(int(x))
            elif cmd == "ins":
                moved = arr.insert(int(args[0]), int(args[1]))
                print(f"  {moved} element sağa sürüşdü")
            elif cmd == "del":
                moved = arr.delete(int(args[0]))
                print(f"  {moved} element sola sürüşdü")
            elif cmd == "find":
                index = arr.find(int(args[0]))
                if index == -1:
                    print("  tapılmadı")
                else:
                    print("  indeks", index)
            elif cmd == "bench":
                arrays.demo()
            else:
                print("  naməlum əmr")
        except (ValueError, IndexError, OverflowError) as error:
            print("  xəta:", error)


# 2. Singly və Doubly Linked List

def linked_list_menu():
    print("\n=== 2. Singly və Doubly Linked List ===")
    print("  type s / type d  singly və ya doubly siyahıya keç")
    print("  front 5          başa əlavə")
    print("  back 5           sona əlavə")
    print("  popf             başdan sil")
    print("  popb             sondan sil (singly-də O(n))")
    print("  del 5            dəyərə görə sil")
    print("  find 5           axtar")
    print("  bench            singly və doubly müqayisəsi")
    print("  q                menyuya qayıt")

    lst = SinglyLinkedList()
    for x in [10, 20, 30]:
        lst.append(x)
    while True:
        if isinstance(lst, SinglyLinkedList):
            print("  [singly]", lst.show())
        else:
            print("  [doubly]", lst.show())
        cmd, args = read_command()
        try:
            if cmd == "q":
                return
            elif cmd == "type":
                values = lst.to_list()
                if args[0] == "d":
                    lst = DoublyLinkedList()
                else:
                    lst = SinglyLinkedList()
                for x in values:
                    lst.append(x)
            elif cmd == "front":
                lst.push_front(int(args[0]))
            elif cmd == "back":
                lst.append(int(args[0]))
            elif cmd == "popf":
                print("  silindi:", lst.pop_front())
            elif cmd == "popb":
                print("  silindi:", lst.pop_back())
            elif cmd == "del":
                if not lst.delete(int(args[0])):
                    print("  tapılmadı")
            elif cmd == "find":
                index, steps = lst.find(int(args[0]))
                if index == -1:
                    print(f"  tapılmadı, {steps} node keçildi")
                else:
                    print(f"  indeks {index}, {steps} node keçildi")
            elif cmd == "bench":
                linked_lists.demo()
            else:
                print("  naməlum əmr")
        except (ValueError, IndexError) as error:
            print("  xəta:", error)


# 3. Stack, Queue, Deque: sadə brauzer

def browser_menu():
    print("\n=== 3. Brauzer: Stack, Queue, Deque ===")
    print("  open aztu.edu.az səhifə aç (köhnəsi geri stack-ə düşür)")
    print("  back             geri (stack)")
    print("  fwd              irəli (stack)")
    print("  dl fayl.pdf      yükləmə növbəsinə əlavə et (queue)")
    print("  next             növbədəki birinci faylı yüklə (queue)")
    print("  bench            ssenari və queue müqayisəsi")
    print("  q                menyuya qayıt")

    browser = Browser()
    while True:
        browser.show()
        cmd, args = read_command()
        try:
            if cmd == "q":
                return
            elif cmd == "open":
                browser.open(args[0])
            elif cmd == "back":
                browser.back()
            elif cmd == "fwd":
                browser.forward()
            elif cmd == "dl":
                browser.add_download(args[0])
            elif cmd == "next":
                print("  yükləndi:", browser.next_download())
            elif cmd == "bench":
                stack_queue.demo()
            else:
                print("  naməlum əmr")
        except IndexError as error:
            print("  xəta:", error)


# 4. Hash Table

def hash_table_menu():
    print("\n=== 4. Hash Table (chaining) ===")
    print("  put alma 1       əlavə et və ya yenilə")
    print("  get alma         axtar")
    print("  del alma         sil")
    print("  new 5 off        yeni cədvəl: tutum 5, rehash söndürülüb (on - yandırılıb)")
    print("  hash abc cba     iki hash funksiyasını müqayisə et")
    print("  bench            collision nümunələri və load factor ölçümü")
    print("  q                menyuya qayıt")

    table = HashTable(capacity=4)
    while True:
        table.show()
        cmd, args = read_command()
        try:
            if cmd == "q":
                return
            elif cmd == "put":
                old = table.capacity
                table.put(args[0], args[1])
                if table.capacity != old:
                    print(f"  load factor 0.75-i keçdi, rehash: {old} -> {table.capacity}")
            elif cmd == "get":
                value = table.get(args[0])
                bucket = table.bucket_index(args[0])
                print(f"  {args[0]} = {value}  (bucket {bucket}, {table.last_compares} müqayisə)")
            elif cmd == "del":
                if not table.delete(args[0]):
                    print("  tapılmadı")
            elif cmd == "new":
                rehash = len(args) < 2 or args[1] == "on"
                table = HashTable(int(args[0]), rehash)
            elif cmd == "hash":
                for key in args:
                    print(f"  {key}: cəm hash -> bucket {simple_hash(key, table.capacity)}, "
                          f"polinom hash -> bucket {poly_hash(key, table.capacity)}")
            elif cmd == "bench":
                hash_table.demo()
            else:
                print("  naməlum əmr")
        except (ValueError, IndexError) as error:
            print("  xəta:", error)
        except KeyError:
            print("  tapılmadı")


# 5. Binary Search Tree

def bst_menu():
    print("\n=== 5. Binary Search Tree ===")
    print("  add 35 65        əlavə et")
    print("  del 30           sil")
    print("  find 65          axtar, keçilən yolu göstər")
    print("  walk             preorder, inorder, postorder")
    print("  sorted 7         1..7 sıralı əlavə et (ağac xəttə çevrilir)")
    print("  clear            ağacı təmizlə")
    print("  bench            sıralı və təsadüfi əlavənin müqayisəsi")
    print("  q                menyuya qayıt")

    tree = BST()
    for key in [50, 30, 70, 20, 40, 60, 80]:
        tree.insert(key)
    while True:
        tree.show()
        print("  hündürlük =", tree.height(tree.root))
        cmd, args = read_command()
        try:
            if cmd == "q":
                return
            elif cmd == "add":
                for x in args:
                    tree.insert(int(x))
            elif cmd == "del":
                if not tree.delete(int(args[0])):
                    print("  tapılmadı")
            elif cmd == "find":
                found, path = tree.search(int(args[0]))
                if found:
                    print(f"  tapıldı, yol: {path}, {len(path)} müqayisə")
                else:
                    print(f"  yoxdur, yol: {path}, {len(path)} müqayisə")
            elif cmd == "walk":
                print("  preorder: ", tree.preorder(tree.root, []))
                print("  inorder:  ", tree.inorder(tree.root, []))
                print("  postorder:", tree.postorder(tree.root, []))
            elif cmd == "sorted":
                tree = BST()
                for key in range(1, int(args[0]) + 1):
                    tree.insert(key)
                print("  hər açar əvvəlkindən böyükdür, ona görə həmişə sağa gedir")
            elif cmd == "clear":
                tree = BST()
            elif cmd == "bench":
                bst.demo()
            else:
                print("  naməlum əmr")
        except (ValueError, IndexError) as error:
            print("  xəta:", error)


def main():
    while True:
        print("\nData Structures konsol tətbiqi")
        print("  1. Array və Dynamic Array")
        print("  2. Singly və Doubly Linked List")
        print("  3. Stack, Queue və Deque (brauzer)")
        print("  4. Hash Table (chaining)")
        print("  5. Binary Search Tree")
        print("  0. Çıxış")
        choice = input("Seçim: ").strip()
        if choice == "1":
            array_menu()
        elif choice == "2":
            linked_list_menu()
        elif choice == "3":
            browser_menu()
        elif choice == "4":
            hash_table_menu()
        elif choice == "5":
            bst_menu()
        elif choice == "0":
            break


if __name__ == "__main__":
    main()
