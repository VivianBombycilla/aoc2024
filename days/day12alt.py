
from pathlib import Path
from collections import Counter
import time

start=time.time()
with open(Path(__file__).parent / "../inputs/day12.txt") as file:
    lines = file.read().splitlines()


class UnionFind:
    def __init__(self,id):
        self.parent = self
        self.size = 1
        self.id = id
    def root(self):
        if self.parent == self.parent.parent: return self.parent
        self.parent = self.parent.parent
        return self.root() # collapse?
    def merge_with(self,other):
        self_root = self.root()
        other_root = other.root()
        if (self_root == other_root): return
        if self_root.size < other_root.size:
            self_root.merge_into(other_root)
        else:
            other_root.merge_into(self_root)
    def merge_into(self,other):
        self.parent = other
        other.size += self.size
    def is_head(self):
        return self.parent == self


class GardenPlot(UnionFind):
    def __init__(self,id):
        self.parent = self
        self.size = 1
        self.id = id
        self.perimeter = perim_contribution(id)
        self.corners = corner_contribution(id)
    def merge_into(self,other):
        self.parent = other
        other.size += self.size
        other.perimeter += self.perimeter
        other.corners += self.corners
    
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
    corner_values = [0,0,0,0]
    poss_nbrs = [(position[0]-1,position[1]+0),
                 (position[0]+0,position[1]+1),
                 (position[0]+1,position[1]+0),
                 (position[0]+0,position[1]-1)]
    pos_item = item(position)
    for i in range(4):
        poss_nbr = poss_nbrs[i]
        if not is_OOB(poss_nbr):
            if item(poss_nbr) == pos_item:
                corner_values[i] += 1
                corner_values[(i+1)%4] += 1
    poss_corner_nbrs = [(position[0]-1,position[1]-1),
                        (position[0]-1,position[1]+1),
                        (position[0]+1,position[1]+1),
                        (position[0]+1,position[1]-1)]
    for i in range(4):
        if corner_values[i] < 2:
            contribution += 1-corner_values[i]
            continue
        poss_corner_nbr = poss_corner_nbrs[i]
        if not is_OOB(poss_corner_nbr):
            if not(item(poss_corner_nbr) == pos_item):
                contribution += 1
    return contribution

plot = [[GardenPlot((row,col)) for col in range(cols)]  for row in range(rows)]

for row in range(rows):
    for col in range(cols):
        position = (row,col)
        pos_item = item(position)
        for nbr in down_right_nbrs(position):
            if item(nbr) == pos_item:
                plot[row][col].merge_with(plot[nbr[0]][nbr[1]])

result1 = 0
result2 = 0
for row in range(rows):
    for col in range(cols):
        obj = plot[row][col]
        if obj.is_head():
            # print(obj.id,obj.size,obj.perimeter,obj.corners)
            result1 += obj.size*obj.perimeter
            result2 += obj.size*obj.corners
end=time.time()
print(result1)
print(result2)
print(end-start)