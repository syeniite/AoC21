from functools import reduce


def read_file(file_path: str) -> list:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def get_bit_count_at_each_index(binaries: list):
    return reduce(lambda curr, b: [i + int(j) for i, j in zip(curr, b)], binaries, [0] * len(binaries[0]))


def get_bit_count_at_index(binaries: list, i):
    return reduce(lambda curr, b: curr + int(b[i]), binaries, 0)


def get_most_common_bit_list(bit_count, len_binaries):
    return [i > len_binaries//2 for i in bit_count]


def get_num(bit_list):
    return reduce(lambda curr, b: (curr << 1) + int(b), bit_list, 0)


def filter_until_only_one(binaries, most_common_func):
    possible_values = binaries
    i = 0
    while len(possible_values) > 1 and i < len(binaries[0]):
        bit_count_at_i = get_bit_count_at_index(possible_values, i)
        possible_values = [
            val for val in possible_values if int(val[i]) == most_common_func(bit_count_at_i, len(possible_values))
        ]
        i += 1

    return possible_values[0]


def oxy_generator(bc, vals_len):
    return bc >= vals_len - bc


def oxy_scrub(bc, vals_len):
    return bc < vals_len - bc


if __name__ == '__main__':
    input_list = read_file("input.txt")
    # bit_list_most_common = get_most_common_bit_list(get_bit_count_at_each_index(input_list), len(input_list))
    # print(get_num(bit_list_most_common)*get_num([not b for b in bit_list_most_common]))
    print(int(filter_until_only_one(input_list, oxy_generator), 2)
          * int(filter_until_only_one(input_list, oxy_scrub), 2))
