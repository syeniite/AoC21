from functools import reduce


def parse_input(file_name: str) -> list:
    def translate_cmd_to_coordinate_value_pair(line) -> tuple:
        match line.split():
            case ['forward', value]:
                return 0, int(value)
            case ['down', value]:
                return 1, int(value)
            case ['up', value]:
                return 1, -int(value)

    with open(file_name, "r") as f:
        return [translate_cmd_to_coordinate_value_pair(line) for line in f.readlines()]


def find_destination(cmds: list, origin=(0, 0, 0)) -> tuple:
    return reduce(with_aim, cmds, origin)


def no_aim(curr_pos: tuple, cmd: tuple) -> tuple:
    return curr_pos[0] + (1-cmd[0])*cmd[1], curr_pos[1] + cmd[0]*cmd[1]


def with_aim(curr_pos: tuple, cmd: tuple) -> tuple:
    return curr_pos[0] + (1-cmd[0])*cmd[1], curr_pos[1] + (1-cmd[0])*cmd[1]*curr_pos[2], curr_pos[2] + cmd[0]*cmd[1]


if __name__ == '__main__':
    commands = parse_input("input.txt")
    destination = find_destination(commands)
    print(destination[0]*destination[1])
