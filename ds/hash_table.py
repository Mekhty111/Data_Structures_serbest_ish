# Mövzu 4: öz hash table-ımız. Collision chaining üsulu ilə həll olunur:
# hər bucket bir siyahıdır, eyni bucket-ə düşən açarlar həmin siyahıya əlavə olunur.
import random
import string
from time import perf_counter

from .common import micro, print_table, print_title


def simple_hash(key, capacity):
    """Pis hash: simvol kodlarının cəmi. abc və cba həmişə eyni bucket-ə düşür."""
    total = 0
    for ch in key:
        total += ord(ch)
    return total % capacity


def poly_hash(key, capacity):
    """Polinomial hash: h = h * 31 + kod. Simvolların sırası da nəzərə alınır."""
    h = 0
    for ch in key:
        h = (h * 31 + ord(ch)) % 4294967296
    return h % capacity


class HashTable:
    def __init__(self, capacity=4, rehash=True):
        self.capacity = capacity
        self.rehash_on = rehash
        self.buckets = []
        for i in range(capacity):
            self.buckets.append([])
        self.size = 0
        self.last_compares = 0             # sonuncu axtarışda neçə açar yoxlandı

    def load_factor(self):
        return self.size / self.capacity

    def bucket_index(self, key):
        return poly_hash(key, self.capacity)

    def put(self, key, value):
        bucket = self.buckets[self.bucket_index(key)]
        for pair in bucket:
            if pair[0] == key:             # açar artıq var, dəyəri yeniləyirik
                pair[1] = value
                return
        bucket.append([key, value])        # collision olsa da, sadəcə siyahının sonuna
        self.size += 1
        if self.rehash_on and self.load_factor() > 0.75:
            self.rehash()

    def get(self, key):
        bucket = self.buckets[self.bucket_index(key)]
        self.last_compares = 0
        for pair in bucket:
            self.last_compares += 1
            if pair[0] == key:
                return pair[1]
        raise KeyError(key)

    def contains(self, key):
        bucket = self.buckets[self.bucket_index(key)]
        self.last_compares = 0
        for pair in bucket:
            self.last_compares += 1
            if pair[0] == key:
                return True
        return False

    def delete(self, key):
        bucket = self.buckets[self.bucket_index(key)]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket.pop(i)
                self.size -= 1
                return True
        return False

    def rehash(self):
        """Tutumu 2 dəfə artırır və bütün açarları yenidən yerləşdirir."""
        old_buckets = self.buckets
        self.capacity = self.capacity * 2
        self.buckets = []
        for i in range(self.capacity):
            self.buckets.append([])
        for bucket in old_buckets:
            for pair in bucket:
                self.buckets[self.bucket_index(pair[0])].append(pair)

    def longest_chain(self):
        longest = 0
        for bucket in self.buckets:
            if len(bucket) > longest:
                longest = len(bucket)
        return longest

    def collisions(self):
        used = 0
        for bucket in self.buckets:
            if len(bucket) > 0:
                used += 1
        return self.size - used

    def show(self):
        for i in range(self.capacity):
            bucket = self.buckets[i]
            if len(bucket) == 0:
                print(f"  [{i}] boş")
            else:
                parts = []
                for pair in bucket:
                    parts.append(f"{pair[0]}:{pair[1]}")
                print(f"  [{i}] " + " -> ".join(parts))
        print(f"  size={self.size} capacity={self.capacity} load factor={round(self.load_factor(), 2)} "
              f"collision={self.collisions()}")


def random_keys(n, seed):
    rnd = random.Random(seed)
    keys = []
    for i in range(n):
        word = ""
        for j in range(8):
            word += rnd.choice(string.ascii_lowercase)
        keys.append(word)
    return keys


def load_factor_benchmark():
    """5000 açar, tutum dəyişir, rehash söndürülüb. Olmayan açar axtarılır: bütün zəncir yoxlanır."""
    n = 5000
    keys = random_keys(n, 1)
    missing = []
    for k in keys[:500]:
        missing.append(k.upper())         # böyük hərflə: cədvəldə yoxdur

    rows = []
    for lf in [0.5, 1, 2, 4, 8, 16, 32, 64]:
        table = HashTable(capacity=int(n / lf), rehash=False)
        for k in keys:
            table.put(k, 1)

        compares = 0
        for k in missing:
            table.contains(k)
            compares += table.last_compares

        start = perf_counter()
        for k in missing:
            table.contains(k)
        search_time = micro(start, len(missing))

        rows.append([lf, table.capacity, table.longest_chain(), round(compares / len(missing), 1), search_time])
    return rows


def demo():
    print_title("4. Hash Table (chaining)")

    print("\nİş prinsipi")
    print("  index = hash(key) % capacity. Hər bucket bir siyahıdır.")
    print("  İki açar eyni bucket-ə düşəndə (collision) ikincisi həmin siyahının sonuna əlavə olunur.")
    print("  Load factor = element sayı / tutum. 0.75-i keçəndə tutum 2 dəfə artır (rehash).")

    print("\nCollision nümunəsi (tutum 8)")
    rows = []
    for key in ["abc", "cba", "bca", "listen", "silent"]:
        rows.append([key, simple_hash(key, 8), poly_hash(key, 8)])
    print_table(["açar", "cəm hash -> bucket", "polinom hash -> bucket"], rows)

    print("\nChaining: tutum 5, 8 meyvə, rehash söndürülüb")
    t = HashTable(capacity=5, rehash=False)
    fruits = ["alma", "armud", "banan", "gilas", "heyva", "nar", "üzüm", "limon"]
    for i in range(len(fruits)):
        t.put(fruits[i], i)
    t.show()
    print(f"  get('nar') = {t.get('nar')}, zəncirdə {t.last_compares} açar yoxlandı")

    print("\nAvtomatik rehash: 40 açar əlavə edirik")
    t = HashTable(capacity=4)
    for key in random_keys(40, 1):
        old = t.capacity
        t.put(key, 1)
        if t.capacity != old:
            print(f"  {t.size}-ci açarda tutum {old} -> {t.capacity}")

    print("\nLoad factor və olmayan açarın axtarış vaxtı (n=5000)")
    print_table(["load factor", "tutum", "ən uzun zəncir", "orta müqayisə", "axtarış µs"], load_factor_benchmark())

    print("\nNəticə")
    print("  Load factor kiçik saxlananda zəncirlər qısa olur və axtarış orta hesabla O(1) qalır.")
