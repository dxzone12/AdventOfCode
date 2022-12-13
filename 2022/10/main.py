# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

# Part 1
thresholds = [20, 60, 100, 140, 180, 220]
next_threshold = thresholds.pop(0)

cycle_count = 0
x = 1
signal_strengths = 0
for line in input_lines:
    parts = line.split()

    # Increase count
    cycle_count += 1 if len(parts) == 1 else 2

    # Check if need to report signal strength
    if cycle_count >= next_threshold:
        signal_strengths += x * next_threshold
        if len(thresholds) == 0:
            break
        next_threshold = thresholds.pop(0)
    
    # Add to x if needed
    if len(parts) == 2:
        x += int(parts[1])

print(f"The sum of all signal strengths is: {signal_strengths}")


# Part 2
grid = [['.' for j in range(0, 40)] for i in range(0, 6)]
cycle_count = 0
x = 1
for line in input_lines:
    parts = line.split()

    # how much to increase
    cycle_count_increase = 1 if len(parts) == 1 else 2

    # Simulate cycles and build grid
    for i in range(0, cycle_count_increase):
        line_num = cycle_count // 40
        col_num = cycle_count % 40
        if (x - 1) <= col_num <= (x + 1):
            grid[line_num][col_num] = '#'
        cycle_count += 1
    
    # Add to x if needed
    if len(parts) == 2:
        x += int(parts[1])

for grid_line in grid:
    print(grid_line)