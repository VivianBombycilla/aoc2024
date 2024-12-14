from pathlib import Path
from collections import namedtuple, Counter
import time

start=time.time()
with open(Path(__file__).parent / "../inputs/day14.txt") as file:
    lines = file.read().splitlines()
map_width = 101
map_height = 103

# lines = """p=0,4 v=3,-3
# p=6,3 v=-1,-3
# p=10,3 v=-1,2
# p=2,0 v=2,-1
# p=0,0 v=1,3
# p=3,0 v=-2,-2
# p=7,6 v=-1,-3
# p=3,0 v=-1,-2
# p=9,3 v=2,3
# p=7,3 v=-1,2
# p=2,4 v=2,-3
# p=9,5 v=-3,-3""".splitlines()
# map_width = 11
# map_height = 7

Vector = namedtuple("Vector",("x","y"))
class Robot:
    def __init__(self,pos,vel):
        self.pos = Vector(pos[0],pos[1])
        self.vel = Vector(vel[0],vel[1])
    def increment(self):
        self.pos = Vector((self.pos.x+self.vel.x)%map_width,
                          (self.pos.y+self.vel.y)%map_height)
    def position_after(self,seconds):
        return ((self.pos.x+self.vel.x*seconds)%map_width,
                (self.pos.y+self.vel.y*seconds)%map_height)
    def quadrant_after(self,seconds):
        return quadrant(self.position_after(seconds))
    def increment_times(self,seconds):
        self.pos = self.position_after(seconds)
# 0 1
# 2 3
def quadrant(position):
    if (position[0] == map_width//2) or (position[1] == map_height//2):
        return -1
    quad = 0
    if position[0] > map_width//2:
        quad += 1
    if position[1] > map_height//2:
        quad += 2
    return quad

def display_robots():
    robot_positions = set(map(lambda robot:robot.pos,robots))
    for y in range(map_height):
        for x in range(map_width):
            if Vector(x,y) in robot_positions:
                print("#", end="")
            else:
                print(".", end="")
        print("\n", end="")

# def bezout(a,b):


robots = []
for line in lines:
    data = line[2:].split(" v=")
    robots.append(Robot(pos=tuple(map(int,data[0].split(","))),
                        vel=tuple(map(int,data[1].split(",")))))

quadrant_counts = Counter()
for robot in robots:
    quadrant_counts[robot.quadrant_after(100)] += 1

result1 = 1
for i in range(4):
    result1 *= quadrant_counts[i]
print(result1)

# CRT solving 9 mod 101, 65 mod 103
x = 9
for i in range(103):
    if x%103 == 65:
        result2 = x
        break
    x += 101

print(result2)

for robot in robots:
    robot.increment_times(result2)
# for i in range(103):
    # print("-"*20)
    # print("time =",i)
    # print("-"*20)
    # display_robots()
    # for robot in robots:
    #     robot.increment()
    # input()
display_robots()