from pathlib import Path
import re

with open(Path(__file__).parent / "../inputs/day03.txt") as file:
    lines = file.read().splitlines()

# lines = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))""".splitlines()
# lines = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))""".splitlines()


muls = []
for line in lines:
    muls.extend(re.findall(r"(mul\(([0-9]{1,3}),([0-9]{1,3})\)|do\(\)|don\'t\(\))", line))

print(muls)
result1 = 0
result2 = 0
doing = True
for mul in muls:
    if mul[0][0:3] == "do(":
        doing = True
        continue
    elif mul[0][0:3] == "mul":
        if doing: result2 += int(mul[1])*int(mul[2])
        result1 += int(mul[1])*int(mul[2])
    elif mul[0][0:3] == "don":
        doing = False
    
print(result1)
print(result2)
