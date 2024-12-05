from pathlib import Path

with open(Path(__file__).parent / "../inputs/day02.txt") as file:
    lines = file.read().splitlines()

# lines = """7 6 4 2 1
# 1 2 7 8 9
# 9 7 6 2 1
# 1 3 2 4 5
# 8 6 4 4 1
# 1 3 6 7 9""".splitlines()

def is_safe1(report):
    if report[0] > report[1]:
        report = list(reversed(report))
    for i in range(len(report)-1):
        if report[i]>=report[i+1]:
            return False
        if abs(report[i+1]-report[i])>3:
            return False
    return True

def is_safe2(report):
    if is_safe1(report): return True
    for i in range(len(report)):
        subreport = report.copy()
        del(subreport[i])
        if is_safe1(subreport): return True
    return False

result1 = 0
result2 = 0
for i in range(len(lines)):
    # line = list(map(int,lines[i].split()))
    line = [ int(x) for x in lines[i].split() ]
    if is_safe1(line):
        result1 += 1
    if is_safe2(line):
        result2 += 1
print(result1)
print(result2)