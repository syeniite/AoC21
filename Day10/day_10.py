corresponding_bracket = {"(": ")", ")": "(", "[": "]", "]": "[", "{": "}", "}": "{", "<": ">", ">": "<"}


def scoring_func(bracket):
    match bracket:
        case ")":
            return 3
        case "]":
            return 57
        case "}":
            return 1197
        case ">":
            return 25137
        case _:
            return 0


def scoring_func_complete(bracket):
    match bracket:
        case ")":
            return 1
        case "]":
            return 2
        case "}":
            return 3
        case ">":
            return 4


def read_file(file_name):
    with open(file_name, "r") as f:
        return [[b.strip() for b in line.strip()] for line in f.readlines()]


def check_brackets(brackets):
    stack = []

    for possible_bracket in brackets:
        if possible_bracket in "([{<":
            stack.append(possible_bracket)
        else:
            last_opened = stack[-1]

            if corresponding_bracket[last_opened] == possible_bracket:
                stack.pop()
            else:
                return possible_bracket, stack
    return "", stack


def get_total_error_score(brackets, error_func=scoring_func):
    return sum(error_func(check_brackets(line)[0]) for line in brackets)


def get_total_completion_score(brackets, completion_scoring_func=scoring_func_complete):
    scores = []

    for line in brackets:
        score_of_line = 0
        error_bracket, remaining = check_brackets(line)

        if not error_bracket:
            while remaining:
                score_of_line *= 5
                score_of_line += completion_scoring_func(corresponding_bracket[remaining.pop()])

            scores.append(score_of_line)

    return scores


if __name__ == '__main__':
    subsystem = read_file("input.txt")
    # print(get_total_error_score(subsystem))
    sorted_scores = sorted(get_total_completion_score(subsystem))
    print(sorted_scores[len(sorted_scores)//2])

