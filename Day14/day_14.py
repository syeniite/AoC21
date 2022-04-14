from linked_list import LinkedList, Node
from collections import Counter
from time import perf_counter


num_of_occurrences = dict()


def count_occurrence(element):
    if element not in num_of_occurrences:
        num_of_occurrences[element] = 1
    else:
        num_of_occurrences[element] += 1


def polymerize_linked_list(template, substitution_table, steps):
    result = LinkedList()

    for t in template:
        result.add_last(Node(t))

    for step in range(steps):
        current = result.head

        while current.next:
            nxt = current.next
            result.add_right_to(current, Node(substitution_table[f'{current.key}{nxt.key}']))
            current = nxt

    for x in result:
        count_occurrence(x)


def polymerize_bottom_up(template, substitution_table, steps):
    alphabet = get_all_unique_letters(substitution_table)

    occurrences = [[Counter() for _ in range(len(alphabet))] for _ in range(len(alphabet))]

    # base case: populate occurrences of step 0 -> occ(AB) = {A: 1, B: 1}
    # note that there might be illegal substitutions - instructions aren't clear on that
    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            sub = f'{alphabet[i]}{alphabet[j]}'

            if sub in substitution_table:
                occurrences[i][j] = Counter([alphabet[i], alphabet[j]])

    # if AB->C then occ(AB, i) = occ(AC, i-1) + occ(CB, i-1) - {C}. -C because we count C twice
    # an order in which we can update the occ table can not be trivially determined, so we are lazy and just create a
    # new updated table for each step
    for step in range(steps):
        occurrences = update_occurrences(occurrences, substitution_table, alphabet)

    # get num of occurrences for template:
    # go from left to right and add all occurrences for template[i]template[i+1]
    # example: template = ABC -> occ(AB) + occ(BC) - {B} since B was counted twice
    total_occurrences_template = Counter()

    for i in range(len(template)-1):
        total_occurrences_template += \
            occurrences[get_index_of_sub(template[i], alphabet)][get_index_of_sub(template[i+1], alphabet)]

    # subtract all that have been counted twice
    for i in range(1, len(template) - 1):
        total_occurrences_template -= Counter(template[i])

    ordered_most_common_occurrences = total_occurrences_template.most_common()

    return ordered_most_common_occurrences[0][1] - ordered_most_common_occurrences[-1][1]


def update_occurrences(occurrences, sub_table, alphabet):
    updated_occs = [[{} for _ in range(len(occurrences[0]))] for _ in range(len(occurrences))]

    for i in range(len(updated_occs)):
        for j in range(len(updated_occs[0])):
            sub_index = get_index_of_sub(sub_table[f'{alphabet[i]}{alphabet[j]}'], alphabet)

            updated_occs[i][j] = (occurrences[i][sub_index] + occurrences[sub_index][j]) - Counter(alphabet[sub_index])

    return updated_occs


def get_index_of_sub(_sub, alphabet):
    high = len(alphabet)
    low = 0

    while high >= low:
        mid = (high + low) // 2

        if alphabet[mid] == _sub:
            return mid
        elif alphabet[mid] > _sub:
            high = mid - 1
        else:
            low = mid + 1

    raise ValueError(f"Couldn't find {_sub} in {alphabet}")


def get_all_unique_letters(substitution_table):
    unique_letter_set = set()

    for key in substitution_table.keys():
        unique_letter_set.add(key[0])
        unique_letter_set.add(key[1])

    return sorted(list(unique_letter_set))


def read_file(file_name):
    with open(file_name, "r") as f:
        template = f.readline().strip()
        table = dict()
        f.readline()

        for line in f.readlines():
            s, t = line.strip().split("->")
            table[s.strip()] = t.strip()

        return template, table


if __name__ == '__main__':
    start_template, sub_table = read_file("input.txt")
    t1 = perf_counter()
    answer = polymerize_bottom_up(start_template, sub_table, 40)
    t2 = perf_counter()
    print(f'{answer=} in {t2-t1:.5f}s')
    # polymerize_linked_list(*read_file("input.txt"), steps=20)
    # sorted_occurrences = sorted(num_of_occurrences.values())
    # print(sorted_occurrences[-1] - sorted_occurrences[0])
