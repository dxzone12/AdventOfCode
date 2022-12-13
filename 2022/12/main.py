from heapq import heappush, heappop

# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

grid = [list(line) for line in input_lines]

start = None
end = None
for i, line in enumerate(grid):
    for j, point in enumerate(line):
        if point == 'S':
            start = (i, j)
            grid[i][j] = 'a'
        if point == 'E':
            end = (i, j)
            grid[i][j] = 'z'
        if start is not None and end is not None:
            break

# Part 1
# We want to A* search from start to end
pq_entry_map = {}
def addNode(heap, node, priority):
    if node in pq_entry_map:
        to_clean = pq_entry_map.pop(node)
        to_clean[2] = False
    entry = (priority, node, True)
    pq_entry_map[node] = entry
    heappush(heap, entry)

def nextNode(heap):
    while len(heap) > 0:
        possible = heappop(heap)
        if possible[2]:
            del pq_entry_map[possible[1]]
            return possible[1]

def getValidNeighbours(el_map, node):
    neighbours = []

    node_i, node_j = node
    node_height = ord(el_map[node_i][node_j])
    possible_height = node_height + 1

    # Check top
    up_i = node_i - 1
    if up_i >= 0 and ord(el_map[up_i][node_j]) <= possible_height:
        neighbours.append((up_i, node_j))
    # Check bottom
    down_i = node_i + 1
    if down_i < len(el_map) and ord(el_map[down_i][node_j]) <= possible_height:
        neighbours.append((down_i, node_j))
    # Check right
    right_j = node_j + 1
    if right_j < len(el_map[0]) and ord(el_map[node_i][right_j]) <= possible_height:
        neighbours.append((node_i, right_j))
    # Check left
    left_j = node_j - 1
    if left_j >= 0 and ord(el_map[node_i][left_j]) <= possible_height:
        neighbours.append((node_i, left_j))

    return neighbours

def heuristic(node, target):
    # using manhatten distance for 4 directional movement
    return abs(target[0] - node[0]) + abs(target[1] - node[1])

prev = {start: None}
dist = {start: 0}
pq = []
addNode(pq, start, 0)
while len(pq) > 0:
    # Get node
    current = nextNode(pq)
    if current == end:
        break

    # Process node
    valid_neighbours = getValidNeighbours(grid, current)
    for neighbour in valid_neighbours:
        tentative_dist = dist[current] + 1
        if neighbour not in dist or tentative_dist < dist[neighbour]:
            prev[neighbour] = current
            dist[neighbour] = tentative_dist
            addNode(pq, neighbour, tentative_dist + heuristic(current, neighbour))

# reconstruct the path and print its length minus 1 for the start node
print(f"We went {dist[end]} steps")

# Part 2
def getValidNeighboursInverse(el_map, node):
    neighbours = []

    node_i, node_j = node
    node_height = ord(el_map[node_i][node_j])
    possible_height = node_height - 1

    # Check top
    up_i = node_i - 1
    if up_i >= 0 and ord(el_map[up_i][node_j]) >= possible_height:
        neighbours.append((up_i, node_j))
    # Check bottom
    down_i = node_i + 1
    if down_i < len(el_map) and ord(el_map[down_i][node_j]) >= possible_height:
        neighbours.append((down_i, node_j))
    # Check right
    right_j = node_j + 1
    if right_j < len(el_map[0]) and ord(el_map[node_i][right_j]) >= possible_height:
        neighbours.append((node_i, right_j))
    # Check left
    left_j = node_j - 1
    if left_j >= 0 and ord(el_map[node_i][left_j]) >= possible_height:
        neighbours.append((node_i, left_j))

    return neighbours

prev = {end: None}
dist = {end: 0}
pq = []
pq_entry_map = {}
addNode(pq, end, 0)
while len(pq) > 0:
    # Get node
    current = nextNode(pq)

    # Process node
    valid_neighbours = getValidNeighboursInverse(grid, current)
    for neighbour in valid_neighbours:
        tentative_dist = dist[current] + 1
        if neighbour not in dist or tentative_dist < dist[neighbour]:
            prev[neighbour] = current
            dist[neighbour] = tentative_dist
            addNode(pq, neighbour, tentative_dist + heuristic(current, neighbour))

valid_end_distances = sorted([dist[key] for key in dist if grid[key[0]][key[1]] == 'a'])
print(f"Shortest hike start is: {valid_end_distances[0]}")