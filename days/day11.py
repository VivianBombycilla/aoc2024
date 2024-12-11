from pathlib import Path
from collections import Counter
import time

start=time.time()
with open(Path(__file__).parent / "../inputs/day11e.txt") as file:
    lines = file.read().splitlines()

# lines = """125 17""".splitlines()

def num_digits(n):
    return len(str(n))

def split_num_by_digits(n):
    string = str(n)
    length = len(string)
    return int(string[:length//2]),int(string[length//2:])

line = list(map(int,lines[0].split(" ")))

counts = Counter(line)
# print(counts)
for i in range(75):
    new_counts = Counter()
    for rock in list(counts):
        digits = num_digits(rock)
        if rock == 0:
            new_counts[1] += counts[0]
        elif digits % 2 == 1:
            new_counts[rock*2024] += counts[rock]
        else:
            new_rocks = split_num_by_digits(rock)
            for new_rock in new_rocks:
                new_counts[new_rock] += counts[rock]
    counts = new_counts
    # print(i,counts)
    if i == 24:
        result1 = counts.total()
        
    if i == 74:
        result2 = counts.total()            
print(result1)
print(result2)