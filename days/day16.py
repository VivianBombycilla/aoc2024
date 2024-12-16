from pathlib import Path
from collections import namedtuple, Counter
import time

# start=time.time()
with open(Path(__file__).parent / "../inputs/day16.txt") as file:
    lines = file.read().splitlines()

# lines = """###############
# #.......#....E#
# #.#.###.#.###.#
# #.....#.#...#.#
# #.###.#####.#.#
# #.#.#.......#.#
# #.#.#####.###.#
# #...........#.#
# ###.#.#####.#.#
# #...#.....#.#.#
# #.#.#.###.#.#.#
# #.....#...#.#.#
# #.###.#.#.#.#.#
# #S..#.....#...#
# ###############""".splitlines()

rows = len(lines)
cols = len(lines[0])

ReindeerState = namedtuple("ReindeerState",["position","direction"])

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

class Maze:
    def __init__(self,start_states,end_states):
        self.new_states = start_states
        self.costs = {}
        for start_state in start_states:
            self.costs[start_state] = 0
        self.end_states = end_states
    def analyze_new_state(self):
        state = self.new_states.pop()
        position,direction = state
        cost = self.costs[state]
        # print("analysing state:",state)
        # print("current cost:",cost)
        ### Try moving 1 in front
        next_pos = step_position(state)
        if item(next_pos) != "#":
            self.try_add_state(ReindeerState(next_pos,direction),cost+1)
        ### Try turning
        for new_direction in DIRECTIONTURNS[direction]:
            self.try_add_state(ReindeerState(position,new_direction),cost+1000)
    def try_add_state(self,state,cost):
        # print("trying to add state:",state)
        # print("with cost:",cost)
        if (state in self.costs):
            # print("state reached already, with cost:",costs[state])
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
        

# costs = dict()
# old_states = set()
# new_states = set()

def initialize_state():
    for row in range(rows):
        for col in range(cols):
            if lines[row][col] == "S":
                start_pos = (row,col)
            elif lines[row][col] == "E":
                end_pos = (row,col)
    return start_pos,end_pos

def item(position):
    return lines[position[0]][position[1]]

def step_position(state):
    position = state.position
    direction = state.direction
    return (position[0]+direction[0],position[1]+direction[1])

def all_direction_states(pos):
    states = set()
    for direction in DIRECTIONS:
        states.add(ReindeerState(pos,direction))
    return states

start_pos,end_pos = initialize_state()
maze1 = Maze({ReindeerState(start_pos,EAST)},all_direction_states(end_pos))
maze1.fully_explore_maze()
# print(costs)
# print(new_states)
# print(rows*cols)
# while len(maze1.new_states) > 0:
#     maze1.analyze_new_state()
    # # print("costs:",costs)
    # print("#costs:",len(costs))
    # # print("new states:",new_states)
    # print("#new states:",len(new_states))
    # input()

result1 = 0
end_costs1 = {}
for end_state in maze1.end_states:
    end_costs1[end_state] = maze1.costs[end_state]
result1 = end_costs1[min(end_costs1)]
print(result1)
least_cost_states1 = set()
for end_state in maze1.end_states:
    if end_costs1[end_state] == result1:
        least_cost_states1.add(end_state)

start_states2 = set()
for least_cost_state1 in least_cost_states1:
    position,direction = least_cost_state1
    start_states2.add(ReindeerState(position,DIRECTIONFLIPS[direction]))
maze2 = Maze(start_states2,ReindeerState(start_pos,WEST))
maze2.fully_explore_maze()

good_spots = set()
for state in maze1.costs:
    position,direction = state
    flipped_state = ReindeerState(position,DIRECTIONFLIPS[direction])
    total_cost = maze1.costs[state] + maze2.costs[flipped_state]
    if total_cost == result1:
        good_spots.add(position)


result2 = len(good_spots)
print(result2)