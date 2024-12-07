from pathlib import Path
import time

with open(Path(__file__).parent / "../inputs/day07.txt") as file:
    lines = file.read().splitlines()

# lines = """190: 10 19
# 3267: 81 40 27
# 83: 17 5
# 156: 15 6
# 7290: 6 8 6 15
# 161011: 16 10 13
# 192: 17 8 14
# 21037: 9 7 18 13
# 292: 11 6 16 20""".splitlines()

def parse_line(line):
    line = line.split(": ")
    return int(line[0]), list(map(int,line[1].split(" ")))


def try_line1(line):
    target, operands = parse_line(line)
    outcomes = {target}
    for i in reversed(range(len(operands))):
        operand = operands[i]
        new_outcomes = set()
        for outcome in outcomes:
            if operand <= outcome:
                new_outcomes.add(outcome - operand)
            if outcome%operand == 0:
                new_outcomes.add(outcome // operand)
        if len(new_outcomes) == 0:
            return 0
        outcomes = new_outcomes.copy()
    if 0 in outcomes:
        return target
    return 0



def try_line2(line):
    target, operands = parse_line(line)
    outcomes = {target}
    for i in reversed(range(len(operands))):
        operand = operands[i]
        new_outcomes = set()
        for outcome in outcomes:
            if operand <= outcome:
                new_outcomes.add(outcome - operand)
            if outcome%operand == 0:
                new_outcomes.add(outcome // operand)
            if (outcome-operand)%(10**len(str(operand))) == 0:
                new_outcomes.add((outcome-operand)//(10**len(str(operand))))
        if len(new_outcomes) == 0:
            return 0
        outcomes = new_outcomes.copy()
    if 0 in outcomes:
        return target
    return 0

start = time.time()
result1 = 0
result2 = 0
for line in lines:
    result1 += try_line1(line)
    result2 += try_line2(line)
end = time.time()
    

print(result1)
print(result2)
print(end-start)


