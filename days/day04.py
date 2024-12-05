from pathlib import Path

with open(Path(__file__).parent / "../inputs/day04.txt") as file:
    lines = file.read().splitlines()

# lines = """MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX""".splitlines()

x_len = len(lines[0])
y_len = len(lines)
good_words1 = ("XMAS","SAMX")
good_words2 = ("AMMSS","AMSSM","ASMMS","ASSMM")
result1 = 0
result2 = 0

for i in range(y_len):
    for j in range(x_len):
        word1 = ""
        word2 = ""
        word3 = ""
        word4 = ""
        word5 = ""
        if j < x_len-3:
            word1 = lines[i][j]+lines[i][j+1]+lines[i][j+2]+lines[i][j+3]
        if (i < y_len-3) and (j < x_len-3):
            word2 = lines[i][j]+lines[i+1][j+1]+lines[i+2][j+2]+lines[i+3][j+3]
        if i < y_len-3:
            word3 = lines[i][j]+lines[i+1][j]+lines[i+2][j]+lines[i+3][j]
        if (i < y_len-3) and (j >= 3):
            word4 = lines[i][j]+lines[i+1][j-1]+lines[i+2][j-2]+lines[i+3][j-3]
        if (i >= 1) and (j >= 1) and (i < x_len-1) and (j < y_len-1):
            word5 = lines[i][j]+lines[i-1][j-1]+lines[i-1][j+1]+lines[i+1][j+1]+lines[i+1][j-1]
        
        if word1 in good_words1:
            result1 += 1
        if word2 in good_words1:
            result1 += 1
        if word3 in good_words1:
            result1 += 1
        if word4 in good_words1:
            result1 += 1
        if word5 in good_words2:
            result2 += 1

print(result1)
print(result2)

