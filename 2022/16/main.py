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

def recursivePermute(output_perms: list[str], current_dist: int, dists: dict[str,int], current_perm: list[str], remaining_elements: list[str]):
    remaining_elements = list(remaining_elements)
    if len(remaining_elements) <= 0:
        output_perms.append(list(current_perm))
        return
    
    can_proceed = False
    for element in remaining_elements:
        tentative_dist = current_dist + dists[getKey(current_perm[-1], element)] + 1 # add one is for valve opening time
        if tentative_dist >= 30:
            continue

        can_proceed = True
        new_perm = list(current_perm)
        new_perm.append(element)
        now_remaining = list(remaining_elements)
        now_remaining.remove(element)
        recursivePermute(output_perms, tentative_dist, dists, new_perm, now_remaining)
    
    if not can_proceed:
        output_perms.append(current_perm)
    return

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

# Attempted greedy approach
remaining_nodes = [node_info[0] for node_info in node_infos if node_info[1] > 0]
permutations = []
recursivePermute(permutations, 0, shortest_paths, ['AA'], remaining_nodes)


pressure_map = {node_info[0]:node_info[1] for node_info in node_infos if node_info[1] > 0}
best_score = 0
for perm in permutations:
    this_perm_score = 0
    previous_element = 'AA'
    remaining_time = 30
    for element in perm[1:]:
        travel_time = shortest_paths[getKey(previous_element, element)]
        total_time = travel_time + 1
        remaining_time -= total_time
        this_perm_score += pressure_map[element] * remaining_time
        previous_element = element
    if this_perm_score > best_score:
        best_score = this_perm_score

print(f"The most pressure that could be released is: {best_score}")