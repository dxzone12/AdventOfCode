# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

# part 1
def getPriority(item):
    ascii_val = ord(item)
    return ascii_val - 96 if ascii_val >= 97 else ascii_val - 38

total_priority = 0
for line in input_lines:
    half_way = int(len(line)/2)
    pocket_one = set()
    pocket_two = set()
    for i in range(half_way):
        item_in_pocket_one = line[i]
        item_in_pocket_two = line[i + half_way]
        # Check if item is in the other pocket already and break out
        if item_in_pocket_one in pocket_two:
            total_priority += getPriority(item_in_pocket_one)
            break
        pocket_one.add(item_in_pocket_one)
        if item_in_pocket_two in pocket_one:
            total_priority += getPriority(item_in_pocket_two)
            break
        pocket_two.add(item_in_pocket_two)

print(f"Total priority: {total_priority}")

# part 2
total_priority2 = 0
for start_line_for_group in range(0, len(input_lines), 3):
    elves_with_item = dict()
    for elf_in_group in range(3):
        line_num = start_line_for_group + elf_in_group
        line = input_lines[line_num]
        for letter in line:
            if letter not in elves_with_item:
                elves_with_item[letter] = set()
            elves_with_item[letter].add(elf_in_group)
    identifier_item = next(x for x in elves_with_item if len(elves_with_item[x]) == 3)
    total_priority2 += getPriority(identifier_item)

print(f"Total priority of groups: {total_priority2}")