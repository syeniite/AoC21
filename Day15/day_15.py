import heapq
from time import perf_counter


def read_map(file_name):
    with open(file_name, "r") as f:
        return [[int(risk_level.strip()) for risk_level in line.strip()]
                for line in f.readlines()]


def expand_map(initial_risk_map):
    expanded_map = [[0 for _ in range(len(initial_risk_map[0])*5)] for _ in range(len(initial_risk_map)*5)]

    for i in range(len(expanded_map)):
        for j in range(len(expanded_map[0])):
            new_risk_level = initial_risk_map[i % len(initial_risk_map)][j % len(initial_risk_map[0])] \
                             + i // len(initial_risk_map) + j // len(initial_risk_map[0])

            expanded_map[i][j] = new_risk_level % 10 + new_risk_level//10

    return expanded_map


def get_neighbours(i, j):
    return [(i, j-1), (i-1, j), (i, j+1), (i+1, j)]


def is_valid(i, j, risk_map):
    return 0 <= i < len(risk_map) and 0 <= j < len(risk_map[0])


def get_total_risk_level_dijkstra(risk_map, start=(0, 0)):
    def set_visited(pair, val):
        visited[pair[0]][pair[1]] = val

    def set_total_risk(pair, val):
        total_risk[pair[0]][pair[1]] = val

    def get_visited(pair):
        return visited[pair[0]][pair[1]]

    def get_total_risk(pair):
        return total_risk[pair[0]][pair[1]]

    def get_risk(pair):
        return risk_map[pair[0]][pair[1]]

    queue = []
    visited = [[False for _ in range(len(risk_map[0]))] for _ in range(len(risk_map))]
    total_risk = [[float('inf') for _ in range(len(risk_map[0]))] for _ in range(len(risk_map))]

    set_total_risk(start, 0)

    heapq.heappush(queue, (get_total_risk(start), start))

    while queue:
        _, node = heapq.heappop(queue)

        if get_visited(node):
            continue
        set_visited(node, True)

        for neighbour in get_neighbours(*node):
            if is_valid(*neighbour, risk_map):
                # and not get_visited(neighbour)
                dist = get_total_risk(node) + get_risk(neighbour)

                if dist < get_total_risk(neighbour):
                    heapq.heappush(queue, (dist, neighbour))
                    set_total_risk(neighbour, dist)

    return total_risk[-1][-1]


def pp_matrix(m):
    for i in range(len(m)):
        for j in range(len(m[0])):
            print(int(m[i][j]), end=" ")
        print()
    print()


if __name__ == '__main__':
    risks = read_map("input.txt")
    t1 = perf_counter()
    _expanded_map = expand_map(risks)
    print(f"time elapsed to expand map {perf_counter()-t1:.3f}s")
    t2 = perf_counter()
    print(get_total_risk_level_dijkstra(_expanded_map))
    print(f"time elapsed to find path {perf_counter()-t2:.3f}s")
