import os
# Would be even smarter to convert to numbers and use numpy but I don't feel like it

directory = os.path.dirname(os.path.realpath(__file__))
input_file_path = os.path.join(directory, 'input.txt')
# Read file
with open(input_file_path, 'r') as file:
    h_lines = file.readlines()

# Clean lines
h_lines = [line.strip() for line in h_lines]
# Reverse lines
v_lines = []
for i in range(len(h_lines[0])):
    new_line = ""
    for j in range(len(h_lines)):
        new_line += h_lines[j][i]
    v_lines.append(new_line)

xmas_counter = 0
key = "XMAS"
reverse_key = key[::-1]

# ..XMAS.....XMAS.....XMAS.....XMAS.....XMAS.....XMAS.....XMAS...
# .XMAS.....XMAS.....XMAS.....XMAS.....XMAS.....XMAS.....XMAS...X
# XMAS.....XMAS.....XMAS.....XMAS.....XMAS.....XMAS.....XMAS...XM
# MAS.....XMAS.....XMAS.....XMAS.....XMAS.....XMAS.....XMAS...XMA
# Horizontal search
for line in h_lines:
    xmas_counter += line.count(key)
    xmas_counter += line.count(reverse_key)
# Vertical search
for line in v_lines:
    xmas_counter += line.count(key)
    xmas_counter += line.count(reverse_key)

# ..X...X...X...X...X...X...X...X...X...X...X...X...X...X...X...
# ...M...M...M...M...M...M...M...M...M...M...M...M...M...M...M..
# A...A...A...A...A...A...A...A...A...A...A...A...A...A...A...A.
# .S...S...S...S...S...S...S...S...S...S...S...S...S...S...S...S
# Downward diagonal search
for i in range(len(h_lines) - 3):
    for j in range(len(h_lines[0]) - 3):
        if h_lines[i][j] == key[0] and h_lines[i + 1][j + 1] == key[1] and h_lines[i + 2][j + 2] == key[2] and h_lines[i + 3][j + 3] == key[3]:
            xmas_counter += 1
        if h_lines[i][j] == reverse_key[0] and h_lines[i + 1][j + 1] == reverse_key[1] and h_lines[i + 2][j + 2] == reverse_key[2] and h_lines[i + 3][j + 3] == reverse_key[3]:
            xmas_counter += 1
# Upward diagonal search
for i in range(3, len(h_lines)):
    for j in range(len(h_lines[0]) - 3):
        if h_lines[i][j] == key[0] and h_lines[i - 1][j + 1] == key[1] and h_lines[i - 2][j + 2] == key[2] and h_lines[i - 3][j + 3] == key[3]:
            xmas_counter += 1
        if h_lines[i][j] == reverse_key[0] and h_lines[i - 1][j + 1] == reverse_key[1] and h_lines[i - 2][j + 2] == reverse_key[2] and h_lines[i - 3][j + 3] == reverse_key[3]:
            xmas_counter += 1

print("XMAS appears", xmas_counter, "times")