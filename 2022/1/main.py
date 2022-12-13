# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

count = 0
counts = []
for line in input_lines:
    if line == "":
        counts.append(count)
        count = 0
    else:
        count += int(line)
counts.append(count)
counts.sort(reverse = True)

print(f"Max is: {counts[0]}")
print(f"Total of top 3 is: {counts[0] + counts[1] + counts[2]}")