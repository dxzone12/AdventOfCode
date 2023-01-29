import math

# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

cleaned_inputs = [line.replace("Valve ", "").replace(" has flow rate=", ";").replace(" tunnels lead to valves ", "").replace(" tunnel leads to valve ", "").replace(" ","") for line in input_lines]
raw_node_infos = [tuple(clean_input.split(";")) for clean_input in cleaned_inputs]
node_infos = [(raw_info[0], int(raw_info[1]), raw_info[2].split(",")) for raw_info in raw_node_infos]
node_names = [node_info[0] for node_info in node_infos]

# Part 1
def getKey(node_1, node_2):
    return tuple(sorted((node_1, node_2)))

def recursivePermute(output_perms: list[str], current_dist: int, dists: dict[str,int], current_perm: list[str], remaining_elements: list[str], time_limit: int):
    remaining_elements = list(remaining_elements)
    if len(remaining_elements) <= 0:
        output_perms.append(list(current_perm))
        return
    
    can_proceed = False
    for element in remaining_elements:
        tentative_dist = current_dist + dists[getKey(current_perm[-1], element)] + 1 # add one is for valve opening time
        if tentative_dist >= time_limit:
            continue

        can_proceed = True
        new_perm = list(current_perm)
        new_perm.append(element)
        now_remaining = list(remaining_elements)
        now_remaining.remove(element)
        recursivePermute(output_perms, tentative_dist, dists, new_perm, now_remaining, time_limit)
    
    if not can_proceed:
        output_perms.append(current_perm)
    return

def calcPermScore(permutation, shortest_path_map, map_of_pressures, time_limit):
    this_perm_score = 0
    previous_element = 'AA'
    remaining_time = time_limit
    for element in permutation[1:]:
        travel_time = shortest_path_map[getKey(previous_element, element)]
        total_time = travel_time + 1
        remaining_time -= total_time
        this_perm_score += map_of_pressures[element] * remaining_time
        previous_element = element
    return this_perm_score

# floyd-warshall algorithm for any to any shrotest path
shortest_paths = {}
for i in node_names:
    for j in node_names:
        shortest_paths[getKey(i, j)] = 10000 if i != j else 0
for node_info in node_infos:
    for target_node in node_info[2]:
        from_node = node_info[0]
        shortest_paths[getKey(from_node, target_node)] = 1
for k in node_infos:
    k_name = k[0]
    for i in node_infos:
        i_name = i[0]
        for j in node_infos:
            j_name = j[0]
            i_to_k = shortest_paths[getKey(i_name, k_name)]
            k_to_j = shortest_paths[getKey(k_name, j_name)]
            i_to_j = shortest_paths[getKey(i_name, j_name)]
            if i_to_j > (i_to_k + k_to_j):
                shortest_paths[getKey(i_name, j_name)] = (i_to_k + k_to_j)

# Generate all permutations possible in this time frame
PART1_TIME_LIMIT = 30
remaining_nodes = [node_info[0] for node_info in node_infos if node_info[1] > 0]
permutations = []
recursivePermute(permutations, 0, shortest_paths, ['AA'], remaining_nodes, PART1_TIME_LIMIT)

pressure_map = {node_info[0]:node_info[1] for node_info in node_infos if node_info[1] > 0}
best_score = 0
for perm in permutations:
    this_perm_score = calcPermScore(perm, shortest_paths, pressure_map, PART1_TIME_LIMIT)
    if this_perm_score > best_score:
        best_score = this_perm_score

print(f"The most pressure that could be released is: {best_score}")

# Part 2
PART2_TIME_LIMIT = 26
def recursivePermuteOfDepth(output_perms: list[str], current_dist: int, dists: dict[str,int], current_perm: list[str], remaining_elements: list[str], time_limit: int, max_depth: int):
    remaining_elements = list(remaining_elements)
    if len(current_perm) == (max_depth + 1): # +1 to account for the start node in perm list
        output_perms.append(list(current_perm))
        return
    
    for element in remaining_elements:
        tentative_dist = current_dist + dists[getKey(current_perm[-1], element)] + 1 # add one is for valve opening time
        if tentative_dist >= time_limit:
            continue

        new_perm = list(current_perm)
        new_perm.append(element)
        now_remaining = list(remaining_elements)
        now_remaining.remove(element)
        recursivePermuteOfDepth(output_perms, tentative_dist, dists, new_perm, now_remaining, time_limit, max_depth)
    
    return

def getPermScoreMapKey(perm):
    return ';'.join(sorted(perm))

perm_score_map = {}
best_combined_score = 0
for i in range(1, int(math.ceil(len(remaining_nodes)/2)) + 1):
    # Find all perms at exactly this depth
    pos_perms = []
    recursivePermuteOfDepth(pos_perms, 0, shortest_paths, ['AA'], remaining_nodes, PART2_TIME_LIMIT, i)

    # Find the best perm at this depth when accounting for the elephant working on the remainder
    for perm in pos_perms:
        main_perm_score = calcPermScore(perm, shortest_paths, pressure_map, PART2_TIME_LIMIT)
        now_remaining = list(remaining_nodes)
        for node in perm[1:]:
            now_remaining.remove(node)
        
        # Work out the best path for all nodes not covered by perm and cache the answer as it is likely to re-appear
        perm_score_map_key = getPermScoreMapKey(now_remaining)
        best_remaining_score = None
        if perm_score_map_key in perm_score_map:
            best_remaining_score = perm_score_map[perm_score_map_key]
        else:
            remaining_pos_perms = []
            recursivePermute(remaining_pos_perms, 0, shortest_paths, ['AA'], now_remaining, PART2_TIME_LIMIT)
            pos_best_remaining_score = 0
            for rem_perm in remaining_pos_perms:
                this_perm_score = calcPermScore(rem_perm, shortest_paths, pressure_map, PART2_TIME_LIMIT)
                if this_perm_score > pos_best_remaining_score:
                    pos_best_remaining_score = this_perm_score
            perm_score_map[perm_score_map_key] = pos_best_remaining_score
            best_remaining_score = pos_best_remaining_score
        
        # Calculate combined score of perm and the best path through remaining nodes
        this_combined_score = best_remaining_score + main_perm_score
        if this_combined_score > best_combined_score:
            best_combined_score = this_combined_score

print(f"The most pressure that could be released by you and the elephant is: {best_combined_score}")