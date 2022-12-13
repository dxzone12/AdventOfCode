import math

# Get input
input_lines = None
with open("input.txt", "r") as input_file:
    input_lines = input_file.read().splitlines()

# Extract monkeys
class Monkey:
    Items = []
    Operation = ""
    DivisibleBy = 0
    TrueTarget = -10
    FalseTarget = -10
    Inspections = 0

    def __str__(self):
        return f"Items: {self.Items}, Operation: {self.Operation}, DivisibleBy: {self.DivisibleBy}, TrueTarget: {self.TrueTarget}, FalseTarget: {self.FalseTarget}"
    def __repr__(self):
        return str(self)

monkeys: list[Monkey] = []
i = 0
while i < len(input_lines):
    monkey = Monkey()
    i += 1 # skip over monkey number line
    monkey.Items = [int(x) for x in input_lines[i].replace("  Starting items:", "").replace(" ", "").split(",")]
    i += 1
    monkey.Operation = input_lines[i].replace("  Operation: new = ", "")
    i += 1
    monkey.DivisibleBy = int(input_lines[i].replace("  Test: divisible by ", ""))
    i += 1
    monkey.TrueTarget = int(input_lines[i].replace("    If true: throw to monkey ", ""))
    i += 1
    monkey.FalseTarget = int(input_lines[i].replace("    If false: throw to monkey ", ""))
    i += 2
    monkeys.append(monkey)

# Part 1
for round in range(0, 20):
    for monkey in monkeys:
        for i in range(0, len(monkey.Items)):
            monkey.Inspections += 1
            item = monkey.Items.pop(0)
            item = eval(monkey.Operation.replace("old", str(item)))
            item = item // 3
            if (item % monkey.DivisibleBy) == 0:
                monkeys[monkey.TrueTarget].Items.append(item)
            else:
                monkeys[monkey.FalseTarget].Items.append(item)

monkeys_by_activity = sorted(monkeys, key=lambda x: x.Inspections, reverse=True)
print(f"Monkey business level after 20 rounds is: {monkeys_by_activity[0].Inspections * monkeys_by_activity[1].Inspections}")

# Part 2
monkeys.clear()
i = 0
while i < len(input_lines):
    monkey = Monkey()
    i += 1 # skip over monkey number line
    monkey.Items = [int(x) for x in input_lines[i].replace("  Starting items:", "").replace(" ", "").split(",")]
    i += 1
    monkey.Operation = input_lines[i].replace("  Operation: new = ", "")
    i += 1
    monkey.DivisibleBy = int(input_lines[i].replace("  Test: divisible by ", ""))
    i += 1
    monkey.TrueTarget = int(input_lines[i].replace("    If true: throw to monkey ", ""))
    i += 1
    monkey.FalseTarget = int(input_lines[i].replace("    If false: throw to monkey ", ""))
    i += 2
    monkeys.append(monkey)

lcm = math.lcm(*[monkey.DivisibleBy for monkey in monkeys])
print(f"The lcm is: {lcm}")
for round in range(0, 10000):
    for monkey in monkeys:
        for i in range(0, len(monkey.Items)):
            monkey.Inspections += 1
            item = monkey.Items.pop(0)
            item = item - (lcm * (item // lcm))
            item = eval(monkey.Operation.replace("old", str(item)))
            if (item % monkey.DivisibleBy) == 0:
                monkeys[monkey.TrueTarget].Items.append(item)
            else:
                monkeys[monkey.FalseTarget].Items.append(item)
monkeys_by_activity = sorted(monkeys, key=lambda x: x.Inspections, reverse=True)
print(f"Monkey business level after 10000 rounds is: {monkeys_by_activity[0].Inspections * monkeys_by_activity[1].Inspections}")