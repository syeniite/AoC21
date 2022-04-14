from collections import namedtuple


Segment = namedtuple("Segment", "start_x start_y end_x end_y")


def parse_file(file_name):
    with open(file_name, "r") as f:
        return [Segment(*[int(i) for i in line.replace("->", ",").split(",")]) for line in f.readlines()]


def get_domain_of_segment(seg):
    def signum(x, y):
        if x > y:
            return 1
        return -1 if x < y else 0

    direction_vector_normed = (signum(seg.end_x, seg.start_x), signum(seg.end_y, seg.start_y))

    domain = [(seg.start_x, seg.start_y)]
    while domain[-1] != (seg.end_x, seg.end_y):
        domain.append((domain[-1][0] + direction_vector_normed[0], domain[-1][1] + direction_vector_normed[1]))

    return domain


def get_range(x, y):
    if x < y:
        return range(x, y+1)
    elif y < x:
        return range(y, x+1)
    else:
        return []


def calc_overlaps(segments):
    max_x = max(x for seg in segments for x in (seg.start_x, seg.end_x)) + 1
    max_y = max(y for seg in segments for y in (seg.start_y, seg.end_y)) + 1
    overlap_map = [[0 for _ in range(max_x)] for _ in range(max_y)]

    for seg in segments:
        for (i, j) in get_domain_of_segment(seg):
            overlap_map[j][i] += 1

    return overlap_map


def get_num_of_overlaps(overlap_map):
    return sum(sum(e > 1 for e in row) for row in overlap_map)


def pprint_overlaps(m):
    for i in range(len(m)):
        for j in range(len(m[0])):
            print("." if m[i][j] == 0 else m[i][j], end=" ")
        print()
    print()


if __name__ == '__main__':
    print(get_num_of_overlaps(calc_overlaps(parse_file("input.txt"))))
