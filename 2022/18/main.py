# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

cube_locations = [tuple([int(x) for x in line.split(",")]) for line in input_lines]

# Part 1
def getExposedSides(locations: set[tuple[int,int,int]], target: tuple[int,int,int]) -> int:
    exposed = 0
    # Check left
    new_x = target[0] - 1
    pos_loc = (new_x, target[1], target[2])
    if pos_loc not in locations:
        exposed += 1
    # Check right
    new_x = target[0] + 1
    pos_loc = (new_x, target[1], target[2])
    if pos_loc not in locations:
        exposed += 1
    # Check up
    new_y = target[1] + 1
    pos_loc = (target[0], new_y, target[2])
    if pos_loc not in locations:
        exposed += 1
    # Check down
    new_y = target[1] - 1
    pos_loc = (target[0], new_y, target[2])
    if pos_loc not in locations:
        exposed += 1
    # Check front
    new_z = target[2] - 1
    pos_loc = (target[0], target[1], new_z)
    if pos_loc not in locations:
        exposed += 1
    # Check back
    new_z = target[2] + 1
    pos_loc = (target[0], target[1], new_z)
    if pos_loc not in locations:
        exposed += 1

    return exposed

cube_locations_set = set(cube_locations)
exposed_sides = 0
for cube in cube_locations:
    exposed_sides += getExposedSides(cube_locations_set, cube)

print(f"There are {exposed_sides} exposed sides")

# Part 2
all_x = [cube[0] for cube in cube_locations]
all_y = [cube[1] for cube in cube_locations]
all_z = [cube[2] for cube in cube_locations]

# Find coordinates of box 1 wider on all sides
low_bound_x = min(all_x) - 1
low_bound_y = min(all_y) - 1 
low_bound_z = min(all_z) - 1
upper_bound_x = max(all_x) + 1
upper_bound_y = max(all_y) + 1
upper_bound_z = max(all_z) + 1

# BFS from bottom left through all empty cubes to count all faces touching empty cubes
air_cubes = [(low_bound_x, low_bound_y, low_bound_z)]
visited_air_cubes = set()
exposed_sides = 0
while len(air_cubes) > 0:
    next_node = air_cubes.pop(0)
    if next_node in visited_air_cubes:
        continue
    visited_air_cubes.add(next_node)
    # Check left
    new_x = next_node[0] - 1
    pos_loc = (new_x, next_node[1], next_node[2])
    if pos_loc in cube_locations_set:
        exposed_sides += 1
    elif new_x >= low_bound_x:
        air_cubes.append(pos_loc)
    # Check right
    new_x = next_node[0] + 1
    pos_loc = (new_x, next_node[1], next_node[2])
    if pos_loc in cube_locations_set:
        exposed_sides += 1
    elif new_x <= upper_bound_x:
        air_cubes.append(pos_loc)
    # Check up
    new_y = next_node[1] + 1
    pos_loc = (next_node[0], new_y, next_node[2])
    if pos_loc in cube_locations_set:
        exposed_sides += 1
    elif new_y <= upper_bound_y:
        air_cubes.append(pos_loc)
    # Check down
    new_y = next_node[1] - 1
    pos_loc = (next_node[0], new_y, next_node[2])
    if pos_loc in cube_locations_set:
        exposed_sides += 1
    elif new_y >= low_bound_y:
        air_cubes.append(pos_loc)
    # Check front
    new_z = next_node[2] - 1
    pos_loc = (next_node[0], next_node[1], new_z)
    if pos_loc in cube_locations_set:
        exposed_sides += 1
    elif new_z >= low_bound_z:
        air_cubes.append(pos_loc)
    # Check back
    new_z = next_node[2] + 1
    pos_loc = (next_node[0], next_node[1], new_z)
    if pos_loc in cube_locations_set:
        exposed_sides += 1
    elif new_z <= upper_bound_z:
        air_cubes.append(pos_loc)

print(f"There are {exposed_sides} sides exposed to outside air")