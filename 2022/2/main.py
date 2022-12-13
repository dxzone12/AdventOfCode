# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

# part 1
hand_map = {
    'A': 'R',
    'B': 'P',
    'C': 'S',
    'X': 'R',
    'Y': 'P',
    'Z': 'S'
}

play_score = {
    'R': 1,
    'P': 2,
    'S': 3
}

round_score = {
    'L': 0,
    'D': 3,
    'W': 6
}

def playHand(opponent, me):
    if opponent == 'R':
        if me == 'R':
            return 'D'
        elif me == 'P':
            return 'W'
        elif me == 'S':
            return 'L'
    elif opponent == 'P':
        if me == 'R':
            return 'L'
        elif me == 'P':
            return 'D'
        elif me == 'S':
            return 'W'
    elif opponent == 'S':
        if me == 'R':
            return 'W'
        elif me == 'P':
            return 'L'
        elif me == 'S':
            return 'D'

total = 0
for line in input_lines:
    opponent_encrypted = line[0]
    me_encrypted = line[2]
    opponent_un_encrypted = hand_map[opponent_encrypted]
    me_un_encrypted = hand_map[me_encrypted]
    result = playHand(opponent_un_encrypted, me_un_encrypted)
    total += round_score[result] + play_score[me_un_encrypted]

print(f"total score: {total}")

#part 2
result_map = {
    'X': 'L',
    'Y': 'D',
    'Z': 'W'
}
def getHand(opponent, result):
    if opponent == 'R':
        if result == 'D':
            return 'R'
        elif result == 'W':
            return 'P'
        elif result == 'L':
            return 'S'
    elif opponent == 'P':
        if result == 'L':
            return 'R'
        elif result == 'D':
            return 'P'
        elif result == 'W':
            return 'S'
    elif opponent == 'S':
        if result == 'W':
            return 'R'
        elif result == 'L':
            return 'P'
        elif result == 'D':
            return 'S'

total_2 = 0
for line in input_lines:
    opponent_encrypted = line[0]
    result_encrypted = line[2]
    opponent_un_encrypted = hand_map[opponent_encrypted]
    result__un_encrypted = result_map[result_encrypted]
    my_hand = getHand(opponent_un_encrypted, result__un_encrypted)
    total_2 += round_score[result__un_encrypted] + play_score[my_hand]

print(f"total score: {total_2}")