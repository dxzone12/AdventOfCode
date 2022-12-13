from itertools import zip_longest
from functools import cmp_to_key

# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

pairs = []
for i in range(0, len(input_lines), 3):
    left = eval(input_lines[i])
    right = eval(input_lines[i+1])
    pairs.append((left, right))

# Part 1
def getDifference(first, second):
    # if both int
    if isinstance(first, int) and isinstance(second, int):
        if first == second:
            return 0
        else:
            return -1 if first < second else 1

    # if mixed, then coerce to lists
    if not isinstance(first, list):
        first = [first]
    if not isinstance(second, list):
        second = [second]

    # if both list
    for left_item, right_item in zip_longest(first, second):
        # Check if either list has been exhausted
        if left_item == None:
            return -1
        if right_item == None:
            return 1

        difference = getDifference(left_item, right_item)
        if difference == 0:
            continue
        else:
            return difference
    return 0

def isInOrder(first, second):
    difference = getDifference(first, second)
    return difference < 0

sum_of_ordered_pair_indexes = 0
for itr, pair in enumerate(pairs):
    if isInOrder(pair[0], pair[1]):
        sum_of_ordered_pair_indexes += itr + 1

print(f"The sum of all the ordered pair indexes (1 based) is: {sum_of_ordered_pair_indexes}")

# Part 2
divider_packet_1 = [[2]]
divider_packet_2 = [[6]]

flattened_pairs = [item for pair in pairs for item in pair]
flattened_pairs.append(divider_packet_1)
flattened_pairs.append(divider_packet_2)

flattened_pairs.sort(key=cmp_to_key(getDifference))

divider_packet_1_index = flattened_pairs.index(divider_packet_1) + 1
divider_packet_2_index = flattened_pairs.index(divider_packet_2) + 1
print(f"The product of the two divider packet indexes (1 based) is: {divider_packet_1_index * divider_packet_2_index}")