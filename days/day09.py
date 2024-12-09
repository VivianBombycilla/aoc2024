from pathlib import Path
import time

with open(Path(__file__).parent / "../inputs/day09.txt") as file:
    lines = file.read().splitlines()

# lines = """2333133121414131402""".splitlines()
# lines = """11122""".splitlines()

line = list(map(int,lines[0]))

total_space_needed = 0
low_file_num = 0
high_file_num = -1
for i in range(0,len(line),2):
    total_space_needed += line[i]
    high_file_num += 1
print(total_space_needed)

current_block = 0
disk_position = 0
result1 = 0
while True:
    if disk_position%2 == 0:
        for i in range(line[disk_position]):
            # print("a",low_file_num)
            result1 += low_file_num*current_block
            current_block += 1
        disk_position += 1
        low_file_num += 1
    elif line[high_file_num*2] < line[disk_position]: # Fits cleanly
        for i in range(line[high_file_num*2]):
            # print("b",high_file_num)
            result1 += high_file_num*current_block
            current_block += 1
        line[disk_position] -= line[high_file_num*2]
        high_file_num -= 1
    else:
        for i in range(line[disk_position]):
            # print("c",high_file_num)
            result1 += high_file_num*current_block
            current_block += 1
        line[high_file_num*2] -= line[disk_position]
        disk_position += 1
        
    if high_file_num < low_file_num:
        break
    # break
print(result1)

starttime=time.time()
line = list(map(int,lines[0]))
file_sizes = []
file_starts = []
spaces = []
space_starts = []
count = 0
for i in range(len(line)):
    if i%2 == 0:
        file_sizes.append(line[i])
        file_starts.append(count)
    else:
        spaces.append(line[i])
        space_starts.append(count)
    count += line[i]
for i in reversed(range(1,len(file_sizes))):
    # print(i)
    file_size = file_sizes[i]
    if not spaces: break
    if file_size <= max(spaces):
        # print("compressing")
        for j in range(len(spaces)):
            if file_size <= spaces[j]:
                file_starts[i] = space_starts[j]
                space_starts[j] += file_sizes[i]
                spaces[j] -= file_sizes[i]
                if spaces[j] == 0:
                    spaces.pop(j)
                    space_starts.pop(j)
                break
    spaces.pop()
    space_starts.pop()
result2 = 0
for i in range(1,len(file_sizes)):
    start = file_starts[i]
    for j in range(file_sizes[i]):
        result2 += i*(start+j)

endtime = time.time()
print(result2)
print(endtime-starttime)