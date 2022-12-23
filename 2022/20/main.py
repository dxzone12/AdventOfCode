# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()


# Part 1
class Node:
    def __init__(self, val) -> None:
        self.Value = val
        self.Next: Node = None
        self.Prev: Node = None

def popNode(node_to_pop: Node):
    node_to_pop.Prev.Next = node_to_pop.Next
    node_to_pop.Next.Prev = node_to_pop.Prev

def nextNode(node: Node, backwards: bool, start_node: Node):
    pos_next_node = node.Prev if backwards else node.Next
    if pos_next_node is start_node:
        pos_next_node = pos_next_node.Prev if backwards else pos_next_node.Next
    next_next_node = pos_next_node.Prev if backwards else pos_next_node.Next
    if next_next_node is start_node:
        return start_node
    return pos_next_node

def insertBetween(to_insert: Node, prev_node: Node, next_node: Node):
    prev_node.Next = to_insert
    to_insert.Prev = prev_node
    next_node.Prev = to_insert
    to_insert.Next = next_node

def getList(start_node: Node):
    vals = []
    node = start_node.Next
    while node.Value is not None:
        vals.append(node.Value)
        node = node.Next
    return vals

# Build a link list with a dummy empty node to mark the start of the list
# Also record a link to each node for their original position in the input
nodes: list[Node] = []
start_node = Node(None)
cur_node = start_node
for line in input_lines:
    value = int(line)
    new_node = Node(value)
    nodes.append(new_node)
    cur_node.Next = new_node
    new_node.Prev = cur_node
    cur_node = new_node
# link the end back to the start
cur_node.Next = start_node
start_node.Prev = cur_node

for node in nodes:
    places_to_shift = abs(node.Value) % (len(nodes) - 1) # subtract 1 here as we will pull ourselves out of the list to loop
    if places_to_shift == 0:
        continue
    
    popNode(node)

    moving_backwards = node.Value < 0
    next_node = node
    for __ in range(0, places_to_shift):
        next_node = nextNode(next_node, moving_backwards, start_node)
    
    if moving_backwards:
        insertBetween(node, next_node.Prev, next_node)
    else:
        insertBetween(node, next_node, next_node.Next)

new_list = getList(start_node)
zero_index = new_list.index(0)
cooardinates = [
    new_list[(zero_index + 1000) % len(new_list)],
    new_list[(zero_index + 2000) % len(new_list)],
    new_list[(zero_index + 3000) % len(new_list)]
]
print(f"The sum of coordinates is: {sum(cooardinates)}")

# Part 2
# Build a link list with a dummy empty node to mark the start of the list
# Also record a link to each node for their original position in the input
nodes: list[Node] = []
start_node = Node(None)
cur_node = start_node
for line in input_lines:
    value = int(line) * 811589153
    new_node = Node(value)
    nodes.append(new_node)
    cur_node.Next = new_node
    new_node.Prev = cur_node
    cur_node = new_node
# link the end back to the start
cur_node.Next = start_node
start_node.Prev = cur_node

for __ in range(0, 10):
    for node in nodes:
        places_to_shift = abs(node.Value) % (len(nodes) - 1) # subtract 1 here as we will pull ourselves out of the list to loop
        if places_to_shift == 0:
            continue
        
        popNode(node)

        moving_backwards = node.Value < 0
        next_node = node
        for __ in range(0, places_to_shift):
            next_node = nextNode(next_node, moving_backwards, start_node)
        
        if moving_backwards:
            insertBetween(node, next_node.Prev, next_node)
        else:
            insertBetween(node, next_node, next_node.Next)

new_list = getList(start_node)
zero_index = new_list.index(0)
cooardinates = [
    new_list[(zero_index + 1000) % len(new_list)],
    new_list[(zero_index + 2000) % len(new_list)],
    new_list[(zero_index + 3000) % len(new_list)]
]
print(f"The sum of decrypted coordinates is: {sum(cooardinates)}")