# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

sensor_beacon_pairs = [tuple([tuple([int(x) for x in point.split(",")]) for point in line.replace("Sensor at x=", "").replace(" closest beacon is at x=", "").replace(" y=", "").split(":")]) for line in input_lines]

# Part 1
def manhattenDistance(start, end):
    return abs(end[0] - start[0]) + abs(end[1] - start[1])

def doesOverlap(sensor_beacon_distance, y):
    return sensor_beacon_distance[2] >= abs(sensor_beacon_distance[0][1] - y)

def getOverlap(sensor_beacon_distance, y):
    sensor = sensor_beacon_distance[0]
    distance = sensor_beacon_distance[2]
    remaining_distance = distance - abs(y - sensor[1])
    return (sensor[0] - remaining_distance, sensor[0] + remaining_distance)

y_to_use = 10
# y_to_use = 2000000

sensor_beacon_distance_tuples = [(sensor_beacon[0], sensor_beacon[1], manhattenDistance(sensor_beacon[0], sensor_beacon[1]))for sensor_beacon in sensor_beacon_pairs]
overlap_lines = [getOverlap(sensor_beacon_distance, y_to_use) for sensor_beacon_distance in sensor_beacon_distance_tuples if doesOverlap(sensor_beacon_distance, y_to_use)]

unique_spots = set()
for line_segment in overlap_lines:
    for i in range(line_segment[0], line_segment[1] + 1):
        unique_spots.add(i)

for sensor_beacon in sensor_beacon_pairs:
    beacon = sensor_beacon[1]
    if beacon[1] == y_to_use:
        unique_spots.discard(beacon[0])

print(f"There are {len(unique_spots)} places a beacon can't be")

# Part 2
def getOverlapBound(sensor_beacon_distance, y, bound_x):
    sensor = sensor_beacon_distance[0]
    distance = sensor_beacon_distance[2]
    remaining_distance = distance - abs(y - sensor[1])
    pos_x_low = sensor[0] - remaining_distance
    pos_x_high = sensor[0] + remaining_distance
    if pos_x_high < 0 or pos_x_low > bound_x:
        return None
    return (max(0, pos_x_low), min(pos_x_high, bound_x))

def simplifyOverlaps(overlaps):
    overlaps.sort()
    stack = [overlaps.pop(0)]
    for line_segment in overlaps:
        comp = stack.pop()
        if comp[0] <= line_segment[0] <= comp[1]:
            # merge
            stack.append((comp[0], max(comp[1], line_segment[1])))
        else:
            stack.append(comp)
            stack.append(line_segment)
    return stack

max_y = 20
# max_y = 4000000
for stripe_y in range(0, max_y + 1):
    overlap_lines = []
    for sensor_beacon_distance in sensor_beacon_distance_tuples:
        if doesOverlap(sensor_beacon_distance, stripe_y):
            overlap = getOverlapBound(sensor_beacon_distance, stripe_y, max_y)
            if overlap is not None:
                overlap_lines.append(overlap)

    overlaps = simplifyOverlaps(overlap_lines)

    if len(overlaps) > 1:
        print(f"y: {stripe_y}")
        print(f"segments: {overlaps}")
        print(f"tuning frequency is: {(4000000 * (overlaps[0][1] + 1)) + stripe_y}")
        break