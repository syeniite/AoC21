from dataclasses import dataclass
from functools import reduce


@dataclass
class Cell:
    value: int
    marked: bool

    def get_val_if_not_marked(self):
        return (not self.marked) * self.value


def parse_file(file_name):
    with open(file_name, "r") as f:
        number_pool = [int(n) for n in f.readline().split(",")]
        boards = [[[Cell(int(n), False) for n in row.strip().split()] for row in board.strip().split("\n")]
                  for board in f.read().split("\n\n")]
        return number_pool, boards


def check_row_or_col(row_or_col):
    return all(cell.marked for cell in row_or_col)


def is_bingo(board):
    return any(check_row_or_col(row) for row in board) or \
           any(check_row_or_col([board[row][col] for row in range(len(board))]) for col in range(len(board[0])))


def mark_all_numbers(board, num):
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col].value == num:
                board[row][col].marked = True


def get_first_winner_board_and_last_number(pool, boards):
    for number in pool:
        for board in boards:
            mark_all_numbers(board, number)

            if is_bingo(board):
                return board, number


def get_last_winner_board_and_last_number(pool, boards):
    board_status = [False] * len(boards)

    for number in pool:
        last_board_won = -1
        for i, board in enumerate(boards):
            if not board_status[i]:
                mark_all_numbers(board, number)

                if is_bingo(board):
                    board_status[i] = True
                    last_board_won = i

        if all(board_status):
            return boards[last_board_won], number


def calc_answer(board, number):
    return number * sum(sum(cell.get_val_if_not_marked() for cell in row) for row in board)


if __name__ == '__main__':
    # print(calc_answer(*get_first_winner_board_and_last_number(*parse_file("input.txt"))))
    print(calc_answer(*get_last_winner_board_and_last_number(*parse_file("input.txt"))))
