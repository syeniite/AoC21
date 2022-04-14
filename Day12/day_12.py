from time import perf_counter


def read_file(file_name):
    def add_to_adj(s, t):
        if s not in adj:
            adj[s] = [t]
        else:
            adj[s].append(t)

    with open(file_name, "r") as f:
        adj = {}

        for line in f.readlines():
            u, v = line.strip().split("-")
            add_to_adj(u, v)
            add_to_adj(v, u)

    return adj


def get_number_of_all_paths(adj, starting_vertex='start', ending_vertex='end'):
    def dfs_visit(vertex, visited_small_caves, curr_path):
        # curr path for debugging purposes
        # print(visited_small_caves)
        nonlocal num_of_all_possible_paths

        if vertex == ending_vertex:
            # print(curr_path)
            num_of_all_possible_paths += 1
        else:
            for neighbor in adj[vertex]:
                if neighbor not in visited_small_caves:
                    if neighbor.islower():
                        # ugh copying them all the time? :/
                        dfs_visit(neighbor, visited_small_caves.copy() | {neighbor}, curr_path + [neighbor])
                    else:
                        dfs_visit(neighbor, visited_small_caves.copy(), curr_path + [neighbor])

    num_of_all_possible_paths = 0
    small_caves = set()

    if starting_vertex.islower():
        small_caves.add(starting_vertex)

    dfs_visit(starting_vertex, small_caves, [starting_vertex])

    return num_of_all_possible_paths


def get_number_of_all_paths_single_small_cave_twice(adj, starting_vertex='start', ending_vertex='end'):
    def dfs_visit(vertex, visited_small_caves, small_cave_visited_twice, curr_path):
        if vertex == ending_vertex:
            all_paths.append(curr_path)
        else:
            for neighbor in adj[vertex]:
                if neighbor not in visited_small_caves:
                    if neighbor.islower():
                        if not small_cave_visited_twice:
                            dfs_visit(neighbor, visited_small_caves.copy(), True, curr_path + [neighbor])

                        dfs_visit(neighbor, visited_small_caves.copy() | {neighbor}, small_cave_visited_twice,
                                  curr_path + [neighbor])
                    else:
                        dfs_visit(neighbor, visited_small_caves.copy(), small_cave_visited_twice,
                                  curr_path + [neighbor])

    all_paths = []
    dfs_visit(starting_vertex,  {starting_vertex}, False, [starting_vertex])

    # len(set([''.join(path) for path in all_paths]))
    return len(set([''.join(path) for path in all_paths]))


if __name__ == '__main__':
    t1 = perf_counter()
    graph = read_file("input.txt")
    num = get_number_of_all_paths_single_small_cave_twice(graph)
    t2 = perf_counter()
    print(f'answer={num} in {t2-t1:.3f}s')
