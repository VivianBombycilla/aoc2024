from pathlib import Path
from collections import Counter
import time

start=time.time()
with open(Path(__file__).parent / "../inputs/day12.txt") as file:
    lines = file.read().splitlines()



        
# lines = """AAAA
# BBCD
# BBCC
# EEEC""".splitlines()
# lines = """OOOOO
# OXOXO
# OOOOO
# OXOXO
# OOOOO""".splitlines()
# lines = """RRRRIICCFF
# RRRRIICCCF
# VVRRRCCFFF
# VVRCCCJFFF
# VVVVCJJCFE
# VVIVCCJJEE
# VVIIICJJEE
# MIIIIIJJEE
# MIIISIJEEE
# MMMISSJEEE""".splitlines()
# lines = """ABB
# AAA
# ABA""".splitlines()

rows = len(lines)
cols = len(lines[0])

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

def down_right_nbrs(position):
    nbrs = set()
    poss_nbrs = [(position[0]+1,position[1]+0),
                 (position[0]+0,position[1]+1)]
    for poss_nbr in poss_nbrs:
        if not is_OOB(poss_nbr):
            nbrs.add(poss_nbr)
    return nbrs

def item(position):
    return lines[position[0]][position[1]]

def perim_contribution(position):
    contribution = 4
    nbrs = grid_nbrs(position)
    for nbr in nbrs:
        if item(nbr) == item(position):
            contribution -= 1
    return contribution

# 0     0     1
#    0 --- 1
# 3  |     |  1
#    3 --- 2
# 3     2     2
def corner_contribution(position):
    contribution = 0
    corners = [0,0,0,0]
    poss_nbrs = [(position[0]-1,position[1]+0),
                 (position[0]+0,position[1]+1),
                 (position[0]+1,position[1]+0),
                 (position[0]+0,position[1]-1)]
    pos_item = item(position)
    for i in range(4):
        poss_nbr = poss_nbrs[i]
        if not is_OOB(poss_nbr):
            if item(poss_nbr) == pos_item:
                corners[i] += 1
                corners[(i+1)%4] += 1
    poss_corner_nbrs = [(position[0]-1,position[1]-1),
                        (position[0]-1,position[1]+1),
                        (position[0]+1,position[1]+1),
                        (position[0]+1,position[1]-1)]
    for i in range(4):
        if corners[i] < 2:
            contribution += 1-corners[i]
            continue
        poss_corner_nbr = poss_corner_nbrs[i]
        if not is_OOB(poss_corner_nbr):
            if not(item(poss_corner_nbr) == pos_item):
                contribution += 1
    # print(position,corners,contribution)
    return contribution

plot_reps = [[(row,col) for col in range(cols)]  for row in range(rows)]
perims = [[perim_contribution((row,col)) for col in range(cols)] for row in range(rows)]
corners = [[corner_contribution((row,col)) for col in range(cols)] for row in range(rows)]
tree_sizes = [[1 for col in range(cols)] for row in range(rows)]

def find_rep(position): # add collapsing
    parent = plot_reps[position[0]][position[1]]
    while position != parent:
        position = parent
        parent = plot_reps[position[0]][position[1]]
    return position

def try_join(pos1,pos2):
    if not (item(pos1) == item(pos2)): return
    pos1 = find_rep(pos1)
    pos2 = find_rep(pos2)
    if pos1 == pos2: return
    if tree_sizes[pos1[0]][pos1[1]] >= tree_sizes[pos2[0]][pos2[1]]:
        plot_reps[pos2[0]][pos2[1]] = pos1
        tree_sizes[pos1[0]][pos1[1]] += tree_sizes[pos2[0]][pos2[1]]
        perims[pos1[0]][pos1[1]] += perims[pos2[0]][pos2[1]]
        corners[pos1[0]][pos1[1]] += corners[pos2[0]][pos2[1]]
    else:
        plot_reps[pos1[0]][pos1[1]] = pos2
        tree_sizes[pos2[0]][pos2[1]] += tree_sizes[pos1[0]][pos1[1]]
        perims[pos2[0]][pos2[1]] += perims[pos1[0]][pos1[1]]
        corners[pos2[0]][pos2[1]] += corners[pos1[0]][pos1[1]]

print(plot_reps)
print(tree_sizes)
print(perims)
print(corners)
for row in range(rows):
    for col in range(cols):
        position = (row,col)
        for nbr in down_right_nbrs(position):
            try_join(position,nbr)

# print(plot_reps)
# print(tree_sizes)
# print(perims)
# print(corners)
result1 = 0
result2 = 0
for row in range(rows):
    for col in range(cols):
        position = (row,col)
        if plot_reps[row][col] == position:
            print(item(position),position,tree_sizes[row][col],perims[row][col],corners[row][col])
            result1 += tree_sizes[row][col]*perims[row][col]
            result2 += tree_sizes[row][col]*corners[row][col]
print(result1)
print(result2)