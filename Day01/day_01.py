
def read_file(file_path: str):
    with open(file_path, "r") as f:
        return [int(line) for line in f.readlines()]


def get_sliding_window(reads):
    return [reads[i] + reads[i+1] + reads[i+2] for i in range(len(reads)-2)]


def has_increased(accumulated_reads):
    return [accumulated_reads[i] < accumulated_reads[i+1] for i in range(len(accumulated_reads) - 1)]


if __name__ == '__main__':
    measurements = read_file("input.txt")
    accumulated = get_sliding_window(measurements)
    print(sum(has_increased(accumulated)))
