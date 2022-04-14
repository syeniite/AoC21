def read_file(file_name):
    with open(file_name, "r") as f:
        return [int(n) for n in f.readline().split(",")]


def simulate(seed, day, reset_val=6, max_val=8):
    population_status = [0 for _ in range(max_val+1)]

    for f in seed:
        population_status[f] += 1

    for _ in range(day):
        new_fish = population_status[0]

        for i in range(1, len(population_status)):
            population_status[i-1] = population_status[i]

        population_status[reset_val] += new_fish
        population_status[max_val] = new_fish

    return sum(population_status)


if __name__ == '__main__':
    print(simulate(read_file("input.txt"), 256))
