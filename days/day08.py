from pathlib import Path
import time

with open(Path(__file__).parent / "../inputs/day08.txt") as file:
    lines = file.read().splitlines()

# lines = """............
# ........0...
# .....0......
# .......0....
# ....0.......
# ......A.....
# ............
# ............
# ........A...
# .........A..
# ............
# ............""".splitlines()

# lines = """T.........
# ...T......
# .T........
# ..........
# ..........
# ..........
# ..........
# ..........
# ..........
# ..........""".splitlines()

def is_OOB(position):
    return not ((0 <= position[0] < rows) and (0 <= position[1] < cols))

def all_valid_antinodes(node1,node2):
    i = 0
    valid_antinodes = set()
    while True:
        antinode = ((i+1)*coord1[0]-i*coord2[0],(i+1)*coord1[1]-i*coord2[1])
        i += 1
        if not is_OOB(antinode):
            valid_antinodes.add(antinode)
        else: break
    i = 0
    while True:
        antinode = ((i+1)*coord2[0]-i*coord1[0],(i+1)*coord2[1]-i*coord1[1])
        i += 1
        if not is_OOB(antinode):
            valid_antinodes.add(antinode)
        else: break
    return valid_antinodes

start = time.time()
rows = len(lines)
cols = len(lines[0])
coords = {}
for row in range(rows):
    for col in range(cols):
        thing = lines[row][col]
        if (thing == "."): continue
        if thing in coords:
            coords[thing].append((row,col))
        else:
            coords[thing] = [(row,col)]

antinodes1 = set()
antinodes2 = set()
for antenna_type in coords:
    type_coords = coords[antenna_type]
    for i in range(len(type_coords)):
        coord1 = type_coords[i]
        for j in range(i+1,len(type_coords)):
            coord2 = type_coords[j]
            new_AN1 = (2*coord1[0]-coord2[0],2*coord1[1]-coord2[1])
            new_AN2 = (2*coord2[0]-coord1[0],2*coord2[1]-coord1[1])
            if not is_OOB(new_AN1):
                antinodes1.add(new_AN1)
            if not is_OOB(new_AN2):
                antinodes1.add(new_AN2)
            antinodes2.update(all_valid_antinodes(coord1,coord2))
            # print(antinodes2)
end = time.time()
result1 = len(antinodes1)
result2 = len(antinodes2)
print(result1)
print(result2)
print(end-start)