# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

traces_as_points = [[tuple([int(i) for i in point_str.split(',')]) for point_str in line.split(" -> ")] for line in input_lines]

# Part 1
def drawLine(grid, line):
    start = line[0]
    end = line[1]
    if start[0] != end[0]:
        # Horizontal line
        y = start[1]
        for i in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
            grid[y][i] = '#'
    else:
        # Vertical line
        x = start[0]
        for i in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
            grid[i][x] = '#'

def tryPlaceSand(grid, point):
    """Will return the point it slid to (if same as point it didn't slide)
    or None if it would have gone out of bounds.
    """
    # Check if at bottom border
    down_y = point[1] + 1
    if down_y >= len(grid):
        return None
    # Check straight down
    if grid[down_y][point[0]] == '.':
        possible_y = down_y
        # Move down as far as possible
        while grid[possible_y + 1][point[0]] == '.':
            possible_y += 1
        return (point[0], possible_y)

    # Check left border
    left_x = point[0] - 1
    if left_x < 0:
        return None
    # Check down left
    if grid[down_y][left_x] == '.':
        return (left_x, down_y)

    # Check right border
    right_x = point[0] + 1
    if right_x >= len(grid[0]):
        return None
    # Check down right
    if grid[down_y][right_x] == '.':
        return (right_x, down_y)
    
    return point

def dropSand(grid, drop_point):
    """Returns false if it could not place and true if it could"""
    test_point = drop_point
    drop_result = tryPlaceSand(grid, test_point)
    while test_point != drop_result:
        test_point = drop_result
        drop_result = tryPlaceSand(grid, test_point)
        if drop_result is None:
            return False
    grid[drop_result[1]][drop_result[0]] = '0'
    return True

# Find the max and min extent on both axis so we can shrink the grid to build
def getAllPoints(lines):
    for line in lines:
        for point in line:
            yield point
max_x = max(getAllPoints(traces_as_points), key=lambda item:item[0])[0]
min_x = min(getAllPoints(traces_as_points), key=lambda item:item[0])[0]
max_y = max(getAllPoints(traces_as_points), key=lambda item:item[1])[1]
min_y = min(getAllPoints(traces_as_points), key=lambda item:item[1])[1]

# Shift the indexes to fit into the smaller grid
traces_with_shifted_indexes = [[(point[0] - min_x, point[1]) for point in trace] for trace in traces_as_points]

# Draw all the lines in the grid
grid = [['.' for j in range(0, max_x - min_x + 1)] for i in range(0, max_y + 1)]
for trace in traces_with_shifted_indexes:
    for line in zip(trace, trace[1:]):
        drawLine(grid, line)

# Keep dropping sand till we cant any more
count = 0
while dropSand(grid, (500 - min_x, 0)):
    count += 1

print(f"Need to drop {count} grains of sand till one falls into the abyss")

# Part 2
# For part 2 I converted the grid into a map so it could expand forever.
# Could technically be a set instead since the actual characters don't matter but
# I used them for drawing while testing.

def tryPlaceSandSparse(block_map, point, max):
    """Will return the point it slid to (if same as point it didn't slide)
    """
    # Check for bottom border
    down_y = point[1] + 1
    if down_y > max:
        return point
    # Check straight down
    if (point[0], down_y) not in block_map:
        possible_y = down_y
        # Move down as far as possible
        while possible_y + 1 <= max and (point[0], possible_y + 1) not in block_map:
            possible_y += 1
        return (point[0], possible_y)

    # Check down left
    left_x = point[0] - 1
    if (left_x, down_y) not in block_map:
        return (left_x, down_y)

    # Check down right
    right_x = point[0] + 1
    if (right_x, down_y) not in block_map:
        return (right_x, down_y)
    
    return point

def dropSandSparse(block_map, drop_point, max):
    """Returns false if it could not place and true if it could"""
    test_point = drop_point
    drop_result = tryPlaceSandSparse(block_map, test_point, max)
    while test_point != drop_result:
        test_point = drop_result
        drop_result = tryPlaceSandSparse(block_map, test_point, max)
    block_map[drop_result] = '0'
    return drop_result


def drawLineSparse(block_map, line):
    start = line[0]
    end = line[1]
    if start[0] != end[0]:
        # Horizontal line
        y = start[1]
        for i in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
            block_map[(i, y)] = '#'
    else:
        # Vertical line
        x = start[0]
        for i in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
            block_map[(x, i)] = '#'

# Draw all the lines in the grid
blocked_points = {}
for trace in traces_as_points:
    for line in zip(trace, trace[1:]):
        drawLineSparse(blocked_points, line)

count = 0
while dropSandSparse(blocked_points, (500, 0), max_y + 1) != (500, 0):
    count += 1

print(f"Need to drop {count + 1} grains of sand to reach the top.")