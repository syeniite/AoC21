from collections import deque


def read_file(file_name):
    with open(file_name, "r") as f:
        return [[int(n) for n in line.strip()] for line in f.readlines()]


def update_energy_levels(curr_levels):
    for i in range(len(curr_levels)):
        for j in range(len(curr_levels[0])):
            curr_levels[i][j] += 1


def reset_energy_levels_greater_nine(curr_levels):
    for i in range(len(curr_levels)):
        for j in range(len(curr_levels[0])):
            if curr_levels[i][j] > 9:
                curr_levels[i][j] = 0


def get_indices_of_adjacent_cells(i, j):
    return [(i, j-1), (i-1, j), (i, j+1), (i+1, j), (i-1, j-1), (i-1, j+1), (i+1, j+1), (i+1, j-1)]


def is_valid_cell(i, j, m):
    return 0 <= i < len(m) and 0 <= j < len(m[i])


def flash_bfs(energy_levels):
    is_flashing_octopus = [[False for _ in range(len(energy_levels[0]))] for _ in range(len(energy_levels))]
    flash_count = 0

    for row in range(len(energy_levels)):
        for col in range(len(energy_levels[0])):
            if energy_levels[row][col] > 9 and not is_flashing_octopus[row][col]:
                is_flashing_octopus[row][col] = True
                q = deque()
                q.append((row, col))

                while q:
                    current_octo = q.popleft()
                    flash_count += 1

                    for i, j in get_indices_of_adjacent_cells(current_octo[0], current_octo[1]):
                        if is_valid_cell(i, j, energy_levels):
                            energy_levels[i][j] += 1

                            if not is_flashing_octopus[i][j] and energy_levels[i][j] > 9:
                                q.append((i, j))
                                is_flashing_octopus[i][j] = True

    return flash_count


def simulate(energy_levels, steps):
    total_flashes = 0

    for _ in range(steps):
        update_energy_levels(energy_levels)
        total_flashes += flash_bfs(energy_levels)
        reset_energy_levels_greater_nine(energy_levels)

    return total_flashes


def simulate_until_first_synchronization(energy_levels):
    steps = 0
    total_flashes = 0

    while total_flashes != len(energy_levels)*len(energy_levels[0]):
        update_energy_levels(energy_levels)
        total_flashes = flash_bfs(energy_levels)
        reset_energy_levels_greater_nine(energy_levels)
        steps += 1

    return steps


def pp_matrix(m):
    for i in range(len(m)):
        for j in range(len(m[0])):
            print(int(m[i][j]), end=" ")
        print()
    print()


if __name__ == '__main__':
    # print(simulate(read_file("input.txt"), 100))
    print(simulate_until_first_synchronization(read_file("input.txt")))
