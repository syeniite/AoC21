from __future__ import annotations
import copy
from dataclasses import dataclass
from functools import reduce
from math import ceil
from enum import Enum
from time import perf_counter


class Child(Enum):
    LEFT = 0
    RIGHT = 1

    @staticmethod
    def get_other(child: Child):
        return Child(1 - child.value)


class Pair:
    children: list[Pair | Number | None]
    parent: Pair | None

    def __init__(self, left=None, right=None, parent=None):
        self.parent = parent
        self.children = [None, None]
        self.set_child(Child.LEFT, left)
        self.set_child(Child.RIGHT, right)

    def is_left_child(self):
        return self.parent.children[Child.LEFT.value] is self

    def __repr__(self):
        return f'[{self.children[Child.LEFT.value]},{self.children[Child.RIGHT.value]}]'

    def get_child(self, child: Child):
        return self.children[child.value]

    def set_child(self, child_type: Child, child):
        self.children[child_type.value] = child

    def get_next_number(self, direction: Child):
        possible_turn = self.parent
        curr_pair = self

        while possible_turn is not None and possible_turn.get_child(direction) is curr_pair:
            curr_pair = possible_turn
            possible_turn = possible_turn.parent

        if possible_turn:
            next_number = possible_turn.get_child(direction)

            while not isinstance(next_number, Number):
                next_number = next_number.get_child(Child.get_other(direction))

            return next_number
        return None

    def explode(self, depth):
        if depth == 4:
            if next_left := self.get_next_number(Child.LEFT):
                next_left.value += self.get_child(Child.LEFT).value

            if next_right := self.get_next_number(Child.RIGHT):
                next_right.value += self.get_child(Child.RIGHT).value

            update_parent(self, Number(0, self.parent))
            return True
        return False

    def __add__(self, other):
        new_pair = Pair(left=self, right=other, parent=None)
        self.parent = new_pair
        other.parent = new_pair
        reduce_number(new_pair)

        return new_pair


@dataclass
class Number:
    value: int
    parent: Pair

    def __repr__(self):
        return str(self.value)

    def is_left_child(self):
        return self.parent.get_child(Child.LEFT) is self

    def split(self):
        if self.value >= 10:
            new_pair = Pair()
            new_pair.set_child(Child.LEFT, Number(self.value // 2, new_pair))
            new_pair.set_child(Child.RIGHT, Number(ceil(self.value / 2), new_pair))
            new_pair.parent = self.parent

            update_parent(self, new_pair)
            return True
        return False


def read_numbers_from_file(file_name):
    with open(file_name, "r") as f:
        return read_numbers(f)


def read_numbers(content):
    _pairs = [parse_pair(content, None)]

    while _pairs[-1]:
        content.read(1)  # read \n
        _pairs.append(parse_pair(content, None))
    _pairs.pop()

    return _pairs


def parse_pair(file, parent):
    new_char = file.read(1)
    if not new_char:
        return False

    if new_char == "[":
        new_pair = Pair()
        new_pair.parent = parent

        new_pair.set_child(Child.LEFT, parse_pair(file, new_pair))
        file.read(1)  # read ,
        new_pair.set_child(Child.RIGHT, parse_pair(file, new_pair))
        file.read(1)  # read ]

        return new_pair

    elif new_char.isdigit():
        return Number(int(new_char), parent)

    raise ValueError("Invalid Input")


def update_parent(node, update):
    node.parent.set_child(Child(not node.is_left_child()), update)


def reduce_number(pair):
    while explode_left_first(pair) or split_left_first(pair):
        continue


def explode_left_first(root, depth=0):
    if not isinstance(root, Number):
        return explode_left_first(root.get_child(Child.LEFT), depth=depth+1) or root.explode(depth) \
               or explode_left_first(root.get_child(Child.RIGHT), depth=depth+1)
    return False


def split_left_first(root):
    if isinstance(root, Number):
        return root.split()
    return split_left_first(root.get_child(Child.LEFT)) or split_left_first(root.get_child(Child.RIGHT))


def add_all(numbers):
    return reduce(lambda a, b: a + b, numbers)


def get_magnitude(number):
    if isinstance(number, Number):
        return number.value
    return 3 * get_magnitude(number.get_child(Child.LEFT)) + 2 * get_magnitude(number.get_child(Child.RIGHT))


def get_largest_magnitude_of_any_sum(numbers):
    return max(get_magnitude(copy.deepcopy(numbers[i]) + copy.deepcopy(numbers[j])) for i in range(len(numbers))
               for j in range(len(numbers)) if i != j)


if __name__ == '__main__':
    pairs = read_numbers_from_file("input.txt")
    print(get_largest_magnitude_of_any_sum(pairs))
