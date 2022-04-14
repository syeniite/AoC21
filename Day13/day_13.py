from collections import namedtuple
from dataclasses import dataclass
from time import perf_counter

FoldInstruction = namedtuple("FoldInstruction", "direction value")


@dataclass
class Dot:
    x: int
    y: int


def read_file(file_name):
    with open(file_name, "r") as f:
        _dots, _instructions = [], []

        while line := f.readline().strip():
            if not line:
                break
            x, y = line.split(",")
            _dots.append(Dot(int(x), int(y)))

        while line := f.readline().strip():
            dir_instr, value = line.split("=")
            _instructions.append(FoldInstruction(dir_instr[-1], int(value)))

    return _dots, _instructions


def fold(dots_sorted_by_x, dots_sorted_by_y, instruction):
    # horizontal fold
    if instruction.direction == "y":
        first_fold_index = find_val(dots_sorted_by_y, instruction.value, lambda k: k.y, True)
        for i in range(first_fold_index, len(dots_sorted_by_y)):
            # fold up
            folded_y_position = 2*instruction.value - dots_sorted_by_y[i].y
            dots_sorted_by_y[i].y = folded_y_position

    else:
        # vertical fold
        first_fold_index = find_val(dots_sorted_by_x, instruction.value, lambda k: k.x, True)
        for i in range(first_fold_index, len(dots_sorted_by_x)):
            # fold left
            folded_x_position = 2 * instruction.value - dots_sorted_by_x[i].x
            dots_sorted_by_x[i].x = folded_x_position

    return sorted(dots_sorted_by_x, key=lambda k: k.x), sorted(dots_sorted_by_y, key=lambda k: k.y)


def find_val(lst, val, key, get_bigger=False):
    high = len(lst) - 1
    low = 0

    while high >= low:
        mid = (low + high) // 2

        if key(lst[mid]) == val:
            return mid
        elif val < key(lst[mid]):
            high = mid - 1
        else:
            low = mid + 1

    if get_bigger:
        return low
    return -1


def get_num_of_dots(dots_x, dots_y, print_fold=False):
    m = [['.' for _ in range(dots_x[-1].x+1)] for _ in range(dots_y[-1].y+1)]

    for dot in dots_x:
        m[dot.y][dot.x] = '#'

    if print_fold:
        for i in range(len(m)):
            for j in range(len(m[0])):
                print(m[i][j], end="")
            print()
        print()

    return sum(line.count("#") for line in m)


if __name__ == '__main__':
    t1 = perf_counter()
    dots, instructions = read_file("input.txt")
    folded_x = sorted(dots, key=lambda k: k.x)
    folded_y = sorted(dots, key=lambda k: k.y)

    for fold_instruction in instructions:
        folded_x, folded_y = fold(folded_x, folded_y, fold_instruction)
    t2 = perf_counter()
    print(get_num_of_dots(folded_x, folded_y, True))
    print(f'total time (read+solve): {t2-t1:.4f}s')
