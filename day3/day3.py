import os

directory = os.path.dirname(os.path.realpath(__file__))
input_file_path = os.path.join(directory, 'input.txt')
# Read file
with open(input_file_path, 'r') as file:
    lines = file.readlines()

instructions = ""
for line in lines:
    instructions += line.strip()

# TOGGLE CONDITIONNALS
CONDITIONNALS = True # False: Part1 solution, True: Part2 solution

def verify_mul(pos):
    # Check distance until comma is valid
    d = 0
    for c in instructions[pos:]:
        if c == ",":
            break
        d += 1
    if not (0 < d <= 3): return 0

    # Check if distance until closing parenthesis is valid
    p = 0
    for c in instructions[pos+d+1:]:
        if c == ")":
            break
        p += 1
    if not (0 < p <= 3): return 0

    # Check if numbers are valid
    a = instructions[pos:pos+d]
    if not a.isnumeric(): return 0
    b = instructions[pos+d+1:pos+d+1+p]
    if not b.isnumeric(): return 0

    # Return the multiplication of the numbers
    return int(a) * int(b)

k = "mul(" # Instruction key
t = ["do()","don't()"] # Toggles
kernel_width = max([len(toggle) for toggle in t]) # Kernel width for reading through instructions
total = 0 # Sum of all valid multiplications
enabled = True # Toggle for the mul finder

if (len(k) > kernel_width) or (kernel_width - len(k) > len(k) + 4):
    # I'm using a single for loop below, because it just so happens that stopping in time
    # to not go out of bounds when checking for "don't()" is fine because you can't fit a
    # "mul()" instruction in the remaining space anyways.
    raise Exception("Invalid input: For loop range would need to be tweaked.")

# Scan the string of instructions
for i in range(0,len(instructions)-kernel_width):
    if CONDITIONNALS:
        # Check for toggles - "do()"
        if instructions[i:i+len(t[0])] == t[0]:
            enabled = True
        # Check for toggles - "don't()"
        if instructions[i:i+len(t[1])] == t[1]:
            enabled = False
    # Check if mul finder is enabled
    if enabled:
        # If we find a valid instruction key, we verify the instruction
        if instructions[i:i+len(k)] == k:
            total += verify_mul(i+len(k))    

# Print the result
print("Multiplications Total: ", total)