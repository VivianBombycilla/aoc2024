from pathlib import Path
from collections import namedtuple, Counter
import time
import random

start=time.time()
with open(Path(__file__).parent / "../inputs/day25.txt") as file:
    lines = file.read().splitlines()

# lines = """#####
# .####
# .####
# .####
# .#.#.
# .#...
# .....

# #####
# ##.##
# .#.##
# ...##
# ...#.
# ...#.
# .....

# .....
# #....
# #....
# #...#
# #.#.#
# #.###
# #####

# .....
# .....
# #.#..
# ###..
# ###.#
# ###.#
# #####

# .....
# .....
# .....
# #....
# #.#..
# #.#.#
# #####""".splitlines()

keys = set()
locks = set()
num_schematics = (len(lines)+1)//8
for i in range(num_schematics):
    schematic = lines[i*8:i*8+7]
    # print(schematic)
    if schematic[0][0] == "#": # is lock
        pins = []
        for pin in range(5):
            for h in range(6):
                if schematic[h+1][pin] == ".":
                    break
            pins.append(h)
        locks.add(tuple(pins))
    if schematic[0][0] == ".": # is key
        pins = []
        for pin in range(5):
            for h in range(6):
                if schematic[5-h][pin] == ".":
                    break
            pins.append(h)
        keys.add(tuple(pins))
    # print("keys",keys)
    # print("keys",locks)
    # input()
def overlap(key,lock):
    for pin in range(5):
        if key[pin]+lock[pin] > 5:
            return True
    return False
result1 = 0
for key in keys:
    for lock in locks:
        if not overlap(key,lock):
            result1 += 1
print(result1)