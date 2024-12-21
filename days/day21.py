from pathlib import Path
from collections import namedtuple, Counter
import time

start=time.time()
with open(Path(__file__).parent / "../inputs/day21.txt") as file:
    lines = file.read().splitlines()

# lines = """029A
# 980A
# 179A
# 456A
# 379A""".splitlines()


NORTH = (-1, 0)
SOUTH = ( 1, 0)
EAST  = ( 0, 1)
WEST  = ( 0,-1)
UP    = NORTH
DOWN  = SOUTH
LEFT  = WEST
RIGHT = EAST
DIRECTIONS = {NORTH,SOUTH,EAST,WEST}
DIRECTIONFLIPS = {
    EAST:   WEST,
    SOUTH: NORTH,
    WEST:   EAST,
    NORTH: SOUTH
}
DIRECTIONARROWS = {
    NORTH: "^",
    SOUTH: "v",
    EAST:  ">",
    WEST:  "<"
}

# (row,col)
KEYPADNUM = {
    "7":(0,0), "8":(0,1), "9":(0,2),
    "4":(1,0), "5":(1,1), "6":(1,2),
    "1":(2,0), "2":(2,1), "3":(2,2),
               "0":(3,1), "A":(3,2),
}
KEYPADARROWS = {
               "^":(0,1), "A":(0,2),
    "<":(1,0), "v":(1,1), ">":(1,2)
}
def element(s):
    for e in s:
        break
    return e

class Keypad:
    def __init__(self,codes_to_pos):
        self.c2p = codes_to_pos
        self.codes = set(self.c2p.keys())
        self.p2c = {}
        for code in self.codes:
            self.p2c[codes_to_pos[code]] = code
        self.posns = set(self.p2c.keys())
        self.paths,self.short_paths = self.generate_paths_dict()
    def generate_paths_dict(self):
        paths = {"A"}
        short_paths = {}
        for end_pos in self.posns:
            new_paths = [(end_pos,{""},{UP,DOWN,RIGHT,LEFT})]
            short_paths[self.p2c[end_pos]+self.p2c[end_pos]] = {"A"}
            while True:
                old_pos,old_2_end_paths,valid_directions = new_paths.pop()
                for direction in valid_directions:
                    new_pos = (old_pos[0] + direction[0],
                               old_pos[1] + direction[1])
                    if new_pos not in self.posns: continue
                    new_arrow = DIRECTIONARROWS[DIRECTIONFLIPS[direction]]
                    new_2_end_paths = set(map(lambda old_path:new_arrow + old_path,old_2_end_paths))
                    new_valid_dirs = valid_directions.difference({DIRECTIONFLIPS[direction]})
                    new_paths.append((new_pos,new_2_end_paths,new_valid_dirs))
                    new_2_end_code = self.p2c[new_pos]+self.p2c[end_pos]
                    if new_2_end_code not in short_paths:
                        short_paths[new_2_end_code] = set()
                    paths_to_add = set(map(lambda path:path+"A",new_2_end_paths))
                    short_paths[new_2_end_code].update(paths_to_add)
                    paths.update(paths_to_add)
                if len(new_paths) == 0:
                    break
        return paths,short_paths
    def find_all_short_paths(self,output):
        # go from A to first thing
        # print("output",output)
        ways = [Counter()]
        new_output = "A"+output
        # ways = self.short_paths["A"+output[0]]
        # print("ways",ways)
        for i in range(len(output)):
            step = new_output[i]+new_output[i+1]
            new_ways = list()
            # print(self.short_paths)
            for way in ways:
                for next_steps in self.short_paths[step]:
                    new_way = way.copy()
                    new_way[next_steps] += 1
                    new_ways.append(new_way)
            ways = new_ways.copy()
            # print("ways",ways)
        return ways
    def find_all_short_paths(self,output):
        # go from A to first thing
        # print("output",output)
        ways = [Counter()]
        new_output = "A"+output
        # ways = self.short_paths["A"+output[0]]
        # print("ways",ways)
        for i in range(len(output)):
            step = new_output[i]+new_output[i+1]
            new_ways = list()
            # print(self.short_paths)
            for way in ways:
                for next_steps in self.short_paths[step]:
                    new_way = way.copy()
                    new_way[next_steps] += 1
                    new_ways.append(new_way)
            ways = new_ways.copy()
            # print("ways",ways)
        return ways
    
    






def concatenate(instruction_counter):
    return "".join(instruction_counter.elements())
def total_length(instruction_counter):
    length = 0
    for instruction in instruction_counter:
        length += len(instruction)*instruction_counter[instruction]
    return length
def total_cost(instruction_counter):
    cost = 0
    for instruction in instruction_counter:
        cost += arrpad_costs[instruction]*instruction_counter[instruction]
    return cost

numpad = Keypad(KEYPADNUM)
arrpad = Keypad(KEYPADARROWS)

###
arrpad_costs = {}
for path in numpad.paths:
    arrpad_costs[path] = total_length(arrpad.find_all_short_paths(path)[0])

def choose_best_option_BF(orig_options):
    orig_options = list(orig_options)
    options = []
    for option in orig_options:
        options.append([Counter({option:1})])
    # print(options)
    while True:
        costs = []
        # print("choosing best out of:",options)
        for i in range(len(options)):
            new_options = []
            for sub_option in options[i]:
                # print(sub_option)
                # print(concatenate(sub_option))
                
                new_options.extend(arrpad.find_all_short_paths(concatenate(sub_option)))
            # print(new_options)
            new_costs = list(map(total_cost,new_options))
            costs.append(min(new_costs))
            options[i] = new_options
        # costs = list(map(lambda option:min(map(total_cost,option)),options))
        # print(costs)
        sorted_costs = sorted(costs)
        if sorted_costs[0] < sorted_costs[1]:
            for i in range(len(options)):
                if costs[i] == sorted_costs[0]:
                    # print("best option:",orig_options[i])
                    return orig_options[i]
        # print(options)
        # input()

arrowpad_keys = {"^",">","v","<","A"}
best_steps = {}
for key1 in arrowpad_keys:
    for key2 in arrowpad_keys:
        step = key1+key2
        options = arrpad.short_paths[step]
        if len(options) == 1:
            best_steps[step] = element(options)
            continue
        best_steps[step] = choose_best_option_BF(options)

numpad_robots = {}
for path in numpad.paths:
    numpad_robots[path] = Counter()
    # go from A to first thing
    edited_path = "A"+path
    for i in range(len(path)):
        next_step = edited_path[i]+edited_path[i+1]
        # options = arrpad.short_paths[next_step]
        # print(next_step,options)
        numpad_robots[path][best_steps[next_step]] += 1
        # print(next_step,options,best_option)
    # print(path,numpad_robots[path])
    # input()
# print(numpad_robots)

def do_best_step(inst_ctr):
    counts = Counter()
    for inst in inst_ctr:
        path_ctr = numpad_robots[inst]
        for path in path_ctr.keys():
            counts[path] += path_ctr[path]*inst_ctr[inst]
    return counts
def choose_best_option_BS(orig_options):
    if len(orig_options) == 1:
        return element(orig_options)
    orig_options = list(orig_options)
    options = []
    for option in orig_options:
        options.append(Counter({option:1}))
    # print(orig_options,options)
    # print(options)
    while True:
        costs = []
        # print("choosing best out of:",options)
        for i in range(len(options)):
            new_option = do_best_step(options[i])
            new_cost = total_cost(new_option)
            costs.append(new_cost)
            options[i] = new_option
        # costs = list(map(lambda option:min(map(total_cost,option)),options))
        # print(costs)
        sorted_costs = sorted(costs)
        if sorted_costs[0] < sorted_costs[1]:
            for i in range(len(options)):
                if costs[i] == sorted_costs[0]:
                    # print("best option:",orig_options[i])
                    return orig_options[i]
        # print(options)
        # input()
def find_best_paths():
    best_paths = {}
    for key1 in numpad.codes:
        for key2 in numpad.codes:
            step = key1+key2
            options = numpad.short_paths[step]
            best_option = choose_best_option_BS(options) 
            best_paths[step] = best_option
            # print(step,options,best_option)
            # input()
            # sample_path = frozenset(element(short_paths))
            # if sample_path in checked_paths:
            #     best_paths[step] = checked_paths[sample_path]
            #     continue
    return best_paths
best_paths = find_best_paths()
# print(best_paths)
# input()
# raise Exception()

### UNCOMMENT TO SOLVE
def find_instructions(robots,inst_ctr):
    if robots == 0:
        return inst_ctr
    counts = Counter()
    # print(output)
    for key in inst_ctr.keys():
        # print(key,numpad_robots[key])
        next_counter = numpad_robots[key] 
        for path in next_counter.keys():
            counts[path] += next_counter[path]*inst_ctr[key]
    return find_instructions(robots-1,counts)

def find_least_length(robots,output):
    Aoutput = "A"+output
    counts = Counter()
    for i in range(len(output)):
        next_step = Aoutput[i]+Aoutput[i+1]
        counts[best_paths[next_step]] += 1
    # return counts
    a = find_instructions(robots,counts)
    length = 0
    for i in a.keys():
        length += len(i)*a[i]
    # print(length)
    return length


# a = find_least_length(2,"029A")
# print(a)
result1 = 0
result2 = 0
for line in lines:
    number = int(line[:3])
    length1 = find_least_length(2,line)
    length2 = find_least_length(25,line)
    result1 += number*length1
    result2 += number*length2

end = time.time()
print(result1)
print(result2)
print(end-start)
# 203595323205120
# 205511438855024
# 200382402051132
# 198466286401228