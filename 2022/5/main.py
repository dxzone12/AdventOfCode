# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

# extra input processing
groups = []

current_line = 0
while "[" in input_lines[current_line]:
    groups.append(input_lines[current_line])
    current_line += 1
current_line += 2

instructions = []
for instruction_line in input_lines[current_line:]:
    just_nums = [int(x) for x in instruction_line.replace("move ", "").replace("from ", "").replace("to ", "").split()]
    just_nums[1] -= 1
    just_nums[2] -= 1
    instructions.append(just_nums)

stacks = [[] for i in range(0, len(groups[0]), 4)]
stacks2 = [[] for i in range(0, len(groups[0]), 4)]
group_count = len(stacks)
for group_line in groups:
    for i in range(0, group_count):
        start_point = i * 4
        if (group_line[start_point] == "["):
            stacks[i].append(group_line[start_point+1])
            stacks2[i].append(group_line[start_point+1])
for stack in stacks:
    stack.reverse()
for stack in stacks2:
    stack.reverse()

# part 1
for instruction in instructions:
    for i in range(0, instruction[0]):
        stacks[instruction[2]].append(stacks[instruction[1]].pop())

print([stack.pop() for stack in stacks])



# Part 2
for instruction in instructions:
    popped_list = [stacks2[instruction[1]].pop() for i in range(0, instruction[0])]
    popped_list.reverse()
    stacks2[instruction[2]].extend(popped_list)

print([stack.pop() for stack in stacks2])