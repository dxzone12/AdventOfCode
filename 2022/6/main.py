# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

line = input_lines[0]

# Part 1
end_index = 3
sliding_window = line[:4]
while len(set(sliding_window)) < 4:
    end_index += 1
    sliding_window = sliding_window[1:] + line[end_index]
print(f"How many characters processed: {end_index + 1}")

# Part 2
end_index = 13
sliding_window = line[:14]
while len(set(sliding_window)) < 14:
    end_index += 1
    sliding_window = sliding_window[1:] + line[end_index]
print(f"How many characters processed: {end_index + 1}")