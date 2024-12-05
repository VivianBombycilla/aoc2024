from pathlib import Path

with open(Path(__file__).parent / "../inputs/day01.txt") as file:
    lines = file.read().splitlines()

# lines = """two1nine
# eightwothree
# abcone2threexyz
# xtwone3four
# 4nineeightseven2
# zoneight234
# 7pqrstsixteen
# """.splitlines()

print(lines)

result = 0
for line in lines:
    for c in line:
        if c in "123456789":
            first_digit = c
            break
    for c in reversed(line):
        if c in "123456789":
            last_digit = c
            break
    result += int(first_digit)*10+int(last_digit)

print(result)

def check_if_number(string):
    if string[0] in "123456789":
        return (True, int(string[0]))
    if string[0:3] == "one":   return True, 1
    if string[0:3] == "two":   return True, 2
    if string[0:5] == "three": return True, 3
    if string[0:4] == "four":  return True, 4
    if string[0:4] == "five":  return True, 5
    if string[0:3] == "six":   return True, 6
    if string[0:5] == "seven": return True, 7
    if string[0:5] == "eight": return True, 8
    if string[0:4] == "nine":  return True, 9
    return [False]

def get_calibration_value(line):
    for i in range(len(line)):
        check = check_if_number(line[i:i+5])
        if check[0]:
            first_digit = check[1]
            print(line)
            print(first_digit)
            break
    
    for i in reversed(range(len(line))):
        check = check_if_number(line[i:i+5])
        if check[0]:
            last_digit = check[1]
            break

    return 10*first_digit + last_digit
        
calibration_values = map(get_calibration_value,lines)
# print(list(calibration_values))
print(sum(calibration_values))