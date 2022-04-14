from collections import namedtuple

Entry = namedtuple("Entry", "unique_digits output")


def read_file(file_name):
    def read_entry(line):
        unique_digits, output = line.split("|")
        return Entry([d.strip() for d in unique_digits.strip().split(" ")],
                     [o.strip() for o in output.strip().split(" ")])

    with open(file_name, "r") as f:
        return [read_entry(line) for line in f.readlines()]


def get_intersection(*args):
    chars = get_segment_count_map(*args)
    return [key for key in chars if chars[key] > 1]


def get_segment_count_map(*args):
    chars = {}
    for arg in args:
        for d in arg:
            if d in chars:
                chars[d] += 1
            else:
                chars[d] = 1

    return chars


def get_complement(A, B):
    return [e for e in A if e not in B]


def deduce_encoding(encoded_digits):
    encoded_digit_to_real_number = ["" for _ in range(10)]
    real_segment_to_encoded = dict()
    encoded_digit_to_real_number[1] = [d for d in encoded_digits if len(d) == 2][0]
    encoded_digit_to_real_number[7] = [d for d in encoded_digits if len(d) == 3][0]
    encoded_digit_to_real_number[4] = [d for d in encoded_digits if len(d) == 4][0]
    encoded_digit_to_real_number[8] = [d for d in encoded_digits if len(d) == 7][0]

    # 7 without 1 maps to exactly one segment
    real_segment_to_encoded['a'] = get_complement(encoded_digit_to_real_number[7],
                                                  get_intersection(encoded_digit_to_real_number[1],
                                                                   encoded_digit_to_real_number[7]))

    # 2, 3, 5 have exactly 5 segments but only 2 uses segment e with 4 e can be deduced
    seg_count_map = get_segment_count_map(*[d for d in encoded_digits if len(d) == 5], encoded_digit_to_real_number[4])
    real_segment_to_encoded['e'] = [key for key in seg_count_map if seg_count_map[key] == 1]

    # 2 and 1 only share one segment with segment e we can deduce f
    encoded_digit_to_real_number[2] = \
        [d for d in encoded_digits if len(d) == 5 and real_segment_to_encoded['e'][0] in d][0]
    real_segment_to_encoded['f'] = get_complement(encoded_digit_to_real_number[1], encoded_digit_to_real_number[2])

    # with 1 and f we can deduce c
    real_segment_to_encoded['c'] = \
        [d for d in encoded_digit_to_real_number[1] if d not in real_segment_to_encoded['f']]

    # 3 and c and not e and 4 => d, c, f => d segment
    encoded_digit_to_real_number[3] = \
        [d for d in encoded_digits if len(d) == 5 and real_segment_to_encoded['c'][0] in d and
         real_segment_to_encoded['e'][0] not in d][0]
    real_segment_to_encoded['d'] = get_complement(
        get_intersection(encoded_digit_to_real_number[3], encoded_digit_to_real_number[4]),
        [real_segment_to_encoded['c'][0], real_segment_to_encoded['f'][0]])

    # we know all segments of three except for g => deduce g segment
    real_segment_to_encoded['g'] = [d for d in encoded_digit_to_real_number[3] if d not in
                                        [real_segment_to_encoded['a'][0], real_segment_to_encoded['c'][0],
                                         real_segment_to_encoded['d'][0], real_segment_to_encoded['f'][0]]]

    # b is the only remaining segment
    real_segment_to_encoded['b'] = [d for d in 'abcdefg' if d not in
                                    [x for c in real_segment_to_encoded.values() for x in c]]

    encoded_to_real_seg = dict()

    for k, item in real_segment_to_encoded.items():
        encoded_to_real_seg[item[0]] = k

    return encoded_to_real_seg


def read_encoded_number(resolver, encoded_number):
    table = {'abcefg': 0, 'cf': 1, 'acdeg': 2, 'acdfg': 3, 'bcdf': 4, 'abdfg': 5, 'abdefg': 6, 'acf': 7, 'abcdefg': 8,
             'abcdfg': 9}

    return table[''.join(sorted(resolver[d][0] for d in encoded_number))]


def add_all_output_values(entries):
    output_val_sum = 0

    for entry in entries:
        dictionary = deduce_encoding(entry.unique_digits)
        output_val_sum += int(''.join([str(read_encoded_number(dictionary, out)) for out in entry.output]))

    return output_val_sum


if __name__ == '__main__':
    print(add_all_output_values(read_file("input.txt")))
