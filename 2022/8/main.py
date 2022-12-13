# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

grid = [[int(char) for char in line] for line in input_lines]

# Part 1
unique_trees = set()
y_len = len(grid)
x_len = len(grid[0])

for i in range(0, y_len):
    current_max = -1
    for j in range(0, x_len):
        tree_height = grid[i][j]
        if tree_height > current_max:
            current_max = tree_height
            unique_trees.add((i, j))
        if current_max == 9:
            break

# Right pass
for i in range(0, y_len):
    current_max = -1
    for j in reversed(range(0, x_len)):
        tree_height = grid[i][j]
        if tree_height > current_max:
            current_max = tree_height
            unique_trees.add((i, j))
        if current_max == 9:
            break

# Top pass
for j in range(0, x_len):
    current_max = -1
    for i in range(0, y_len):
        tree_height = grid[i][j]
        if tree_height > current_max:
            current_max = tree_height
            unique_trees.add((i, j))
        if current_max == 9:
            break

# Bottom pass
for j in range(0, x_len):
    current_max = -1
    for i in reversed(range(0, y_len)):
        tree_height = grid[i][j]
        if tree_height > current_max:
            current_max = tree_height
            unique_trees.add((i, j))
        if current_max == 9:
            break

print(f"There are {len(unique_trees)} trees that can be seen from outside")

# Part 2
def calcScenicScore(grid, x, y):
    scenic_score = 1
    tree_height =  grid[y][x]

    # Look left
    trees_seen = 0
    for i in reversed(range(0, x)):
        trees_seen += 1
        if grid[y][i] >= tree_height:
            break
    scenic_score *= trees_seen

    # Look right
    trees_seen = 0
    for i in range(x + 1, x_len):
        trees_seen += 1
        if grid[y][i] >= tree_height:
            break
    scenic_score *= trees_seen

    # Look down
    trees_seen = 0
    for i in range(y + 1, y_len):
        trees_seen += 1
        if grid[i][x] >= tree_height:
            break
    scenic_score *= trees_seen

    # Look up
    trees_seen = 0
    for i in reversed(range(0, y)):
        trees_seen += 1
        if grid[i][x] >= tree_height:
            break
    scenic_score *= trees_seen

    return scenic_score

max_scenic_score = 0
for i in range(0, y_len):
    for j in range(0, x_len):
        scenic_score = calcScenicScore(grid, j, i)
        max_scenic_score = max(scenic_score, max_scenic_score)

print(f"The highest scenic score for a tree is: {max_scenic_score}")