from pathlib import Path
import time

start=time.time()
with open(Path(__file__).parent / "../inputs/day10.txt") as file:
    lines = file.read().splitlines()

# lines = """89010123
# 78121874
# 87430965
# 96549874
# 45678903
# 32019012
# 01329801
# 10456732""".splitlines()
# lines = """11122""".splitlines()

def is_OOB(position):
    return not ((0 <= position[0] < rows) and (0 <= position[1] < cols))

def grid_nbrs(position):
    nbrs = set()
    poss_nbrs = [(position[0]+1,position[1]+0),
                     (position[0]+0,position[1]+1),
                     (position[0]-1,position[1]+0),
                     (position[0]+0,position[1]-1)]
    for poss_nbr in poss_nbrs:
        if not is_OOB(poss_nbr):
            nbrs.add(poss_nbr)
    return nbrs

height_locs = {}
for i in range(10):
    height_locs[i] = set()

rows = len(lines)
cols = len(lines[0])


for row in range(rows):
    for col in range(cols):
        height_locs[int(lines[row][col])].add((row,col))

result1 = 0
result2 = 0
# print(height_locs)
nines_reachable = dict()
nine_paths = dict()
for loc in height_locs[9]:
    nines_reachable[loc] = {loc}
    nine_paths[loc] = 1
for height in reversed(range(9)):
    for loc in height_locs[height]:
        nines_reachable[loc] = set()
        nine_paths[loc] = 0
        for nbr in grid_nbrs(loc):
            if nbr in height_locs[height+1]:
                # print(loc,nbr)
                nines_reachable[loc].update(nines_reachable[nbr])
                nine_paths[loc] +=  nine_paths[nbr]
        if height == 0:
            # print(loc,nines_reachable[loc],len(nines_reachable[loc]))
            result1 += len(nines_reachable[loc])
            result2 += nine_paths[loc]
end=time.time()
print(result1)
print(result2)
print(end-start)