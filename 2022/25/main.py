# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

# Part 1
def SnafuToDecimal(snafunum: str):
    decimal_num = 0
    for index, digit in enumerate(reversed(snafunum)):
        multiple = None
        match digit:
            case "-":
                multiple = -1
            case "=":
                multiple = -2
            case _:
                multiple = int(digit)
        decimal_num += multiple * pow(5, index)
    return decimal_num

def maxPossibleWithBits(num_bits: int):
    return pow(5, num_bits) // 2

def decimalToSnafu(decimal_num: int):
    # Find needed bits
    needed_bits = 1
    while maxPossibleWithBits(needed_bits) < decimal_num:
        needed_bits += 1

    # For each bit starting at most significant figure out what value it needs
    # It should get a value so the absolute difference between the num so far and the target num
    # Is less than the max possible with the remaining bits
    snafu_num_as_list = ['0' for __ in range(0, needed_bits)]
    for i in range(0, needed_bits):
        for j in range(-2, 3):
            if j == -2:
                snafu_num_as_list[i] = "="
            elif j == -1:
                snafu_num_as_list[i] = "-"
            else:
                snafu_num_as_list[i] = str(j)

            num_so_far = SnafuToDecimal(''.join(snafu_num_as_list))
            
            if num_so_far == decimal_num:
                return ''.join(snafu_num_as_list)
            elif abs(num_so_far - decimal_num) <= maxPossibleWithBits(needed_bits - 1 - i):
                break
    raise Exception("SHOULD NEVER GET HERE")
            



input_as_decimal = [SnafuToDecimal(line) for line in input_lines]
summed = sum(input_as_decimal)
print(f"The snafu number we are after is: {decimalToSnafu(summed)}")