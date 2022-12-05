from __future__ import annotations
from typing import Iterator
from time import perf_counter
import heapq

cost_per_move = {"A": 1, "B": 10, "C": 100, "D": 1000}

NUM_ROOMS = 4
HALL_LENGTH = NUM_ROOMS * 2 - 1 + 4
ROOM_DEPTH = 2


class Board:
    visited: bool = False
    """
        a board is encoded by a 1D string ordered like this:
        #############
        #89.........#
        ###1#3#5#7###
          #0#2#4#6#
          #########
    """
    state: str
    pred: Board | None
    heuristic: int

    def __init__(self, state, energy_level: int = 0):
        self.state = state
        self.energy_level = energy_level
        self.pred = None
        self.heuristic = 0 # self._get_heuristic()

    def __str__(self):
        def _get_room_level(l):
            return f'  #{"#".join(self.state[i] for i in range(l, ROOM_DEPTH * NUM_ROOMS, ROOM_DEPTH))}#\n'

        return f'{"":#<{HALL_LENGTH + 2}}\n#{self.state[ROOM_DEPTH * NUM_ROOMS:]}#\n' \
               f'###{"#".join(self.state[i] for i in range(ROOM_DEPTH - 1, ROOM_DEPTH * NUM_ROOMS, ROOM_DEPTH))}###\n' \
               f'{"".join(_get_room_level(level) for level in range(ROOM_DEPTH - 2, -1, -1))}' \
               f'  #{"":#<{2 * NUM_ROOMS}}\t{self.energy_level}\t str: {self.state}'

    def __repr__(self):
        return f'({self.state}, {self.energy_level})'

    def get_cost(self):
        return self.energy_level + self.heuristic

    def is_finished(self) -> bool:
        return self.state[:ROOM_DEPTH * NUM_ROOMS] == "A"*ROOM_DEPTH + "B"*ROOM_DEPTH + "C"*ROOM_DEPTH + "D"*ROOM_DEPTH

    def is_free_space(self, pos: int) -> bool:
        return self.state[pos] == "."

    def get_all_valid_next_boards(self) -> Iterator[Board]:
        # return self._get_next_boards_room_to_hall() + self._get_next_boards_hall_to_room()
        for hall_pos in range(ROOM_DEPTH * NUM_ROOMS, ROOM_DEPTH * NUM_ROOMS + HALL_LENGTH):
            if self.is_free_space(hall_pos):
                continue

            if (dest_pos := self._get_destination_pos_or_negative(self.state[hall_pos], hall_pos)) >= 0:
                yield Board(self._get_updated_board(hall_pos, dest_pos),
                            self.energy_level + get_cost_of_movement(self.state[hall_pos], hall_pos, dest_pos))

        for room_number in range(NUM_ROOMS):
            if not self.contains_wrong_pod(room_number):
                continue
            for depth in range(ROOM_DEPTH):
                room_pos = ROOM_DEPTH * (room_number + 1) - depth - 1

                if not self.is_free_space(room_pos):
                    pos_in_hall = self.get_position_in_front_current_room(room_number)
                    if (dest_pos := self._get_destination_pos_or_negative(self.state[room_pos], pos_in_hall)) >= 0:
                        yield Board(self._get_updated_board(room_pos, dest_pos),
                                    self.energy_level + get_cost_of_movement(self.state[room_pos], room_pos, dest_pos))
                        break

                    for hall_pos in self._get_valid_positions_outside_room(room_number):
                        yield Board(self._get_updated_board(room_pos, hall_pos),
                                    self.energy_level + get_cost_of_movement(self.state[room_pos], hall_pos, room_pos))
                    break

    def contains_wrong_pod(self, room_num) -> bool:
        expected_amphipod = get_amphipod_from_room_number(room_num)
        return any(self.state[i] != expected_amphipod and self.state[i] != "."
                   for i in range(ROOM_DEPTH * room_num, ROOM_DEPTH * (room_num + 1)))

    def _get_valid_positions_outside_room(self, room: int) -> list[int]:
        positions = []

        hall_index_left, hall_index_right = ROOM_DEPTH * NUM_ROOMS + 2 - 1 + 2 * room, ROOM_DEPTH * NUM_ROOMS + 2 + 1 + 2 * room

        while ROOM_DEPTH * NUM_ROOMS < hall_index_left and self.is_free_space(hall_index_left + 1) and \
                self.is_free_space(hall_index_left):
            positions.append(hall_index_left)
            hall_index_left -= 2

        if hall_index_left == ROOM_DEPTH * NUM_ROOMS - 1 and self.is_free_space(ROOM_DEPTH * NUM_ROOMS):
            positions.append(ROOM_DEPTH * NUM_ROOMS)

        while hall_index_right < len(self.state) and self.is_free_space(hall_index_right - 1) and \
                self.is_free_space(hall_index_right):
            positions.append(hall_index_right)
            hall_index_right += 2

        if hall_index_right == len(self.state) and self.is_free_space(hall_index_right-1):
            positions.append(len(self.state) - 1)

        return positions

    def _get_updated_board(self, from_move: int, to_move) -> str:
        new_state = self.state[:from_move] + "." + self.state[from_move + 1:]
        return new_state[:to_move] + self.state[from_move] + new_state[to_move + 1:]

    def _get_destination_pos_or_negative(self, amphipod: str, pos: int) -> int:
        dest_room = get_destination_room_number(amphipod)
        pos_in_front_of_room = ROOM_DEPTH * NUM_ROOMS + 2 + 2 * dest_room
        current_pos = pos
        direction = 1 if pos_in_front_of_room >= current_pos else -1

        while current_pos != ROOM_DEPTH * NUM_ROOMS + 2 + 2 * dest_room:
            current_pos += direction
            if not self.is_free_space(current_pos):
                return -1

        expected_pod = get_amphipod_from_room_number(dest_room)
        for room_pos in range(ROOM_DEPTH * dest_room, ROOM_DEPTH * (dest_room + 1)):
            if self.is_free_space(room_pos):
                return room_pos
            elif self.state[room_pos] != expected_pod:
                return -1

        return -1

    def _get_heuristic(self) -> int:
        minimum_energy_required = 0
        for i in range(ROOM_DEPTH * NUM_ROOMS, len(self.state)):
            if self.is_free_space(i):
                continue
            pos_in_front_of_room = self.get_position_in_front_of_dest_room(self.state[i])
            minimum_energy_required += (abs(i - pos_in_front_of_room) + 1) * cost_per_move[self.state[i]]

        for i in range(ROOM_DEPTH * NUM_ROOMS):
            if self.is_free_space(i):
                continue
            current_room_number = i // ROOM_DEPTH
            if current_room_number != get_destination_room_number(self.state[i]):
                pos_in_front_of_own_room = self.get_position_in_front_current_room(current_room_number)
                pos_in_front_of_dest_room = self.get_position_in_front_of_dest_room(self.state[i])
                minimum_energy_required += \
                    (abs(pos_in_front_of_own_room - pos_in_front_of_dest_room) +
                     (current_room_number + 1) * ROOM_DEPTH - i + 1) * cost_per_move[self.state[i]]

        return minimum_energy_required

    @staticmethod
    def get_position_in_front_of_dest_room(amphipod: str) -> int:
        return ROOM_DEPTH * NUM_ROOMS + 2 + 2 * get_destination_room_number(amphipod)

    @staticmethod
    def get_position_in_front_current_room(current_room_number: int) -> int:
        return ROOM_DEPTH * NUM_ROOMS + 2 + 2 * current_room_number


def get_destination_room_number(amphipod: str) -> int:
    return ord(amphipod) - 65


def get_amphipod_from_room_number(num: int) -> str:
    return chr(num + 65)


def get_cost_of_movement(amphipod: str, from_pos, to_pos) -> int:
    # all movements are room -> hall or hall -> room or room -> room
    def steps_room_to_hall(pos):
        return (pos//ROOM_DEPTH + 1)*ROOM_DEPTH - pos
    if from_pos < ROOM_DEPTH * NUM_ROOMS and to_pos < ROOM_DEPTH * NUM_ROOMS:
        hall_pos_from_room = Board.get_position_in_front_current_room(from_pos // ROOM_DEPTH)
        hall_pos_to_room = Board.get_position_in_front_current_room(to_pos // ROOM_DEPTH)

        return (abs(hall_pos_to_room - hall_pos_from_room) + steps_room_to_hall(from_pos) + steps_room_to_hall(to_pos))*\
            cost_per_move[amphipod]
    else:
        hall_pos, room_pos = max(from_pos, to_pos), min(from_pos, to_pos)
        pos_in_front_of_room = Board.get_position_in_front_current_room(room_pos // ROOM_DEPTH)
        return (abs(hall_pos - pos_in_front_of_room) + steps_room_to_hall(room_pos)) * cost_per_move[amphipod]


def find_optimal_energy_cost(initial_state) -> int:
    start_board = Board(initial_state)

    all_boards: dict[str, Board] = {start_board.state: start_board}

    queue: list[tuple[int, str]] = []
    heapq.heappush(queue, (start_board.energy_level, start_board.state))

    while queue:
        cost, state = heapq.heappop(queue)
        current_best_board = all_boards[state]

        if current_best_board.is_finished():
            print(f"total boards considered: {len(all_boards)}")
            return current_best_board.energy_level

        if current_best_board.visited:
            continue
        current_best_board.visited = True

        for next_board in current_best_board.get_all_valid_next_boards():
            if next_board.state in all_boards:
                if (board := all_boards[next_board.state]).energy_level > next_board.energy_level:
                    board.energy_level = next_board.energy_level
                    next_board.pred = current_best_board
                    heapq.heappush(queue, (board.get_cost(), board.state))
            else:
                all_boards[next_board.state] = next_board
                next_board.pred = current_best_board
                heapq.heappush(queue, (next_board.get_cost(), next_board.state))

    print(f"total boards considered: {len(all_boards)}")
    return -1


def get_example_board() -> str:
    global ROOM_DEPTH
    ROOM_DEPTH = 2
    return "ABDCCBAD..........."


def get_example_board2() -> str:
    global ROOM_DEPTH
    ROOM_DEPTH = 4
    return "ADDBDBCCCABBACAD..........."


def get_input_board() -> str:
    global ROOM_DEPTH
    ROOM_DEPTH = 2
    return "CCDBAABD..........."


def get_input_board2() -> str:
    global ROOM_DEPTH
    ROOM_DEPTH = 4
    return "CDDCDBCBAABABCAD..........."


if __name__ == "__main__":
    t1 = perf_counter()
    print(find_optimal_energy_cost(get_input_board2()))
    print(f'total time: {perf_counter() - t1:.3f}s')

