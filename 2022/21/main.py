# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()


# Part 1
class Monkey:
    def __init__(self, name, operation, monkey_map) -> None:
        self.Name = name
        self.RawOperation: str = operation
        self.LookupMap: dict[str, Monkey] = monkey_map
        self.Value = None
    
    def getValue(self):
        if self.Value is not None:
            return self.Value
        
        try:
            val = int(self.RawOperation)
            self.Value = val
            return self.Value
        except ValueError:
            pass

        # We do not have a simple number and need to work stuff out
        OPERATORS = [" + ", " - ", " * ", " / "]
        for op in OPERATORS:
            if op in self.RawOperation:
                operands = self.RawOperation.split(op)
                return eval(self.RawOperation.replace(operands[0], str(self.LookupMap[operands[0]].getValue())).replace(operands[1], str(self.LookupMap[operands[1]].getValue())))


monkey_lookup_map: dict[str, Monkey] = {}
for line in input_lines:
    name_op = line.split(": ")
    monkey_lookup_map[name_op[0]] = Monkey(name_op[0], name_op[1], monkey_lookup_map)

value_of_root = monkey_lookup_map["root"].getValue()
print(f"root is yelling: {value_of_root}")

# Part 2
root_monkey = monkey_lookup_map["root"]

# Find right operand
def dfsToHumnAndRecordOpsOnWayBack(monkey: Monkey, operations, lookup_map: dict[str, Monkey]) -> bool:
    if monkey.Name == "humn":
        return True
    
    operands = None
    operator = None
    OPERATORS = [" + ", " - ", " * ", " / "]
    for op in OPERATORS:
        if op in monkey.RawOperation:
            operands = monkey.RawOperation.split(op)
            operator = op
            break
    
    if operands is None:
        return False

    # Check left path
    if dfsToHumnAndRecordOpsOnWayBack(lookup_map[operands[0]], operations, lookup_map):
        operations.append((operator, True, lookup_map[operands[1]].getValue(), monkey.RawOperation))
        return True
    # Check right path
    if dfsToHumnAndRecordOpsOnWayBack(lookup_map[operands[1]], operations, lookup_map):
        operations.append((operator, False, lookup_map[operands[0]].getValue(), monkey.RawOperation))
        return True
    return False

def applyInvertedOp(op_description, target_val):
    # Plus
    if op_description[0] == " + ":
        return target - op_description[2]
    # Multiply
    if op_description[0] == " * ":
        return target / op_description[2]
    # Minus
    if op_description[0] == " - ":
        if op_description[1]:
            # we were left
            return target + op_description[2]
        else:
            # we were right
            return op_description[2] - target
    # Divide
    if op_description[0] == " / ":
        if op_description[1]:
            # we were left
            return target * op_description[2]
        else:
            # we were right
            return op_description[2] / target

    raise Exception("NOT GOOD")

# Find the target value
right_val = None
left_monkey_name = None
OPERATORS = [" + ", " - ", " * ", " / "]
for op in OPERATORS:
    if op in root_monkey.RawOperation:
        operands = root_monkey.RawOperation.split(op)
        right_val = monkey_lookup_map[operands[1]].getValue()
        left_monkey_name = operands[0]
        break

# Find all the operations needed to get to humn
operations_to_humn = []
dfsToHumnAndRecordOpsOnWayBack(monkey_lookup_map[left_monkey_name], operations_to_humn, monkey_lookup_map)

# undo each operator against target 
target = right_val
while len(operations_to_humn) > 0:
    next_op_desc = operations_to_humn.pop()
    target = applyInvertedOp(next_op_desc, target)

print(f"We need to yell: {target}")