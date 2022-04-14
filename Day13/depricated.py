"""from collections import namedtuple
from dataclasses import dataclass


class LinkedList:

    def __init__(self, head=None):
        self.head = head
        self.tail = head
        self.length = 1 if head else 0

    def __len__(self):
        return self.length

    def __str__(self):
        if not self.tail:
            return "[]"
        else:
            current = self.head
            out = []

            while current:
                out.append(f'({current.x}, {current.y})')
                current = current.next

            return f"[{', '.join(out)}]"

    def add_last(self, element):
        self.length += 1

        if self.tail:
            element.prev = self.tail
            self.tail.next = element
            self.tail = element
        else:
            self.tail = element
            self.head = self.tail

    @staticmethod
    def add_right_to(element, to_be_inserted):
        to_be_inserted.prev = element
        to_be_inserted.next = element.next
        element.next.prev = to_be_inserted
        element.next = to_be_inserted

    def remove(self, element):
        if not element.prev:
            self.head = element.next
            return
        if not element.next:
            self.tail = element.prev
        else:
            element.prev.next = element.next
            element.next.prev = element.prev


FoldInstruction = namedtuple("FoldInstruction", "direction value")
# Dot = namedtuple("Dot", "x y prev next")


@dataclass
class Dot:

    x: int
    y: int
    prev = None
    next = None


def read_file(file_name):
    with open(file_name, "r") as f:
        dots, instructions = [], []

        while line := f.readline().strip():
            if not line:
                break
            x, y = line.split(",")
            dots.append(Dot(int(x), int(y)))

        while line := f.readline().strip():
            dir_instr, value = line.split("=")
            instructions.append(FoldInstruction(dir_instr[-1], int(value)))

    return dots, instructions


def find_first_in_sorted(lst, val, key):
    high = len(lst) - 1
    low = 0

    while high >= low:
        mid = (low + high) // 2
        if (mid == 0 or val > key(lst[mid-1])) and key(lst[mid]) == val:
            return mid
        elif val > key(lst[mid]):
            low = mid + 1
        else:
            high = mid - 1

    return -1


def find_last_in_sorted(lst, val, key):
    high = len(lst) - 1
    low = 0

    while high >= low:
        mid = (low + high) // 2
        if (mid == len(lst)-1 or val < key(lst[mid+1])) and key(lst[mid]) == val:
            return mid
        elif val < key(lst[mid]):
            high = mid - 1
        else:
            low = mid + 1

    return -1


def get_sorted_dots_in_linked_list(all_dots):
    sorted_dots_by_x = sorted(all_dots, key=lambda k: k.x)
    current_value = sorted_dots_by_x[0].x
    result = []

    while True:
        first_occurrence = find_first_in_sorted(sorted_dots_by_x, current_value, lambda k: k.x)
        last_occurrence = find_last_in_sorted(sorted_dots_by_x, current_value, lambda k: k.x)

        for element in sorted(sorted_dots_by_x[first_occurrence:last_occurrence+1], key=lambda k: k.y):
            result.append(element)

        if last_occurrence == len(sorted_dots_by_x) - 1:
            break
        else:
            current_value = sorted_dots_by_x[last_occurrence+1].x

    linked_list = LinkedList()
    for element in result:
        linked_list.add_last(element)

    return linked_list


def fold(fold_instruction: FoldInstruction, sorted_dots: LinkedList):
    ..."""
