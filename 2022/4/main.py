# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

# extra input processing
pairs = []
for line in input_lines:
    raw_pair = line.split(",")
    range1_as_ints = [int(x) for x in raw_pair[0].split("-")]
    range2_as_ints = [int(x) for x in raw_pair[1].split("-")]
    pairs.append((tuple(range1_as_ints), tuple(range2_as_ints)))

# part 1
# returns true if range1 contains range2 completely
def contains(range1, range2):
    return range1[0] <= range2[0] and range1[1] >= range2[1]

count = 0
for pair in pairs:
    # Check if either range contains the other
    if contains(pair[0], pair[1]) or contains(pair[1], pair[0]):
        count += 1

print(f"Count of pairs where one contains another: {count}")

# Part 2
# Returns true if range1 and range2 overlap at all
def overlaps(range1, range2):
    return (range2[0] <= range1[0] <= range2[1]) or (range1[0] <= range2[0] <= range1[1])

count2 = 0
for pair in pairs:
    if overlaps(pair[0], pair[1]):
        count2 += 1
print(f"count of pairs that overlap at all: {count2}")