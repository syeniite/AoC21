from __future__ import annotations
import heapq
from time import perf_counter


cost_per_move = {"A": 1, "B": 10, "C": 100, "D": 1000}

END_STATE = "AABBCCDD"
NUM_ROOMS = 4
HALL_LENGTH = NUM_ROOMS*2 - 1 + 4
ROOM_DEPTH = 2  # TODO: adjust code to variable depth


class Board:
    visited: bool = False
    """
        #############
        #89.........#
        ###1#3#5#7###
          #0#2#4#6#
          #########
    """
    state: str

    def __init__(self, state, energy_level: int = 0):
        self.state = state
        self.energy_level = energy_level

    def __lt__(self, other: Board):
        return self.energy_level < other.energy_level

    def __repr__(self):
        return f'{"":#<{HALL_LENGTH+2}}\n#{self.state[2*NUM_ROOMS:]}#\n' \
               f'###{"#".join(self.state[i] for i in range(1, 2*NUM_ROOMS, 2))}###\n' \
               f'  #{"#".join(self.state[i] for i in range(0, 2*NUM_ROOMS - 1, 2))}#\n' \
               f'  #{"":#<{2*NUM_ROOMS}\t{self.energy_level}}'

    def is_finished(self) -> bool:
        return self.state[:2*NUM_ROOMS] == END_STATE

    def is_free_space(self, pos: int) -> bool:
        return self.state[pos] == "."

    def get_all_valid_next_boards(self) -> list[Board]:
        return self._get_next_boards_room_to_hall() + self._get_next_boards_hall_to_room()

    def _get_next_boards_room_to_hall(self) -> list[Board]:
        boards = []

        for room_number in range(NUM_ROOMS):
            for depth in range(ROOM_DEPTH):
                pos_to_move = 2*(room_number+1) - depth - 1 # TODO: might be wrong
                if not self.is_free_space(pos_to_move):
                    for pos in self._get_valid_positions_outside_room(room_number):
                        boards.append(Board(self._get_updated_state(pos_to_move, pos),
                                            self.energy_level + get_cost_of_movement(self.state[pos_to_move],
                                                                                     pos_to_move, pos)))
                    break

        return boards

    def _get_valid_positions_outside_room(self, room: int) -> list[int]:
        positions = []

        hall_index_left, hall_index_right = ROOM_DEPTH*NUM_ROOMS + 2 - 1 + 2*room, 2*NUM_ROOMS + 2 + 1 + 2*room

        while 2*NUM_ROOMS < hall_index_left and self.is_free_space(hall_index_left+1) and \
                self.is_free_space(hall_index_left):
            positions.append(hall_index_left)
            hall_index_left -= 2

        if hall_index_left == 2*NUM_ROOMS - 1:
            positions.append(2*NUM_ROOMS)

        while hall_index_right < len(self.state) and self.is_free_space(hall_index_left-1) and \
                self.is_free_space(hall_index_right):
            positions.append(hall_index_right)
            hall_index_right += 2

        if hall_index_right == len(self.state):
            positions.append(len(self.state)-1)

        return positions

    def _get_next_boards_hall_to_room(self) -> list[Board]:
        boards = []

        for hall_pos in range(ROOM_DEPTH * NUM_ROOMS, ROOM_DEPTH * NUM_ROOMS + HALL_LENGTH):
            if self.is_free_space(hall_pos):
                continue

            dest_pos = self.get_destination_pos_or_negative(self.state[hall_pos], hall_pos)
            if dest_pos >= 0:
                boards.append(Board(self._get_updated_state(hall_pos, dest_pos),
                                    get_cost_of_movement(self.state[hall_pos], hall_pos, dest_pos)))
        return boards

    def _get_updated_state(self, from_move: int, to_move) -> str:
        new_state = self.state[:from_move] + "." + self.state[from_move+1:]
        return new_state[:to_move] + self.state[from_move] + new_state[to_move+1:]

    def get_destination_pos_or_negative(self, amphipod: str, pos: int) -> int:
        dest_room = get_destination_room_number(amphipod)
        pos_in_front_of_room = ROOM_DEPTH*NUM_ROOMS + 2 + 2*dest_room
        current_pos = pos
        direction = 1 if pos_in_front_of_room >= current_pos else -1

        while current_pos != ROOM_DEPTH*NUM_ROOMS + 2 + 2*dest_room:
            current_pos += direction
            if not self.is_free_space(current_pos):
                return -1

        for room_pos in range(ROOM_DEPTH * (dest_room+1) - 1, ROOM_DEPTH*dest_room, -1):
            if self.is_free_space(room_pos):
                return room_pos

            if self.state[room_pos] != amphipod:
                return -1

        return -1


def get_destination_room_number(amphipod: str) -> int:
    return ord(amphipod) - 65


def get_cost_of_movement(amphipod: str, from_move, to_move) -> int:
    return ...


def find_optimal_energy_cost(initial_state) -> int:
    start_board = Board(initial_state)

    all_boards: dict[str, Board] = {start_board.state: start_board}

    queue: list[Board] = []
    heapq.heappush(queue, start_board)

    while queue:
        current_best_board = heapq.heappop(queue)

        print(current_best_board)

        if len(all_boards) >= 100:
            break

        if current_best_board.is_finished():
            return current_best_board.energy_level

        if current_best_board.visited:
            continue

        current_best_board.visited = True

        for next_board in current_best_board.get_all_valid_next_boards():
            if next_board.state in all_boards:
                if (board := all_boards[next_board.state]).energy_level > next_board.energy_level:
                    board.energy_level = next_board.energy_level
                    heapq.heappush(queue, board)
            else:
                all_boards[next_board.state] = next_board
                heapq.heappush(queue, next_board)
    return -1


def get_example_board() -> str:
    return "ABDCCBAD..........."


def get_input_board() -> str:
    return "CCDBAABD..........."


if __name__ == "__main__":
    print(find_optimal_energy_cost(get_example_board()))
