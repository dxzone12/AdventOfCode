# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

grid_lines = input_lines[:-2]
instruction_line = input_lines[-1]

# Part 1
EMPTY = ' '
FREE = '.'
WALL = '#'

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

RIGHT_INSTRUCTION = "R"
LEFT_INSTRUCTION = "L"

# Parse out a grid
line_lengths = [len(line) for line in grid_lines]
max_line = max(line_lengths)
grid = [[char for char in line] for line in grid_lines]
for line in grid:
    if len(line) < max_line:
        while len(line) < max_line:
            line.append(EMPTY)

# Parse out the instructions
instructions = [int(instruction) if instruction.isdigit() else instruction for instruction in instruction_line.replace("R", ":R:"). replace("L", ":L:").split(":")]

# Follow instructions
def getNewFacing(current_f_p, instruction):
    facing = current_f_p[1]
    if instruction == RIGHT_INSTRUCTION:
        return (current_f_p[0], (facing + 1) % 4)
    elif instruction == LEFT_INSTRUCTION:
        return (current_f_p[0], (facing - 1) % 4)

    raise Exception("SHOULD NEVER HAPPEN")

def applyMoveWithBounds(f_p, x_y_diff, max_x, max_y):
    next_pos = (f_p[0][0] + x_y_diff[0], f_p[0][1] + x_y_diff[1])
    if next_pos[0] < 0:
        next_pos = (max_x - 1, next_pos[1])
    if next_pos[0] >= max_x:
        next_pos = (0, next_pos[1])
    if next_pos[1] < 0:
        next_pos = (next_pos[0], max_y - 1)
    if next_pos[1] >= max_y:
        next_pos = (next_pos[0], 0)
    return (next_pos, f_p[1])

def getNextInDirWithWrap(f_p, grid):
    x_y_diff_for_dir = None
    if f_p[1] == RIGHT:
        x_y_diff_for_dir = (1, 0)
    elif f_p[1] == DOWN:
        x_y_diff_for_dir = (0, 1)
    elif f_p[1] == LEFT:
        x_y_diff_for_dir = (-1, 0)
    elif f_p[1] == UP:
        x_y_diff_for_dir = (0, -1)
    
    next_f_p = applyMoveWithBounds(f_p, x_y_diff_for_dir, len(grid[0]), len(grid))
    while grid[next_f_p[0][1]][next_f_p[0][0]] == EMPTY:
        next_f_p = applyMoveWithBounds(next_f_p, x_y_diff_for_dir, len(grid[0]), len(grid))
    
    return next_f_p

def moveInDirection(current_f_p, distance, grid):
    new_f_p = current_f_p
    for __ in range(0, distance):
        pos_f_p = getNextInDirWithWrap(new_f_p, grid)
        if grid[pos_f_p[0][1]][pos_f_p[0][0]] == WALL:
            break
        new_f_p = pos_f_p
    return new_f_p

current_pos_face = ((grid[0].index(FREE), 0), RIGHT)
for instruction in instructions:
    if isinstance(instruction, str):
        # Direction change
        current_pos_face = getNewFacing(current_pos_face, instruction)
    else:
        # Movement on current heading
        current_pos_face = moveInDirection(current_pos_face, instruction, grid)

print(f"The final password is {(1000 * (current_pos_face[0][1] + 1)) + (4 * (current_pos_face[0][0] + 1)) + current_pos_face[1]}")

# Part 2
