def read_file(file_name):
    with open(file_name, "r") as f:
        return [int(n) for n in f.readline().split(",")]


def get_median_lazy(horizontal_positions):
    return sorted(horizontal_positions)[len(horizontal_positions)//2]


def get_total_fuel_cost(horizontal_positions, m):
    return sum([sum(i for i in range(abs(pos - m)+1)) for pos in horizontal_positions])


def brute_force(horizontal_positions):
    def fuel_cost(p, q):
        return abs(p-q)*(abs(p-q)+1)*0.5

    curr_min = float('inf')
    for i in range(min(horizontal_positions), max(horizontal_positions)+1):
        total_fuel_cost = sum(fuel_cost(p, i) for p in horizontal_positions)

        if total_fuel_cost < curr_min:
            curr_min = total_fuel_cost

    return curr_min


if __name__ == '__main__':
    positions = read_file("input.txt")
    # print(get_average(read_file("example_one_literal.txt")))
    print(brute_force(positions))
