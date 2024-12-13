from pathlib import Path
from collections import namedtuple
import time

start=time.time()
with open(Path(__file__).parent / "../inputs/day13.txt") as file:
    lines = file.read().splitlines()

# lines = """Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400

# Button A: X+26, Y+66
# Button B: X+67, Y+21
# Prize: X=12748, Y=12176

# Button A: X+17, Y+86
# Button B: X+84, Y+37
# Prize: X=7870, Y=6450

# Button A: X+69, Y+23
# Button B: X+27, Y+71
# Prize: X=18641, Y=10279""".splitlines()

Machine = namedtuple('Machine',('vecA','vecB','prize'))
# returns determinant of matrix with columns v1, v2
def det(v1,v2):
    return (v1[0]*v2[1] - v1[1]*v2[0])

def try_integer_divide(p,q):
    if (p%q != 0):
        return False,0
    return True,(p//q)

# returns integer solution to 
def solve_puzzle(machine):
    a = machine.vecA
    b = machine.vecB
    x = machine.prize
    determinant = det(a,b)
    if determinant == 0:
        print("uh oh")
        raise ZeroDivisionError()
    temp1 = b[1]*x[0]-b[0]*x[1]
    temp2 = a[1]*x[0]-a[0]*x[1]
    ok1, result1 = try_integer_divide(temp1,determinant)
    ok2, result2 = try_integer_divide(temp2,determinant)
    if ok1 and ok2:
        return abs(result1)*3+abs(result2)
    return 0
num_prizes = (len(lines)+1)//4
# print(num_prizes)

def add_vectors(v1,v2):
    return (v1[0]+v2[0],v1[1]+v2[1])

machines = []
for i in range(num_prizes):
    machines.append(Machine(tuple(map(int,lines[i*4+0][12:].split(", Y+"))),
                    tuple(map(int,lines[i*4+1][12:].split(", Y+"))),
                    tuple(map(int,lines[i*4+2][ 9:].split(", Y=")))))
# print(puzzles)
result1 = 0
result2 = 0
for machine in machines:
    # print(solve_puzzle(puzzle[0],puzzle[1],puzzle[2]))
    result1 += solve_puzzle(machine)
    new_machine = Machine(machine.vecA,machine.vecB,add_vectors(machine.prize,(10000000000000,10000000000000)))
    result2 += solve_puzzle(new_machine)
print(result1)
print(result2)
    
