from time import perf_counter


class Cave:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.is_small_cave = name.islower()


def read_file(file_name):
    def add_new_cave(cave_name):
        nonlocal curr_id
        if cave_name not in name_to_id_map:
            name_to_id_map[cave_name] = curr_id
            adj.append([])
            caves.append(Cave(curr_id, cave_name))
            curr_id += 1

            return curr_id-1

        return name_to_id_map[cave_name]

    with open(file_name, "r") as f:
        name_to_id_map = {}
        caves = []
        adj = []
        curr_id = 0

        for line in f.readlines():
            u, v = line.strip().split("-")
            cave_id_u = add_new_cave(u)
            cave_id_v = add_new_cave(v)

            adj[cave_id_u].append(cave_id_v)
            adj[cave_id_v].append(cave_id_u)

    return caves, adj, name_to_id_map['start'], name_to_id_map['end']


def is_small_cave_visited(visited_small_cave, cave):
    return visited_small_cave & (1 << cave)


def set_bit(value, bit):
    return value | (1 << bit)


def get_number_of_all_paths_single_small_cave_twice(caves, adj, start_id, end_id):
    def dfs_visit(vertex, visited_small_caves, small_cave_visited_twice, curr_path):
        if vertex == end_id:
            all_paths.append(curr_path)
        else:
            for neighbor in adj[vertex]:
                if not is_small_cave_visited(visited_small_caves, caves[neighbor].id):
                    if caves[neighbor].is_small_cave:
                        if not small_cave_visited_twice:
                            dfs_visit(neighbor, visited_small_caves, True, curr_path + [caves[neighbor].name])

                        dfs_visit(neighbor, set_bit(visited_small_caves, caves[neighbor].id), small_cave_visited_twice,
                                  curr_path + [caves[neighbor].name])
                    else:
                        dfs_visit(neighbor, visited_small_caves, small_cave_visited_twice,
                                  curr_path + [caves[neighbor].name])

    all_paths = []

    dfs_visit(start_id, set_bit(0, start_id), False,
              [caves[start_id].name])
    return len(set([''.join(path) for path in all_paths]))


def translate_paths(paths, cave_ids):
    reversed_ids = {val: key for key, val in cave_ids.items()}
    return [[reversed_ids[i] for i in range(len(cave_ids)) if is_small_cave_visited(path, i)] for path in paths]


def translate_visited_set(visited, cave_ids):
    reversed_ids = {val: key for key, val in cave_ids.items()}
    return [reversed_ids[i] for i in range(len(cave_ids)) if is_small_cave_visited(visited, i)]


if __name__ == '__main__':
    t1 = perf_counter()
    caves, adj, start_id, end_id = read_file("input.txt")
    num = get_number_of_all_paths_single_small_cave_twice(caves, adj, start_id, end_id)
    t2 = perf_counter()
    print(f'answer={num} in {t2-t1:.3f}s')
