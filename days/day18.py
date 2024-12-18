from pathlib import Path
from collections import namedtuple, Counter
import time

start=time.time()
with open(Path(__file__).parent / "../inputs/day18.txt") as file:
    lines = file.read().splitlines()

rows = 71
cols = 71
bytes_to_fall = 1024

# lines = """5,4
# 4,2
# 4,5
# 3,0
# 2,1
# 6,3
# 2,4
# 1,5
# 0,6
# 3,3
# 2,6
# 5,1
# 1,2
# 5,5
# 2,5
# 6,5
# 1,4
# 0,4
# 6,4
# 1,1
# 6,1
# 1,0
# 0,5
# 1,6
# 2,0""".splitlines()
# rows = 7
# cols = 7
# bytes_to_fall = 12

### START OF SOLUTION
NORTH = (-1, 0)
SOUTH = ( 1, 0)
EAST  = ( 0, 1)
WEST  = ( 0,-1)
DIRECTIONS = {NORTH,SOUTH,EAST,WEST}
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

MazeState = namedtuple("MazeState",["position","direction"])
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

def display_maze(maze):
    for row in range(len(maze)):
        print("".join(map(str,maze[row])))

maze = [["." for col in range(cols)] for row in range(rows)]

for i in range(bytes_to_fall):
    x,y = (int(x) for x in lines[i].split(","))
    maze[y][x] = "#"
    # display_maze(maze)
    # input()

maze1 = BasicMaze(maze,(0,0),(rows-1,cols-1))
maze1.fully_explore_maze()
result1 = maze1.costs[(rows-1,cols-1)]
end1 = time.time()
print(result1)
for i in range(bytes_to_fall,len(lines)):
    x,y = (int(x) for x in lines[i].split(","))
    maze[y][x] = "#"
    maze1 = BasicMaze(maze,(0,0),(rows-1,cols-1))
    # display_maze(maze1.maze)
    # input()
    maze1.fully_explore_maze()
    if not ((rows-1,cols-1) in maze1.costs):
        result2 = (f"{x},{y}")
        break
    # print(i)
end2 = time.time()
print(result2)
print(end1-start,end2-start)
# print(maze1.costs)
# display_maze(maze)