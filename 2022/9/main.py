# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

motions = [line.split() for line in input_lines]

# Part 1
head_pos = (0,0)
tail_pos = (0,0)
tail_positions = {tail_pos}

def clamp(x):
    return max(min(1, x), -1)

def move(pos, move_vect):
    return (pos[0] + move_vect[0], pos[1] + move_vect[1])

def moveInDirection(pos, direction):
    match direction:
        case 'U':
            return move(pos, (0, 1))
        case 'D':
            return move(pos, (0, -1))
        case 'R':
            return move(pos, (1, 0))
        case 'L':
            return move(pos, (-1, 0))
        case _:
            raise Exception("Unknown direction")    

def tailMovement(head_position, tail_position):
    dist_x = head_position[0] - tail_position[0]
    dist_y = head_position[1] - tail_position[1]

    if abs(dist_x) >= 2:
        move_x = clamp(dist_x)
        move_y = clamp(dist_y)
        return (move_x, move_y)
    elif abs(dist_y) >= 2:
        move_y = clamp(dist_y)
        move_x = clamp(dist_x)
        return (move_x, move_y)
    else:
        return None

for motion in motions:
    direction = motion[0]
    distance = int(motion[1])

    # Move distance times
    for i in range(0,distance):
        # Move
        head_pos = moveInDirection(head_pos, direction)

        # Move the tail if necessary
        tail_move = tailMovement(head_pos, tail_pos)
        if tail_move:
            tail_pos = move(tail_pos, tail_move)
            tail_positions.add(tail_pos)
        
print(f"Tail went to {len(tail_positions)} unique postiions")

# Part 2
tail_positions = {(0, 0)}
rope_positions = [(0, 0) for i in range(0, 10)]

def printGrid(rope_poss):
    grid = [['.', '.', '.', '.', '.', '.'] for i in range(0, 6)]
    for i in range(0, len(rope_poss)):
        pos = rope_poss[i]
        grid[int(pos[1])][int(pos[0])] = str(i)
    for line in reversed(grid):
        print(line)
    print("----------------------------------------")

for motion in motions:
    direction = motion[0]
    distance = int(motion[1])

    # Move distance times
    for i in range(0, distance):
        # Move head
        rope_positions[0] = moveInDirection(rope_positions[0], direction)

        # Move each other not if necessary
        for j in range(1, 10):
            tail_move = tailMovement(rope_positions[j - 1], rope_positions[j])
            if tail_move:
                rope_positions[j] = move(rope_positions[j], tail_move)
        
        # Record new tail pos
        tail_positions.add(rope_positions[9])

print(f"Tail went to {len(tail_positions)} unique positions")