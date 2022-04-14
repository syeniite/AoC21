from collections import namedtuple, Counter, deque
import numpy as np
from time import perf_counter
import concurrent.futures
Scanner = namedtuple("Scanner", "id beacons")
Match = namedtuple("Match", "scanner matched_with offset rotation_matrix num_matches")


def read_all_scanner_data(file_name):
    with open(file_name, "r") as f:
        return [Scanner(i, np.array([np.array(list(map(int, line.split(",")))) for line in sc.split("\n")[1:]]))
                for i, sc in enumerate(f.read().split("\n\n"))]


def check_matching_pair(reference_scanner: Scanner, scanner: Scanner, num_of_matches=12):
    for rotation_matrix in get_all_transformations_matrices_in_list():
        possible_offsets = Counter()

        for beacon_ref in reference_scanner.beacons:
            for beacon in scanner.beacons:
                possible_offsets[tuple(beacon_ref - rotation_matrix.dot(beacon).A1)] += 1

        most_common_offset = possible_offsets.most_common(1)[0]
        if most_common_offset[1] >= num_of_matches:
            return Match(reference_scanner, scanner, most_common_offset[0], rotation_matrix, most_common_offset[1])
    return None


def get_all_transformations_matrices_in_list():
    sin_theta, cos_theta = (0, 1, 0, -1), (1, 0, -1, 0)

    def get_x_rotation_matrix(theta_index):
        return np.matrix([[1, 0, 0], [0, cos_theta[theta_index], -sin_theta[theta_index]],
                          [0, sin_theta[theta_index], cos_theta[theta_index]]])

    def get_y_rotation_matrix(theta_index):
        return np.matrix([[cos_theta[theta_index], 0, sin_theta[theta_index]], [0, 1, 0],
                          [-sin_theta[theta_index], 0, cos_theta[theta_index]]])

    for first_x_rotation in range(4):
        for second_y_rotation in range(4):
            yield get_x_rotation_matrix(first_x_rotation).dot(get_y_rotation_matrix(second_y_rotation))

    for first_x_rotation in (1, 3):
        for second_y_rotation in range(4):
            yield get_y_rotation_matrix(1).dot(get_x_rotation_matrix(first_x_rotation))\
                .dot(get_y_rotation_matrix(second_y_rotation))


def get_matches(scanners, num_workers=8):
    matches = []
    queue = deque()
    matched_set = set()
    queue.append(scanners[0])
    matched_set.add(scanners[0].id)

    with concurrent.futures.ProcessPoolExecutor(num_workers) as executor:
        while queue:
            current_scanner = queue.popleft()
            futures = [executor.submit(check_matching_pair, current_scanner, potential_match)
                       for potential_match in scanners if potential_match.id not in matched_set]

            for future in concurrent.futures.as_completed(futures):
                if match := future.result():
                    matches.append(match)
                    queue.append(match.matched_with)
                    matched_set.add(match.matched_with.id)

    return matches


def get_offsets_and_rotation_to_first(scanners, matches):
    offsets_relative_to_first_scanner = {scanners[0].id: np.array([0] * len(scanners[0].beacons[0]))}
    rotation_to_first = {scanners[0].id: np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])}

    for match in matches:
        previous = match.scanner
        new = match.matched_with

        rotation_to_first[new.id] = rotation_to_first[previous.id].dot(match.rotation_matrix)
        transformed_offset = rotation_to_first[previous.id].dot(match.offset).A1
        offsets_relative_to_first_scanner[new.id] = offsets_relative_to_first_scanner[previous.id] + transformed_offset

    return offsets_relative_to_first_scanner, rotation_to_first


def get_unique_beacons(offsets_relative_to_first_scanner, rotation_to_first, scanners):
    return len(set(tuple(rotation_to_first[s.id].dot(beacon).A1 + offsets_relative_to_first_scanner[s.id]) for s
                   in scanners for beacon in s.beacons))


def get_max_manhattan_distance(offsets_relative_to_first_scanner):
    def manhattan(p, q):
        return sum(abs(u-v) for u, v in zip(p, q))

    scanner_locations = list(offsets_relative_to_first_scanner.values())

    return max(manhattan(scanner_locations[i], scanner_locations[j])
               for i in range(len(scanner_locations)-1) for j in range(i+1, len(scanner_locations)))


if __name__ == "__main__":
    t1 = perf_counter()
    scs = read_all_scanner_data("input.txt")
    all_matches = get_matches(scs)
    offsets, rotations = get_offsets_and_rotation_to_first(scs, all_matches)
    num_unique_beacons = get_unique_beacons(offsets, rotations, scs)
    max_manhattan_distance = get_max_manhattan_distance(offsets)
    print(f'time elapsed {perf_counter()-t1:.2f}s')
    print([(match.scanner.id, match.matched_with.id) for match in all_matches])
    print(num_unique_beacons)
    print(max_manhattan_distance)
