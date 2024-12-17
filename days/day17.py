from pathlib import Path
from collections import namedtuple, Counter
import time

# start=time.time()
with open(Path(__file__).parent / "../inputs/day17.txt") as file:
    lines = file.read().splitlines()

# lines = """Register A: 729
# Register B: 0
# Register C: 0

# Program: 0,1,5,4,3,0""".splitlines()
# lines = """Register A: 2024
# Register B: 0
# Register C: 0

# Program: 0,3,5,4,3,0""".splitlines()
# lines = """Register A: 10
# Register B: 2024
# Register C: 43690

# Program: 4,0""".splitlines()


class Registers:
    def __init__(self,A,B,C,program):
        self.A = A
        self.B = B
        self.C = C
        self.program = program
        self.instr_pointer = 0
        self.output = []
    def combo(self,operand):
        if operand <= 3:
            return operand
        if operand == 4:
            return self.A
        if operand == 5:
            return self.B
        if operand == 6:
            return self.C
        return ValueError()
    def adv(self,operand):
        self.A = (self.A)//(2**self.combo(operand))
    def bxl(self,operand):
        self.B = (self.B)^(operand)
    def bst(self,operand):
        self.B = self.combo(operand)%8
    def jnz(self,operand):
        if (self.A != 0):
            self.instr_pointer = operand
            self.instr_pointer -= 2
    def bxc(self,operand):
        self.B = (self.B)^(self.C)
    def out(self,operand):
        self.output.append((self.combo(operand))%8)
    def bdv(self,operand):
        self.B = (self.A)//(2**self.combo(operand))
    def cdv(self,operand):
        self.C = (self.A)//(2**self.combo(operand))
        
    def OPCODES(self,opcode):
        return {
            0:self.adv,
            1:self.bxl,
            2:self.bst,
            3:self.jnz,
            4:self.bxc,
            5:self.out,
            6:self.bdv,
            7:self.cdv,
        }[opcode]
    def run_instruction(self):
        opcode,operand = self.program[self.instr_pointer:self.instr_pointer+2]
        self.OPCODES(opcode)(operand)
        self.instr_pointer += 2
    def reset_machine(self,A):
        self.A = A
        self.B = 0
        self.C = 0
        self.instr_pointer = 0
        self.output = []
    def run_program(self,A):
        self.reset_machine(A)
        while self.instr_pointer < len(registers.program):
            self.run_instruction()

    def check_if_quine(self,A):
        self.reset_machine(A)
        while self.instr_pointer < len(registers.program):
            registers.run_instruction()
            if not is_initial_segment(self.output,self.program):
                return False
        return self.output == self.program
    
    # Returns all possible next fragments
    def find_possible_fragments(self,A_fragment,desired_output):
        # print(A_fragment,desired_output)
        possible_fragments = set()
        for i in range(8):
            if A_fragment*8+i == 0: continue
            self.reset_machine(A_fragment*8+i)
            while len(self.output) == 0:
                registers.run_instruction()
            # print(self.output)
            if self.output[0] == desired_output:
                possible_fragments.add(A_fragment*8+i)
        return possible_fragments
    def display_output(self):
        print(",".join(map(str,registers.output)))
    def find_quine(self):
        # dictionary of possible A fragments found, with their associated value being the number of outputs it gets right.
        reversed_program = list(reversed(self.program))
        self.possible_A_fragments = {0:{0}}
        # print(self.possible_A_fragments)
        while True:
            best_result = max(self.possible_A_fragments.keys())
            fragment_to_try = min(self.possible_A_fragments[best_result])
            # print("trying fragment:",fragment_to_try)
            if best_result == len(self.program):
                return fragment_to_try
            self.possible_A_fragments[best_result].remove(fragment_to_try)
            if len(self.possible_A_fragments[best_result]) == 0:
                del self.possible_A_fragments[best_result]
            new_possible_fragments = self.find_possible_fragments(fragment_to_try,reversed_program[best_result])
            # print("new possible fragments:",new_possible_fragments)
            if len(new_possible_fragments) > 0:
                self.possible_A_fragments[best_result+1] = new_possible_fragments
            # print(self.possible_A_fragments)
            # input()


# Returns True if list1 is an initial segment of list2
def is_initial_segment(list1,list2):
    if len(list1) > len(list2): return False
    for i in range(len(list1)):
        if list1[i] != list2[i]: return False
    return True

# Registers = namedtuple("Registers",["A","B","C"])
registers = Registers(int(lines[0][12:]),
                      int(lines[1][12:]),
                      int(lines[2][12:]),
                      list(map(int,lines[4][9:].split(","))))

# print(registers.A,registers.B,registers.C)
# print(registers.program)
# print(registers.instr_pointer)
# print(",".join(map(str,registers.output)))
    # print(registers.A,registers.B,registers.C)
    # print(registers.A%8,registers.B%8,registers.C%8)
    # print(registers.program)
    # print(registers.instr_pointer)
    # print(",".join(map(str,registers.output)))
    # input()
registers.run_program(registers.A)
result1 = ",".join(map(str,registers.output))
print(result1)

# result2 = registers.find_quine()
# print(registers.find_next_3(0,0))
# registers.run_program(117440)
# registers.display_output()
print(registers.find_quine())
# test_A = 417790000
# while True:
#     if test_A % 10000 == 0:
#         print("A",test_A)
#     if registers.check_if_quine(test_A):
#         # print("success")
#         break
#     # print("failed")
#     test_A += 1
# result2 = test_A
# print(test_A)