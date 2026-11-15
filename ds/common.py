# Ortaq funksiyalar: vaxt ölçmə və cədvəl çapı.
from time import perf_counter


def micro(start, count):
    """start anından bəri keçən vaxtı count əməliyyata bölür. Nəticə mikrosaniyədir."""
    return round((perf_counter() - start) / count * 1_000_000, 3)


def print_title(text):
    print()
    print(text)
    print("=" * len(text))


def print_table(header, rows):
    # hər sütunun eni: başlıqdan və ən uzun dəyərdən böyük olanı
    widths = []
    for i in range(len(header)):
        width = len(str(header[i]))
        for row in rows:
            if len(str(row[i])) > width:
                width = len(str(row[i]))
        widths.append(width)

    line = "  "
    for i in range(len(header)):
        line += str(header[i]).ljust(widths[i]) + "  "
    print(line)

    line = "  "
    for i in range(len(header)):
        line += "-" * widths[i] + "  "
    print(line)

    for row in rows:
        line = "  "
        for i in range(len(row)):
            line += str(row[i]).ljust(widths[i]) + "  "
        print(line)
