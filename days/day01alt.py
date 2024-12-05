from pathlib import Path
from collections import Counter

with open(Path(__file__).parent / "../inputs/day01.txt") as file:
    lines = file.read().splitlines()

# lines = """3   4
# 4   3
# 2   5
# 1   3
# 3   9
# 3   3""".splitlines()

list1 = []
list2 = []

for i in range(len(lines)):
    entries = lines[i].split()
    list1.append(int(entries[0]))
    list2.append(int(entries[1]))

count = Counter(list2)

list1.sort()
list2.sort()

result1 = 0
result2 = 0
for i in range(len(list1)):
    result1 += abs(list1[i]-list2[i])
    result2 += list1[i]*count[list1[i]]

print(result1)
print(result2)
