import os
import numpy as np
# Ouaip finalement je vais utiliser numpy... xD

directory = os.path.dirname(os.path.realpath(__file__))
input_file_path = os.path.join(directory, 'input.txt')
# Read input
with open(input_file_path, 'r') as file:
    lines = file.readlines()

patterns = []
patterns.append(["M*M",
                 "*A*",
                 "S*S"])
patterns.append(["M*S",
                 "*A*",
                 "M*S"])
patterns.append(["S*M",
                 "*A*",
                 "S*M"])
patterns.append(["S*S",
                 "*A*",
                 "M*M"])

def to_np(grid):
    # Transform list of string to a 2D numpy array of their ascii values
    return np.array([[ord(char) for char in line] for line in grid])

def check_pattern(differential):
    # Check if the differential is 0 on the diagonals of the pattern
    return np.all(np.diag(differential) == 0) and np.all(np.diag(np.fliplr(differential)) == 0)

def search_pattern(grid, pattern):
    ping_pong = 0
    # Search pattern in grid
    pattern_shape = pattern.shape
    # Slide pattern over the whole grid and subtract it from the grid's values
    for i in range(grid.shape[0] - pattern_shape[0] + 1):
        for j in range(grid.shape[1] - pattern_shape[1] + 1):
            # For each value in the pattern, subtract it from the grid
            diff = grid[i:i + pattern_shape[0], j:j + pattern_shape[1]] - pattern
            # Check if the differential is 0 on the diagonals of the pattern
            if check_pattern(diff):
                ping_pong += 1

    return ping_pong

# Clean lines
lines = [line.strip() for line in lines]
# Convert to numpy array
image = to_np(lines)
# Count all possible X-MAS patterns
matches = 0
for pattern in patterns:
    matches += search_pattern(image, to_np(pattern))

# Dvide by 2 because we are counting the same pattern twice, because the inverse pattern
# happens to get detected as well (e.g. M*S and S*M) because of the way I check for a match.
print("X-MAS detected", matches, "times")