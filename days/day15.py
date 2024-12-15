from pathlib import Path
from collections import namedtuple, Counter
import time

# start=time.time()
with open(Path(__file__).parent / "../inputs/day15.txt") as file:
    lines = file.read().splitlines()

# lines = """########
# #..O.O.#
# ##@.O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########

# <^^>>>vv<v>>v<<""".splitlines()
# lines = """##########
# #..O..O.O#
# #......O.#
# #.OO..O.O#
# #..O@..O.#
# #O#..O...#
# #O..O..O.#
# #.OO.O.OO#
# #....O...#
# ##########

# <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
# vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
# ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
# <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
# ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
# ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
# >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
# <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
# ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
# v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^""".splitlines()

MAP2_TRANSLATION = {
    "#":["#","#"],
    "O":["[","]"],
    ".":[".","."],
    "@":["@","."]
}

map1 = lines.copy()
# print(lines)
for i in range(len(map1)):
    if map1[i] == "":
        rows = i
cols = len(map1[0])

map1 = list(map(list,map1))
# print(lines)
def expand_map(lines):
    new_map = []
    for i in range(rows):
        new_line = []
        for c in lines[i]:
            new_line.extend(MAP2_TRANSLATION[c])
        new_map.append(new_line)
    return new_map

map2 = expand_map(map1)
# print(map2)

def is_OOB(position):
    return not ((0 <= position[0] < rows) and (0 <= position[1] < cols))

LEFT  = ( 0,-1)
UP    = (-1, 0)
RIGHT = ( 0, 1)
DOWN  = ( 1, 0)

DIRECTION = {
    "<": LEFT,
    "^": UP,
    ">": RIGHT,
    "v": DOWN
}

def add_vecs(pos,direction):
    return (pos[0]+direction[0],pos[1]+direction[1])

def add_scalar_mult(pos,direction,times):
    return (pos[0]+times*direction[0],pos[1]+times*direction[1])

def item1(pos):
    return map1[pos[0]][pos[1]]

def item2(pos):
    return map2[pos[0]][pos[1]]

for row in range(rows):
    for col in range(cols):
        thing = map1[row][col]
        if thing == "@":
            robot_pos = (row,col)
            robot_pos2 = (row,2*col)

def try_move_box(pos,direction):
    new_pos = add_vecs(pos,direction)
    new_item = item1(new_pos)
    if new_item == "#":
        return 0
    if new_item == "O":
        result = try_move_box(new_pos,direction)
        if result == 0:
            return 0
        return 1 + result
    if new_item == ".":
        return 1
    raise Exception()

def try_move_robot(direction):
    new_pos = add_vecs(robot_pos,direction)
    new_item = item1(new_pos)
    if new_item == "#":
        return robot_pos
    if new_item == "O":
        boxes_moved = try_move_box(new_pos,direction)
        if boxes_moved == 0:
            return robot_pos
        last_pos = add_scalar_mult(robot_pos,direction,boxes_moved+1)
        map1[robot_pos[0]][robot_pos[1]] = "."
        map1[new_pos[0]][new_pos[1]] = "@"
        map1[last_pos[0]][last_pos[1]] = "O"
        return new_pos
    if new_item == ".":
        map1[robot_pos[0]][robot_pos[1]] = "."
        map1[new_pos[0]][new_pos[1]] = "@"
        return new_pos

def display_map():
    for i in range(rows):
        print("".join(map1[i]))

#
# Begin part 2
#
WIDE_DIRS = {
    LEFT: [(0,-1)],
    UP: [(-1,0),(-1,1)],
    RIGHT: [(0,2)],
    DOWN: [(1,0),(1,1)]
}
# return the set of boxes that move
def can_move_box2(pos,direction):
    # print("tyring to move box at",pos)
    new_poses = list(map(lambda dir:add_vecs(pos,dir),WIDE_DIRS[direction]))
    # print("new positions:",new_poses)
    moved_boxes = {pos}
    for new_pos in new_poses:
        if new_pos in moved_boxes: continue
        new_item = item2(new_pos)
        if new_item == "#":
            return set()
        elif new_item == "[":
            boxes_moved = can_move_box2(new_pos,direction)
            if len(boxes_moved) == 0:
                return set()
            moved_boxes.update(boxes_moved)
        elif new_item == "]":
            boxes_moved = can_move_box2(add_vecs(new_pos,LEFT),direction)
            if len(boxes_moved) == 0:
                return set()
            moved_boxes.update(boxes_moved)
    return moved_boxes
def update_map2(boxes_moved,direction):
    for box_pos in boxes_moved:
        map2[box_pos[0]][box_pos[1]] = "."
        map2[box_pos[0]][box_pos[1]+1] = "."
    for box_pos in boxes_moved:
        new_box_pos = add_vecs(box_pos,direction)
        map2[new_box_pos[0]][new_box_pos[1]] = "["
        map2[new_box_pos[0]][new_box_pos[1]+1] = "]"
def try_move_robot2(direction):
    new_pos = add_vecs(robot_pos2,direction)
    new_item = item2(new_pos)
    # print(new_item)
    if new_item == "#":
        return robot_pos2
    if new_item == "[":
        boxes_moved = can_move_box2(new_pos,direction)
        if len(boxes_moved) == 0:
            return robot_pos2
        update_map2(boxes_moved,direction)
        map2[robot_pos2[0]][robot_pos2[1]] = "."
        map2[new_pos[0]][new_pos[1]] = "@"
        return new_pos
    if new_item == "]":
        boxes_moved = can_move_box2(add_vecs(new_pos,LEFT),direction)
        if len(boxes_moved) == 0:
            return robot_pos2
        update_map2(boxes_moved,direction)
        map2[robot_pos2[0]][robot_pos2[1]] = "."
        map2[new_pos[0]][new_pos[1]] = "@"
        return new_pos
    if new_item == ".":
        map2[robot_pos2[0]][robot_pos2[1]] = "."
        map2[new_pos[0]][new_pos[1]] = "@"
        return new_pos

instructions = map1[rows:]
# print(instructions)
# display_map()
for instr_line in instructions:
    for instr in instr_line:
        robot_pos = try_move_robot(DIRECTION[instr])
        # print(instr)
        # display_map()
        # input()
# display_map()
result1 = 0
for row in range(rows):
    for col in range(cols):
        thing = map1[row][col]
        if thing == "O":
            result1 += 100*row+col
print(result1)

def display_map2():
    for i in range(rows):
        print("".join(map2[i]))


# display_map2()
for instr_line in instructions:
    for instr in instr_line:
        robot_pos2 = try_move_robot2(DIRECTION[instr])
        # print(instr)
        # display_map2()
        # input()
# display_map2()

result2 = 0
for row in range(rows):
    for col in range(2*cols):
        thing = map2[row][col]
        if thing == "[":
            result2 += 100*row+col

print(result2)