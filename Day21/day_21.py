from dataclasses import dataclass
from functools import cache


@dataclass
class Player:
    id: int
    current_position: int
    score: int


def deterministic_dice():
    i = 1
    while True:
        yield i
        i += 1
        if i > 100:
            i = 1


def play_game(start_p1, start_p2, winning_score=1000):
    def turn(player: Player):
        player.current_position = ((player.current_position-1 + sum(next(dice) for _ in range(3))) % 10)+1
        player.score += player.current_position

        if player.score >= winning_score:
            return True
        return False

    players = [Player(0, start_p1, 0), Player(1, start_p2, 0)]
    dice = deterministic_dice()
    dice_rolled = 0
    current_player = players[0]

    while not turn(current_player):
        dice_rolled += 3
        current_player = players[1-current_player.id]

    return [p.score for p in players], dice_rolled+3


@cache
def play_game_multiverse(position_1, position_2, score_1, score_2, winning_score=21):
    # there can only be 10 different positions for each player and 21 different scores for each player
    # use cache to memoize game states -> no dataclasses to make things easier
    # assume it is player 1's turn
    def update_position(first, second, third):
        return ((position_1-1 + first + second + third) % 10)+1

    def get_possible_dice_values():
        return 1, 2, 3

    # winning game state for either current player 1 or current player 2
    # immediately report a win
    if score_1 >= winning_score:
        return 1, 0
    if score_2 >= winning_score:
        return 0, 1

    total_wins_1, total_wins_2 = 0, 0

    for first_roll in get_possible_dice_values():
        for second_roll in get_possible_dice_values():
            for third_roll in get_possible_dice_values():
                new_position_1 = update_position(first_roll, second_roll, third_roll)

                # use memoized(cached) results to avoid redundant recursive calls
                wins_2, wins_1 = play_game_multiverse(position_2, new_position_1, score_2, score_1 + new_position_1)
                total_wins_1 += wins_1
                total_wins_2 += wins_2

    return total_wins_1, total_wins_2


if __name__ == '__main__':
    # player_scores, times_dice_was_rolled = play_game(9, 6)
    # print(min(player_scores)*times_dice_was_rolled)
    print(max(play_game_multiverse(9, 6, 0, 0)))
