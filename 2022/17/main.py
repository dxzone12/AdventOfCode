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
def topSpaceSignature(placed: set[tuple[int,int]], max_height: int) -> list[tuple[int,int]]:
    """This does a bfs from the cell above the top known position
    to geenrate a list of all the cells that are air and not solid blocks at
    the top of the stack. This gives us a key that is unique based on the surface
    blocks can land on to see if we repeat one."""
    
    start_y = max_height + 1
    found_blocks = set()
    found_air = [(0, start_y)]
    visited = set()
    while len(found_air) > 0:
        next_node = found_air.pop(0)
        if next_node in visited:
            continue
        visited.add(next_node)
        # Check left
        new_x = next_node[0] - 1
        if new_x >= 0:
            pos_node = (new_x, next_node[1])
            if pos_node in placed:
                found_blocks.add((pos_node[0] - 0, start_y - pos_node[1]))
            elif pos_node not in visited:
                found_air.append(pos_node)
        # Check down
        new_y = next_node[1] - 1
        if new_y >= 0:
            pos_node = (next_node[0], new_y)
            if pos_node in placed:
                found_blocks.add((pos_node[0] - 0, start_y - pos_node[1]))
            elif pos_node not in visited:
                found_air.append(pos_node)
        # Check right
        new_x = next_node[0] + 1
        if new_x < 7:
            pos_node = (new_x, next_node[1])
            if pos_node in placed:
                found_blocks.add((pos_node[0] - 0, start_y - pos_node[1]))
            elif pos_node not in visited:
                found_air.append(pos_node)
        # Check top
        new_y = next_node[1] + 1
        if new_y <= start_y:
            pos_node = (next_node[0], new_y)
            if pos_node in placed:
                found_blocks.add((pos_node[0] - 0, start_y - pos_node[1]))
            elif pos_node not in visited:
                found_air.append(pos_node)
    node_list = list(found_blocks)
    node_list.sort()
    return node_list

fixed_points = set()
current_instruction = 0
current_block = 0
max_height = -1
unique_tops = {}
best_key = None
TOTAL_BLOCKS_TO_PLACE_PART2 = 1000000000000
for i in range(0, TOTAL_BLOCKS_TO_PLACE_PART2):
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

    top_points = topSpaceSignature(fixed_points, max_height)
    key = str(top_points) + f"{current_block}:{current_instruction}"
    if key in unique_tops:
        unique_tops[key].append((i, max_height))
        if len(unique_tops[key]) > 1:
            best_key = key
            break
    else:
        unique_tops[key] = [(i, max_height)]

# Use the repeat to determine the height as close as we can to the number of blocks needed
repeat_locations = unique_tops[best_key]
repeat_locations.sort()

remaining_blocks_from_first_key = TOTAL_BLOCKS_TO_PLACE_PART2 - repeat_locations[0][0] - 1
blocks_till_next_repeat = repeat_locations[1][0] - repeat_locations[0][0]
height_difference_from_repeat = repeat_locations[1][1] - repeat_locations[0][1]

full_repeats_that_fit = remaining_blocks_from_first_key // blocks_till_next_repeat
max_height_after_repeats_that_fit = repeat_locations[0][1] + (full_repeats_that_fit * height_difference_from_repeat)
difference_left_to_place = remaining_blocks_from_first_key % blocks_till_next_repeat

# Simulate the remaining few blocks to get the last little bit of height
height_before_last_blocks = max_height
for __ in range(0, difference_left_to_place):
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

height_from_last_blocks = max_height - height_before_last_blocks
total_height_after_all_blocks = max_height_after_repeats_that_fit + height_from_last_blocks
print(f"After placing {TOTAL_BLOCKS_TO_PLACE_PART2} blocks the column reaches {total_height_after_all_blocks + 1} high")
