from pathlib import Path
from collections import namedtuple, Counter
import time
import random

start=time.time()
with open(Path(__file__).parent / "../inputs/day24.txt") as file:
    lines = file.read().splitlines()

# lines = """x00: 1
# x01: 1
# x02: 1
# y00: 0
# y01: 1
# y02: 0

# x00 AND y00 -> z00
# x01 XOR y01 -> z01
# x02 OR y02 -> z02""".splitlines()
# lines = """x00: 1
# x01: 0
# x02: 1
# x03: 1
# x04: 0
# y00: 1
# y01: 1
# y02: 1
# y03: 1
# y04: 1

# ntg XOR fgs -> mjb
# y02 OR x01 -> tnw
# kwq OR kpj -> z05
# x00 OR x03 -> fst
# tgd XOR rvg -> z01
# vdt OR tnw -> bfw
# bfw AND frj -> z10
# ffh OR nrd -> bqk
# y00 AND y03 -> djm
# y03 OR y00 -> psh
# bqk OR frj -> z08
# tnw OR fst -> frj
# gnj AND tgd -> z11
# bfw XOR mjb -> z00
# x03 OR x00 -> vdt
# gnj AND wpb -> z02
# x04 AND y00 -> kjc
# djm OR pbm -> qhw
# nrd AND vdt -> hwm
# kjc AND fst -> rvg
# y04 OR y02 -> fgs
# y01 AND x02 -> pbm
# ntg OR kjc -> kwq
# psh XOR fgs -> tgd
# qhw XOR tgd -> z09
# pbm OR djm -> kpj
# x03 XOR y03 -> ffh
# x00 XOR y04 -> ntg
# bfw OR bqk -> z06
# nrd XOR fgs -> wpb
# frj XOR qhw -> z04
# bqk OR frj -> z07
# y03 OR x01 -> nrd
# hwm AND bqk -> z03
# tgd XOR rvg -> z12
# tnw OR pbm -> gnj""".splitlines()


Gate = namedtuple("Gate",["input1","input2","gate_type"])

or_gate = 0
and_gate = 1
xor_gate = 2

values = {}
for i in range(len(lines)):
    line = lines[i]
    if line == "":
        break
    line = line.split(": ")
    values[line[0]] = int(line[1])
# print(values)


def compute_gate(gate):
    if gate.gate_type == "AND":
        return values[gate.input1] & values[gate.input2]
    if gate.gate_type == "OR":
        return values[gate.input1] | values[gate.input2]
    if gate.gate_type == "XOR":
        return values[gate.input1] ^ values[gate.input2]


gates = {}
for i in range(i+1,len(lines)):
    line = lines[i]
    line = line.split(" -> ")
    input1,gate_type,input2 = line[0].split(" ")
    gates[line[1]] = Gate(input1,input2,gate_type)
# print(gates)

result1 = 0
while len(gates) > 0:
    keys_to_remove = set()
    for output in gates:
        gate = gates[output]
        if (gate.input1 in values) and (gate.input2 in values):
            values[output] = compute_gate(gate)
            if output[0] == "z":
                # print(output,values[output])
                result1 += (values[output] << int(output[1:]))
            keys_to_remove.add(output)
    for key in keys_to_remove:
        gates.pop(key)
print(result1)
result2 = "jqf,mdd,skh,wpd,wts,z11,z19,z37" # I did this part in Excel
print(result2)