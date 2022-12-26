# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

# Part 1
def anyoneAround(elf_pos, all_positions):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i ==0 and j == 0:
                continue
            test_pos = (elf_pos[0] + i, elf_pos[1] + j)
            if test_pos in all_positions:
                return True
    return False
def canMoveDir(elf_pos, all_positions, dir):
    if dir == 'N':
        n_pos = (elf_pos[0], elf_pos[1] + 1)
        ne_pos = (elf_pos[0] + 1, elf_pos[1] + 1)
        nw_pos = (elf_pos[0] - 1, elf_pos[1] + 1)
        if n_pos not in all_positions and ne_pos not in all_positions and nw_pos not in all_positions:
            return n_pos
    elif dir == 'S':
        s_pos = (elf_pos[0], elf_pos[1] - 1)
        se_pos = (elf_pos[0] + 1, elf_pos[1] - 1)
        sw_pos = (elf_pos[0] - 1, elf_pos[1] - 1)
        if s_pos not in all_positions and se_pos not in all_positions and sw_pos not in all_positions:
            return s_pos
    elif dir == 'E':
        e_pos = (elf_pos[0] + 1, elf_pos[1])
        se_pos = (elf_pos[0] + 1, elf_pos[1] - 1)
        ne_pos = (elf_pos[0] + 1, elf_pos[1] + 1)
        if e_pos not in all_positions and ne_pos not in all_positions and se_pos not in all_positions:
            return e_pos
    elif dir == 'W':
        w_pos = (elf_pos[0] - 1, elf_pos[1])
        sw_pos = (elf_pos[0] - 1, elf_pos[1] - 1)
        nw_pos = (elf_pos[0] - 1, elf_pos[1] + 1)
        if w_pos not in all_positions and nw_pos not in all_positions and sw_pos not in all_positions:
            return w_pos
    else:
        raise Exception("Should be impossible")
    return None

def firstValidMove(elf_pos, all_positions, dir_order):
    for dir in dir_order:
        pos_move = canMoveDir(elf_pos, all_positions, dir)
        if pos_move is not None:
            return pos_move
    return None
    

elf_positions = set()
for y, line in enumerate(reversed(input_lines)):
    for x, char in enumerate(line):
        if char == '#':
            elf_positions.add((x, y))

TOTAL_ROUNDS = 10
dir_order = ['N', 'S', 'W', 'E']
round_count = 0
while True:
    # Generate possible moves
    desired_move_counts = {}
    elf_moves = {}
    for elf_position in elf_positions:
        if anyoneAround(elf_position, elf_positions):
            # someone is around we need to propose a move
            desired_move = firstValidMove(elf_position, elf_positions, dir_order)
            if desired_move is None:
                continue
            if desired_move in desired_move_counts:
                desired_move_counts[desired_move] += 1
            else:
                desired_move_counts[desired_move] = 1
            elf_moves[elf_position] = desired_move
        else:
            if elf_position in desired_move_counts:
                raise Exception("SHOULD NOT BE POSSIBLE")
            desired_move_counts[elf_position] = 1
    
    # Filter invalid moves
    filtered_moves = {k:v for k,v in elf_moves.items() if desired_move_counts[v] <= 1}
    
    # break when we would not move
    if len(filtered_moves) == 0:
        break
    
    # make filtered moves
    for old_pos, new_pos in filtered_moves.items():
        elf_positions.remove(old_pos)
        elf_positions.add(new_pos)
    
    # rotate move list
    dir_order.append(dir_order.pop(0))
    
    round_count += 1
    
    # Part 1 print
    if round_count == TOTAL_ROUNDS:
        min_x = min(elf_positions, key=lambda a:a[0])[0]
        min_y = min(elf_positions, key=lambda a:a[1])[1]
        max_x = max(elf_positions, key=lambda a:a[0])[0]
        max_y = max(elf_positions, key=lambda a:a[1])[1]
        
        len_x = max_x - min_x + 1
        len_y = max_y - min_y + 1
        print(f"There were {(len_y * len_x) - len(elf_positions)} empty tiles")
print(f"Round {round_count + 1} is the first round with no movement")

