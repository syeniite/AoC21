from functools import reduce


def read_file(file_name):
    with open(file_name, "r") as f:
        return [[int(n) for n in line.strip()] for line in f.readlines()]


def get_risk_level(height):
    return height + 1


def get_total_risk_level(height_map):
    def is_low_point(i, j):
        left_low = j > 0 and height_map[i][j-1] <= height_map[i][j]
        right_low = j < len(height_map[i])-1 and height_map[i][j+1] <= height_map[i][j]
        up_low = i > 0 and height_map[i-1][j] <= height_map[i][j]
        down_low = i < len(height_map)-1 and height_map[i+1][j] <= height_map[i][j]
        return not (left_low or right_low or up_low or down_low)

    total_risk_level = 0

    for row in range(len(height_map)):
        for col in range(len(height_map[0])):
            if is_low_point(row, col):
                total_risk_level += get_risk_level(height_map[row][col])

    return total_risk_level


def get_all_basin_sizes_dfs(height_map):
    def dfs_visit(i, j):
        visited[i][j] = True
        basin_size_neighbors = 0

        if j > 0 and height_map[i][j-1] != 9 and not visited[i][j-1]:
            basin_size_neighbors += dfs_visit(i, j-1)

        if j < len(height_map[i])-1 and height_map[i][j+1] != 9 and not visited[i][j+1]:
            basin_size_neighbors += dfs_visit(i, j+1)

        if i > 0 and height_map[i-1][j] != 9 and not visited[i-1][j]:
            basin_size_neighbors += dfs_visit(i-1, j)

        if i < len(height_map)-1 and height_map[i+1][j] != 9 and not visited[i+1][j]:
            basin_size_neighbors += dfs_visit(i+1, j)

        return basin_size_neighbors + 1

    visited = [[False for _ in range(len(height_map[0]))] for _ in range(len(height_map))]
    basin_sizes = []

    for row in range(len(height_map)):
        for col in range(len(height_map[0])):
            if not visited[row][col] and height_map[row][col] != 9:
                basin_sizes.append(dfs_visit(row, col))

    return basin_sizes


def ppmatrix(m):
    for i in range(len(m)):
        for j in range(len(m[0])):
            print(int(m[i][j]), end="")
        print()
    print()


def get_prod_of_three_largest_basins(basin_sizes):
    return reduce(lambda curr, b: curr*b, sorted(basin_sizes)[-3:])


if __name__ == '__main__':
    height_map_input = read_file("input.txt")
    # import numpy as np
    # print(np.matrix(height_map_input))

    # print(get_total_risk_level(height_map_input))
    print(get_prod_of_three_largest_basins(get_all_basin_sizes_dfs(height_map_input)))
