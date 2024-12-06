from pathlib import Path
import time

with open(Path(__file__).parent / "../inputs/day06.txt") as file:
    lines = file.read().splitlines()

# lines = """....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#..^.....
# ........#.
# #.........
# ......#...""".splitlines()

def is_OOB(position):
    return not ((0 <= position[0] < rows) and (0 <= position[1] < cols))

offsets = {"<":( 0,-1),
           "^":(-1, 0),
           ">":( 0, 1),
           "v":( 1, 0)}

turn_right = {( 0,-1):(-1, 0),
               (-1, 0):( 0, 1),
               ( 0, 1):( 1, 0),
               ( 1, 0):( 0,-1)}

# guard = [(row,col),(headingrow,headingcol)]
BORDER = 0
CLEAR = 1
OBSTACLE = 2
def thing_at_position(position):
    # next_position = (guard[0][0] + guard[1][0],guard[0][1] + guard[1][1])
    if is_OOB(position):
        return BORDER
    if position in obstacles:
        return OBSTACLE
    return CLEAR

def do_guard_step(guard):
    next_position = (guard[0][0] + guard[1][0],guard[0][1] + guard[1][1])
    next_thing = thing_at_position(next_position)
    if next_thing == BORDER: return False
    elif next_thing == CLEAR:
        guard[0] = next_position
    elif next_thing == OBSTACLE:
        guard[1] = turn_right[guard[1]]
    return True

def does_guard_loop(starting_guard):
    guard = starting_guard.copy()
    guard2 = starting_guard.copy()
    while True:
        if not do_guard_step(guard2): return False
        if not do_guard_step(guard2): return False
        do_guard_step(guard)
        if guard == guard2:
            return True

obstacles = set()
rows = len(lines)
cols = len(lines[0])
# Initial map parse
for row in range(rows):
    for col in range(cols):
        thing = lines[row][col]
        if thing == "#":
            obstacles.add((row,col))
        elif thing in "^>v<":
            starting_guard = [(row,col),offsets[thing]]

visited = set()
guard = starting_guard.copy()
start = time.time()
while True:
    visited.add(guard[0])
    if not do_guard_step(guard):
        break    
    # input(guard)
end = time.time()
result1 = len(visited)
print(result1,end-start)

result2 = 0
counter = 0

start = time.time()
visited.remove(starting_guard[0])
for visit in visited:
    obstacles.add(visit)
    if does_guard_loop(starting_guard):
        result2 += 1
    counter += 1
    obstacles.remove(visit)
    # print(counter,end-start)
end = time.time()

print(result2,end-start)