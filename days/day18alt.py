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
def is_OOB(position):
    return not ((0 <= position[0] < rows) and (0 <= position[1] < cols))
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

# (rows,0) is bottom left edges
# (rows,1) is top right edges
class Day18UF(UnionFind):
    def neighbours(self):
        nbrs = set()
        if (self.id[0] == rows-1) or (self.id[1] == 0):
            nbrs.add((rows,0))
        if (self.id[0] == 0) or (self.id[1] == cols-1):
            nbrs.add((rows,1))
        for direction in DIRECTIONS8:
            new_pos = (self.id[0]+direction[0],self.id[1]+direction[1])
            if not (is_OOB(new_pos)):
                nbrs.add(new_pos)
        return nbrs
    def merge_with_wall_neighbours(self):
        for nbr in self.neighbours():
            if (nbr[0] == rows) or (maze[nbr[0]][nbr[1]] == "#"):
                self.merge_with(maze_UF[nbr[0]][nbr[1]])
            


def display_maze(maze):
    for row in range(len(maze)):
        print("".join(map(str,maze[row])))

maze = [["." for col in range(cols)] for row in range(rows)]
maze_UF = [[Day18UF((row,col)) for col in range(cols)] for row in range(rows)]
maze_UF.append([Day18UF((rows,0)),Day18UF((rows,1))])
print(len(maze_UF))

for i in range(len(lines)):
    x,y = (int(x) for x in lines[i].split(","))
    maze[y][x] = "#"
    maze_UF[y][x].merge_with_wall_neighbours()
    if i == bytes_to_fall-1:
        maze1 = BasicMaze(maze,(0,0),(rows-1,cols-1))
        maze1.fully_explore_maze()
        result1 = maze1.costs[(rows-1,cols-1)]
        end1 = time.time()
        print(result1)
    if maze_UF[rows][0].root() == maze_UF[rows][1].root():
        result2 = (f"{x},{y}")
        end2 = time.time()
        print(result2)
        break
print(end1-start)
print(end2-start)