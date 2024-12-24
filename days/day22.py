from pathlib import Path
from collections import namedtuple, Counter
import time

start=time.time()
with open(Path(__file__).parent / "../inputs/day22.txt") as file:
    lines = file.read().splitlines()

# lines = """1
# 2
# 3
# 2024""".splitlines()

def mix(n1,n2):
    return n1^n2
def prune(n):
    return n&(16777216-1) #n%16777216
def step1(n):
    return(prune(mix(n,n << 6)))
def step2(n):
    return(prune(mix(n,n >> 5)))
def step3(n):
    return(prune(mix(n,n << 11)))
def find_next_number(n):
    n = step1(n)
    n = step2(n)
    n = step3(n)
    return n

result1 = 0
total_bananas = Counter()
c = 0
for line in lines:
    c+=1
    if c%10 == 0:
        print(c)
    n = int(line)
    last_4_costs = []
    last_4_diffs = []
    bananas = Counter()
    tuples_found = set()
    for i in range(2001):
        cost = n%10
        last_4_costs.append(cost)
        if i > 0:
            difference = cost-last_4_costs[-2]
            last_4_diffs.append(difference)
        if i > 4:
            last_4_costs.pop(0)
            last_4_diffs.pop(0)
        if i > 3:
            tup = tuple(last_4_diffs)
            if tup not in tuples_found:
                bananas[tup] = cost
                tuples_found.add(tup)
        n = find_next_number(n)
    result1 += n
    total_bananas += bananas
print(result1)

# print(line)
# print(bananas.most_common(2))
print(total_bananas.most_common(1)[0][1])
# input()
