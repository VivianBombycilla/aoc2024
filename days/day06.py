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

def guard_leaving(guard):
    heading = guard[1]
    position = guard[0]
    if heading == "<":
        return position[1] == 0
    if heading == ">":
        return position[1] == cols-1
    if heading == "^":
        return position[0] == 0
    if heading == "v":
        return position[0] == rows-1

offsets = {"<":[ 0,-1],
           "^":[-1, 0],
           ">":[ 0, 1],
           "v":[ 1, 0]}
turn_right = {"<":"^",
              "^":">",
              ">":"v",
              "v":"<"}


BORDER = 0
CLEAR = 1
OBSTACLE = 2
def thing_in_front_of_guard(guard,obstacles):
    if guard_leaving(guard):
        return BORDER
    heading = guard[1]
    position = guard[0]
    next_position = [sum(x) for x in zip(position, offsets[heading])]
    if next_position in obstacles:
        return OBSTACLE
    return CLEAR

def does_guard_loop(starting_guard,obstacles):
    guard = starting_guard.copy()
    guard2 = starting_guard.copy()
    for i in range(rows*cols*4):
        next_thing = thing_in_front_of_guard(guard,obstacles)
        if next_thing == BORDER: return False
        if next_thing == CLEAR:
            guard[0] = [guard[0][i] + offsets[guard[1]][i] for i in range(2)]
        if next_thing == OBSTACLE:
            guard[1] = turn_right[guard[1]]
        
        # Do guard2 twice
        next_thing2 = thing_in_front_of_guard(guard2,obstacles)
        if next_thing2 == BORDER: return False
        if next_thing2 == CLEAR:
            guard2[0] = [guard2[0][i] + offsets[guard2[1]][i] for i in range(2)]
        if next_thing2 == OBSTACLE:
            guard2[1] = turn_right[guard2[1]]
        next_thing2 = thing_in_front_of_guard(guard2,obstacles)
        if next_thing2 == BORDER: return False
        if next_thing2 == CLEAR:
            guard2[0] = [guard2[0][i] + offsets[guard2[1]][i] for i in range(2)]
        if next_thing2 == OBSTACLE:
            guard2[1] = turn_right[guard2[1]]
        
        if guard == guard2:
            return True
    return True

    

obstacles = []
rows = len(lines)
cols = len(lines[0])
# Initial map parse
for row in range(rows):
    for col in range(cols):
        thing = lines[row][col]
        if thing == "#":
            obstacles.append([row,col])
        elif thing in "^>v<":
            starting_guard = [[row,col],thing]

# print(obstacles)
visited = []
guard = starting_guard.copy()
start = time.time()
while True:
    if guard[0] not in visited:
        visited.append(guard[0])
    next_thing = thing_in_front_of_guard(guard,obstacles)
    if next_thing == BORDER: break
    if next_thing == CLEAR:
        guard[0] = [guard[0][i] + offsets[guard[1]][i] for i in range(2)]
    if next_thing == OBSTACLE:
        guard[1] = turn_right[guard[1]]
        
    # input(guard)
end = time.time()
result1 = len(visited)
print(result1,end-start)

result2 = 0
counter = 0

for visit in visited[1:]:
    start = time.time()
    new_obstacles = obstacles.copy()
    new_obstacles.append(visit)
    if does_guard_loop(starting_guard,new_obstacles):
        result2 += 1
    counter += 1
    end = time.time()
    print(counter,end-start)

print(result2)