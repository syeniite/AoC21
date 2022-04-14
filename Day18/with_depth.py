"""import copy
from dataclasses import dataclass, field
from functools import reduce
from math import ceil


@dataclass
class Pair:
    left: object = field(default_factory=object)
    right: object = field(default_factory=object)
    parent: object = field(default_factory=object)

    def is_left_child(self, child):
        return self.left is child

    def __repr__(self):
        return f'[{self.left},{self.right}]'


@dataclass
class Number:
    value: int
    parent: Pair

    def __repr__(self):
        return str(self.value)


def read_numbers_from_file(file_name):
    with open(file_name, "r") as f:
        return read_numbers(f)


def read_numbers(content):
    pairs = [parse_pair(content, None)]

    while pairs[-1]:
        content.read(1)  # read \n
        pairs.append(parse_pair(content, None))

    pairs.pop()

    return pairs


def parse_pair(file, parent):
    new_char = file.read(1)

    if not new_char:
        return False

    if new_char == "[":
        new_pair = Pair()
        new_pair.parent = parent

        new_pair.left = parse_pair(file, new_pair)
        file.read(1)  # read ,

        new_pair.right = parse_pair(file, new_pair)
        file.read(1)  # read ]

        return new_pair
    elif new_char.isdigit():
        return Number(int(new_char), parent)

    raise ValueError("Invalid Input")


def explode_pair(pair, depth):
    if depth == 4:
        possible_turn_right = pair.parent
        curr_pair = pair

        while possible_turn_right is not None and possible_turn_right.right is curr_pair:
            curr_pair = possible_turn_right
            possible_turn_right = possible_turn_right.parent

        if possible_turn_right:
            next_right_number = possible_turn_right.right

            while not isinstance(next_right_number, Number):
                next_right_number = next_right_number.left

            next_right_number.value += pair.right.value

        possible_turn_left = pair.parent
        curr_pair = pair

        while possible_turn_left is not None and possible_turn_left.left is curr_pair:
            curr_pair = possible_turn_left
            possible_turn_left = possible_turn_left.parent

        if possible_turn_left:
            next_left_number = possible_turn_left.left

            while not isinstance(next_left_number, Number):
                next_left_number = next_left_number.right

            next_left_number.value += pair.left.value

        if pair.parent.is_left_child(pair):
            pair.parent.left = Number(0, pair.parent)
        else:
            pair.parent.right = Number(0, pair.parent)

        return True
    return False


def split_number(number):
    if number.value >= 10:
        new_pair = Pair()
        new_pair.left = Number(number.value // 2, new_pair)
        new_pair.right = Number(ceil(number.value / 2), new_pair)
        new_pair.parent = number.parent

        if number.parent.is_left_child(number):
            number.parent.left = new_pair
        else:
            number.parent.right = new_pair
        return True
    return False


def add(pair_left, pair_right):
    new_pair = Pair(left=pair_left, right=pair_right, parent=None)
    pair_left.parent = new_pair
    pair_right.parent = new_pair
    reduce(new_pair)

    return new_pair


def reduce(pair):
    while explode_left_first(pair) or split_left_first(pair):
        continue


def explode_left_first(root, depth=0):
    if not isinstance(root, Number):
        return explode_left_first(root.left, depth=depth+1) or explode_pair(root, depth) \
               or explode_left_first(root.right, depth=depth+1)
    return False


def split_left_first(root):
    if isinstance(root, Number):
        return split_number(root)
    return split_left_first(root.left) or split_left_first(root.right)


def add_all(numbers):
    return reduce(lambda a, b: add(a, b), numbers)


def get_magnitude(number):
    if isinstance(number, Number):
        return number.value
    return 3*get_magnitude(number.left) + 2*get_magnitude(number.right)


def get_largest_magnitude_of_any_sum(numbers):
    return max(get_magnitude(add(copy.deepcopy(numbers[i]), copy.deepcopy(numbers[j]))) for i in range(len(numbers))
               for j in range(len(numbers)) if i != j)


if __name__ == '__main__':
    pairs = read_numbers_from_file("input.txt")
    print(get_largest_magnitude_of_any_sum(pairs))
"""