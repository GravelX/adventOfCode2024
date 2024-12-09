import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from functools import partial
from tqdm import tqdm

#np.set_printoptions(threshold=sys.maxsize, linewidth=408)
directory = os.path.dirname(os.path.realpath(__file__))
input_file_path = os.path.join(directory, 'input.txt')

debug = False
animation = True # Slows execution time considerably when True (but it's cool)

def decode_input(file_path):
    # Read file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    #    Empty cell: '.' = 0
    # Out of bounds: 99
    #     Obstacles: '#' = -1
    #         Guard: 1 = Up, 2 = Right, 3 = Down, 4 = Left
    #     Path cell: 5
    guard_decoder = {'^': 1, '>': 2, 'v': 3, '<': 4}

    # Translate the input into a 2D numpy array
    grid = []
    for line in lines:
        row = []
        for char in line:
            if char == '.':
                row.append(0)
            elif char == '#':
                row.append(-1)
            elif char in guard_decoder:
                row.append(guard_decoder[char])
        grid.append(row)

    # Surround the grid with out of bounds cells
    grid = np.array(grid)
    return np.pad(grid, 1, 'constant', constant_values=99)
# Advance the guard in the grid.
# Mark past path on the grid.
# Return the new position of the guard.
def advance_guard(grid):
    for orientation in [1, 2, 3, 4]:
        position = np.where(grid == orientation)
        if position[0].size != 0 and position[1].size != 0:
            break
    if position[0].size == 0 or position[1].size == 0:
        raise ValueError("No guard found in the grid.")
    position = [position[0][0], position[1][0]]
    
    direction = grid[position[0]][position[1]]

    if direction == 1:
        grid[position[0]][position[1]] = 5
        grid[position[0] - 1][position[1]] = direction
        return ([position[0] - 1, position[1]])
    elif direction == 2:
        grid[position[0]][position[1]] = 5
        grid[position[0]][position[1] + 1] = direction
        return ([position[0], position[1] + 1])
    elif direction == 3:
        grid[position[0]][position[1]] = 5
        grid[position[0] + 1][position[1]] = direction
        return ([position[0] + 1, position[1]])
    elif direction == 4:
        grid[position[0]][position[1]] = 5
        grid[position[0]][position[1] - 1] = direction
        return ([position[0], position[1] - 1])
    else:
        raise ValueError("Unexpected direction encountered while advancing: ", direction)

def rotate_90_right(direction):
    if debug:
        if direction == 1:
            print("Turned right.")
        elif direction == 2:
            print("Turned down.")
        elif direction == 3:
            print("Turned left.")
        elif direction == 4:
            print("Turned up.")
    
    return (direction % 4) + 1

# Check if next move is valid.
# Rotates the guard if needed.
# Return 0 if valid, 1 if out of bounds, 2 if facing an obstacle.
def evaluate_move(grid, position):
    direction = grid[position[0]][position[1]]
    new_pos = 42
    
    if direction == 1: # Up
        new_pos = grid[position[0] - 1][position[1]]
        if debug:
            print("Evaluating moving in direction", direction, ", towards position", [position[0]-1, position[1]],": Value in grid is:", new_pos)
    elif direction == 2: # Right
        new_pos = grid[position[0]][position[1] + 1]
        if debug:
            print("Evaluating moving in direction", direction, ", towards position", [position[0], position[1]+1],": Value in grid is:", new_pos)
    elif direction == 3: # Down
        new_pos = grid[position[0] + 1][position[1]]
        if debug:
            print("Evaluating moving in direction", direction, ", towards position", [position[0]+1, position[1]],": Value in grid is:", new_pos)
    elif direction == 4: # Left
        new_pos = grid[position[0]][position[1] - 1]
        if debug:
            print("Evaluating moving in direction", direction, ", towards position", [position[0], position[1]-1],": Value in grid is:", new_pos)
    else:
        raise ValueError("Unexpected direction encountered while evaluating: ", direction)
    
    # Check if the guard is out of bounds
    if new_pos == 99:
        return 1
    # Check if the guard is facing an obstacle
    elif new_pos == -1:
        # If so, turn right.
        grid[position[0]][position[1]] = rotate_90_right(direction)
        return 2
    # Else, we can move forward right away
    else:
        return 0

def color_code(frame):
    size = frame.shape
    for i in range(size[0]):
        for j in range(size[1]):
            if frame[i][j] == -1:
                frame[i][j] = 99
            elif frame[i][j] == 5:
                frame[i][j] = 50

def run_simulation(grid):
    frames = []
    out_of_bounds = False
    # Position is where the cell with a number betwenn 1 and 4 is located
    position = np.where(grid == 1) or np.where(grid == 2) or np.where(grid == 3) or np.where(grid == 4)
    position = [position[0][0], position[1][0]]
    # If no position is found, raise an error
    if not position:
        raise ValueError("No guard found in the grid.")
    
    while not out_of_bounds:
        if debug:
            print(grid)
            input("Press Enter to continue...")
        if animation:
            frame = grid.copy()
            color_code(frame)
            frames.append(frame)

        e = evaluate_move(grid, position)
        if e == 0:
            position = advance_guard(grid)
        elif e == 1:
            out_of_bounds = True
            advance_guard(grid)
    
    # Log the final frame
    if animation:
            frame = grid.copy()
            color_code(frame)
            frames.append(frame)
    return np.count_nonzero(grid == 5), frames

def update_frame(i, im, los_framos):
    F = los_framos[i]
    im.set_array(F)
    return im,

def main():
    grid = decode_input(input_file_path)

    path_length, los_framos = run_simulation(grid)

    if animation:
        # Visualize the path taken by the guard.
        print("Animating",len(los_framos),"frames.")
        fig = plt.figure()
        im = plt.imshow(los_framos[0], animated=True)
        ani = anim.FuncAnimation(fig,
                                 partial(update_frame,
                                         im=im,
                                         los_framos=los_framos),
                                 blit=True,
                                 repeat=False,
                                 interval=1,
                                 frames=len(los_framos))
        plt.show()

    print("The guard visited", path_length, "distinct positions.")

main()

# DEV NOTES:
# If I were to refactor the vizualisation, I would animate on the first run without saving the frames
# (using a tick method in the while loop). I couldn't do it at first because I didn't know about the
# 'partial' trick to pass function parameteres.