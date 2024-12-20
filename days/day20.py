from pathlib import Path
from collections import namedtuple, Counter
import time

start=time.time()
with open(Path(__file__).parent / "../inputs/day20.txt") as file:
    lines = file.read().splitlines()

# lines = """###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #######.#.#.###
# #######.#.#...#
# #######.#.###.#
# ###..E#...#...#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############""".splitlines()

### START OF SOLUTION
NORTH = (-1, 0)
SOUTH = ( 1, 0)
EAST  = ( 0, 1)
WEST  = ( 0,-1)
NORTHEAST  = (-1, 1)
SOUTHWEST  = ( 1,-1)
SOUTHEAST  = ( 1, 1)
NORTHWEST  = (-1,-1)
DIRECTIONS = {NORTH,SOUTH,EAST,WEST}
DIRECTIONS8 = {NORTH,SOUTH,EAST,WEST,NORTHEAST,SOUTHWEST,SOUTHEAST,NORTHWEST}
DIRECTIONTURNS = {
    EAST:  (SOUTH,NORTH),
    SOUTH: ( WEST, EAST),
    WEST:  (NORTH,SOUTH),
    NORTH: ( EAST, WEST)
}
DIRECTIONFLIPS = {
    EAST:   WEST,
    SOUTH: NORTH,
    WEST:   EAST,
    NORTH: SOUTH
}


# MazeState = namedtuple("MazeState",["position","direction"])
class BasicMaze:
    def __init__(self,maze,start_pos,end_pos):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.new_states = {start_pos}
        self.costs = {start_pos:0}
        # for start_state in start_pos:
        #     self.costs[start_state] = 0
        self.end_pos = end_pos
    def analyze_new_state(self):
        position = self.new_states.pop()
        cost = self.costs[position]
        # print("analysing state:",position)
        # print("current cost:",cost)
        ### Try moving 1 in front
        for direction in DIRECTIONS:
            new_pos = self.step_position(position,direction)
            # print("new_pos",new_pos)
            if (not self.is_OOB(new_pos)) and (self.item(new_pos) != "#"):
                self.try_add_state(new_pos,cost+1)
        # input()
    def try_add_state(self,state,cost):
        # print("trying to add state:",state)
        # print("with cost:",cost)
        if (state in self.costs):
            # print("state reached already, with cost:",self.costs[state])
            if (self.costs[state] <= cost):
                # print("state already achieved with lower cost")
                return
        # else:
            # print("new state!")
        self.new_states.add(state)
        self.costs[state] = cost
        # print("successfully updated state")
    def fully_explore_maze(self):
        while len(self.new_states) > 0:
            self.analyze_new_state()
    def item(self,position):
        return self.maze[position[0]][position[1]]
    def step_position(self,position,direction):
        return (position[0]+direction[0],position[1]+direction[1])
    def is_OOB(self,position):
        return not ((0 <= position[0] < self.rows) and (0 <= position[1] < self.cols))

def neighbours_of_distance(position,distance):
    pos_x,pos_y = position
    nbrs = set()
    for x in range(-distance,distance+1):
        y = abs(x) - distance
        nbrs.add((pos_x+x,pos_y+y))
        nbrs.add((pos_x+x,pos_y-y))
    return nbrs

class Day20Maze(BasicMaze):
    def count_all_shortcuts1(self):
        counts = Counter()
        for track_piece in self.costs:
            for new_pos in neighbours_of_distance(track_piece,2):
                if new_pos not in self.costs: continue
                shortcut_length = self.costs[track_piece] - (self.costs[new_pos]+2)
                if shortcut_length > 0:
                    counts[shortcut_length] += 1
            # for direction in DIRECTIONS:
                # new_pos = self.step_position(track_piece,direction)
                # new_pos = self.step_position(new_pos,direction)
                # if new_pos in self.costs:
                #     shortcut_length = self.costs[track_piece] - (self.costs[new_pos]+2)
                #     if shortcut_length > 0:
                #         counts[shortcut_length] += 1
        return counts
    def count_all_shortcuts2(self):
        counts = Counter()
        for track_piece in self.costs:
            for distance in range(2,21):
                for new_pos in neighbours_of_distance(track_piece,distance):
                    if new_pos not in self.costs: continue
                    shortcut_length = self.costs[track_piece] - (self.costs[new_pos]+distance)
                    if shortcut_length > 0:
                        counts[shortcut_length] += 1
        return counts



rows = len(lines)
cols = len(lines[0])
# maze1 = [list(lines[row]) for row in range(rows)]
# print(maze1)
for row in range(rows):
    for col in range(cols):
        if lines[row][col] == "S":
            start_pos = (row,col)
        elif lines[row][col] == "E":
            end_pos = (row,col)

maze1 = Day20Maze(lines,start_pos,end_pos)
maze1.fully_explore_maze()
shortcuts1 = maze1.count_all_shortcuts1()

result1 = 0
for key in shortcuts1.keys():
    # print(key,shortcuts1[key])
    if key >= 100:
        result1 += shortcuts1[key]
print(result1)

result2 = 0
shortcuts2 = maze1.count_all_shortcuts2()
for key in shortcuts2.keys():
    # print(key,shortcuts2[key])
    if key >= 100:
        result2 += shortcuts2[key]
end = time.time()
print(result2)
print(end-start)