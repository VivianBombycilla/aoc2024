from pathlib import Path
from collections import namedtuple, Counter
import time

start=time.time()
with open(Path(__file__).parent / "../inputs/day19.txt") as file:
    lines = file.read().splitlines()

# lines = """r, wr, b, g, bwu, rb, gb, br

# brwrr
# bggr
# gbbr
# rrbgbr
# ubwu
# bwurrg
# brgr
# bbrgwb""".splitlines()

# Returns True if list1 is an initial segment of list2
def is_initial_segment(list1,list2):
    if len(list1) > len(list2): return False
    for i in range(len(list1)):
        if list1[i] != list2[i]: return False
    return True

# find possible availables quicklier by using a set?
def ways_to_make_pattern(pattern,availables):
    ways_first_n = Counter()
    ways_first_n[0] += 1
    for i in range(len(pattern)):
        if ways_first_n[i] == 0:
            continue
        for avail in availables:
            if is_initial_segment(avail,pattern[i:]):
                ways_first_n[i+len(avail)] += ways_first_n[i]
    return ways_first_n[len(pattern)]
            

availables = lines[0].split(", ")
desireds = lines[2:]
# print(availables)
# print(desireds)
result1 = 0
result2 = 0
for desired in desireds:
    ways = ways_to_make_pattern(desired,availables)
    # print(desired)
    # print(ways)
    # input()
    if ways >= 1:
        result1 += 1
        result2 += ways
end = time.time()
print(result1)
print(result2)
print(end-start)