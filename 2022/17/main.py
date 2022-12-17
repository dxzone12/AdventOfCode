# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

instructions = input_lines[0]

# Part 1
TOTAL_BLOCKS_TO_PLACE = 2022
BLOCKS = [
    [(0, 0), (1, 0), (2, 0), (3, 0)], # Horizontal Line
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)], # Plus
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], # backwards L
    [(0, 0), (0, 1), (0, 2), (0, 3)], # Vertical line
    [(0, 0), (1, 0), (1, 1), (0, 1)], # Square
]

def isValidPosition(solid_blocks: set[tuple[int, int]], test_pos: tuple[int,int], block_type: int):
    # Check if any positions are in a solid block or out of bounds
    for part_offset in BLOCKS[block_type]:
        part_pos = (test_pos[0] + part_offset[0], test_pos[1] + part_offset[1])
        # Check if out of bounds
        if part_pos[1] < 0:
            return False
        if part_pos[0] < 0:
            return False
        if part_pos[0] >= 7:
            return False
        # Check if in any other block
        if part_pos in solid_blocks:
            return False
    return True

def getMovedPosition(move_instruction, current_pos: tuple[int,int]):
    if move_instruction == '<':
        return (current_pos[0] - 1, current_pos[1])
    elif move_instruction == '>':
        return (current_pos[0] + 1, current_pos[1])
    elif move_instruction == 'v':
        return (current_pos[0], current_pos[1] - 1)
    raise Exception("Should not be possible")

def getAllBlockPositions(block_type: int, origin_pos: tuple[int, int]):
    return [(origin_pos[0] + offset[0], origin_pos[1] + offset[1]) for offset in BLOCKS[block_type]]

fixed_points = set()
current_instruction = 0
current_block = 0
max_height = -1
for __ in range(0, TOTAL_BLOCKS_TO_PLACE):
    # spawn block
    block_pos = (2, max_height + 4) # plus 4 because we want a gap of 3 

    # move block till it stops
    while True:
        # Move instruction
        possible_moved_pos = getMovedPosition(instructions[current_instruction], block_pos)
        if isValidPosition(fixed_points, possible_moved_pos, current_block):
            block_pos = possible_moved_pos

        # Increment instruction since we just followed one
        current_instruction += 1
        current_instruction = current_instruction % len(instructions)

        # Move down
        possible_moved_pos = getMovedPosition('v', block_pos)
        if not isValidPosition(fixed_points, possible_moved_pos, current_block):
            break
        else:
            block_pos = possible_moved_pos

    # Record block
    positions_to_add = getAllBlockPositions(current_block, block_pos)
    fixed_points.update(positions_to_add)
    max_height = max(max_height, max([point[1] for point in positions_to_add]))


    # Increment block type
    current_block +=1
    current_block = current_block % len(BLOCKS)

print(f"After placing {TOTAL_BLOCKS_TO_PLACE} blocks the column reaches {max_height + 1} high")

# Part 2
