from pathlib import Path

with open(Path(__file__).parent / "../inputs/day05.txt") as file:
    lines = file.read().splitlines()

# lines = """47|53
# 97|13
# 97|61
# 97|47
# 75|29
# 61|13
# 75|53
# 29|13
# 97|29
# 53|29
# 61|53
# 97|53
# 61|29
# 47|13
# 75|47
# 97|75
# 47|61
# 75|61
# 47|29
# 75|13
# 53|13

# 75,47,61,53,29
# 97,61,53,29,13
# 75,29,13
# 75,97,47,61,53
# 61,13,29
# 97,13,75,29,47""".splitlines()

def check_if_valid(update):
    for j in range(len(update)):
        for k in range(j+1,len(update)):
            if [update[k],update[j]] in rules:
                return False
    return True

# There is an ordering specified for any pair of pages.
def sorted_update(update):
    new_update = []
    for element in update:
        for i in range(len(new_update)):
            page = new_update[i]
            if [element,page] in rules:
                new_update.insert(i, element)
                break
        if element not in new_update:
            new_update.append(element)
    return new_update

rules = []
pages_in_order = []
result1 = 0
result2 = 0

threshold = -1

for i in range(len(lines)):
    line = lines[i]
    if line == "":
        threshold = i
        break
    rules.append([ int(x) for x in line.split("|")])

for i in range(threshold+1,len(lines)):
    line = lines[i]
    update = [int(x) for x in line.split(",")]
    valid = check_if_valid(update)
    if valid:
        result1 += update[len(update)//2]
    else:
        new_update = sorted_update(update)
        result2 += new_update[len(new_update)//2]

print(result1)
print(result2)