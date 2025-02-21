# Issue was I assumed loops could only be found formed by a perfect square.
# Actually, a loop is formed whenever adding an obstacle to the grid would
# result in the gard coming back to the same cell again.
import os
import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt

#np.set_printoptions(threshold=sys.maxsize, linewidth=408)
directory = os.path.dirname(os.path.realpath(__file__))
input_file_path = os.path.join(directory, 'input.txt')

debug = False

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
        grid[position[0]][position[1]] = 0
        grid[position[0] - 1][position[1]] = direction
        return ([position[0] - 1, position[1]])
    elif direction == 2:
        grid[position[0]][position[1]] = 0
        grid[position[0]][position[1] + 1] = direction
        return ([position[0], position[1] + 1])
    elif direction == 3:
        grid[position[0]][position[1]] = 0
        grid[position[0] + 1][position[1]] = direction
        return ([position[0] + 1, position[1]])
    elif direction == 4:
        grid[position[0]][position[1]] = 0
        grid[position[0]][position[1] - 1] = direction
        return ([position[0], position[1] - 1])
    else:
        raise ValueError("Unexpected direction encountered while advancing: ", direction)

def rotate_90_right(direction):
    return (direction % 4) + 1

# Check if next move is valid.
# Rotates the guard if needed.
# Return 0 if valid, 1 if out of bounds, 2 if facing an obstacle.
def evaluate_move(grid, position):
    direction = grid[position[0]][position[1]]
    new_pos = 42
    
    if direction == 1: # Up
        new_pos = grid[position[0] - 1][position[1]]
    elif direction == 2: # Right
        new_pos = grid[position[0]][position[1] + 1]
    elif direction == 3: # Down
        new_pos = grid[position[0] + 1][position[1]]
    elif direction == 4: # Left
        new_pos = grid[position[0]][position[1] - 1]
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
    
def visualize_loop(path, grid, new_ob):
    display_grid = grid.copy()
    for p in path.keys():
        display_grid[p[0]][p[1]] = 50
    # make obstacles more visible
    display_grid[display_grid == -1] = -50
    # highlight the new obstacle
    display_grid[new_ob[0]][new_ob[1]] = -99
    plt.imshow(display_grid, cmap='plasma')
    plt.show()

def visualize_grid_state(grid, prev):
    display_grid = grid.copy()
    # make obstacles more visible
    display_grid[display_grid == -1] = -50
    # highlight guard position (1, 2, 3, 4 all have the same value)
    display_grid[np.isin(display_grid, [1, 2, 3, 4])] = 100
    # highlight the previous guard position
    display_grid[prev[0]][prev[1]] = 80

    plt.imshow(display_grid, cmap='plasma')
    plt.show()
    
def loop_check(grid, position, start_pos):
    # Copy for experimentation
    grid_copy = grid.copy()
    loop_finder = position.copy()
    new_ob = None
    
    # Add an obstacle in front of the guard, but only if it is not the starting cell
    if ([loop_finder[0] - 1, loop_finder[1]] == start_pos or 
        [loop_finder[0], loop_finder[1] + 1] == start_pos or 
        [loop_finder[0] + 1, loop_finder[1]] == start_pos or 
        [loop_finder[0], loop_finder[1] - 1] == start_pos):
        return 0
    direction = grid_copy[loop_finder[0]][loop_finder[1]]
    if direction == 1: # Up
        grid_copy[loop_finder[0] - 1][loop_finder[1]] = -1
        new_ob = [loop_finder[0] - 1, loop_finder[1]]
    elif direction == 2: # Right
        grid_copy[loop_finder[0]][loop_finder[1] + 1] = -1
        new_ob = [loop_finder[0], loop_finder[1] + 1]
    elif direction == 3: # Down
        grid_copy[loop_finder[0] + 1][loop_finder[1]] = -1
        new_ob = [loop_finder[0] + 1, loop_finder[1]]
    elif direction == 4: # Left
        grid_copy[loop_finder[0]][loop_finder[1] - 1] = -1
        new_ob = [loop_finder[0], loop_finder[1] - 1]

    # Advance the guard until loop or end
    out_of_bounds = False
    prev_spin = None
    spin_counter = 0
    loop_path = {}
    while not out_of_bounds:
        direction = grid_copy[loop_finder[0]][loop_finder[1]]
        # If the key (loop finder) is already in the dic

        loop_path.update({(loop_finder[0], loop_finder[1]): direction})
        e = evaluate_move(grid_copy, loop_finder)

        if e == 0: # Valid move
            loop_finder = advance_guard(grid_copy)
            spin_counter = 0
            # Check if current position is in the loop path, with same direction
            if ((loop_finder[0], loop_finder[1]) in loop_path and
                loop_path[(loop_finder[0], loop_finder[1])] == direction):
                    if debug: visualize_loop(loop_path, grid_copy, new_ob)
                    return 1
        elif e == 1: # Out of bounds
            out_of_bounds = True
        else:
            # Detect infinite loops, where the guard is spinning but remaining in the same spot
            if prev_spin == None:
                spin_counter += 1
            else:
                if prev_spin == loop_finder:
                    spin_counter += 1                    
                if spin_counter > 3:
                    return 0
            prev_spin = loop_finder.copy()

    return 0

# Let's change our approach to the problem.
# Instead of checking later, let's look for loops AS the guard moves.
# The big difference is this: we need to change how we are detecting loops.
# This time we will try a different approach: 
# 1. Everytime we move the guard, we make a copy of the grid.
# 2. In this copy, we place an obstacle right in front of the guard.
# 3. We log the current position of the guard.
# 4. We advance the simulation and stop if either the guard returns to the
#    same cell (loop detected) or the simulation ends (guard leaves the grid, not a loop).
# 5. The only constraints to placing a new obstacle is that it cannot be placed
#    in the starting cell of the guard from the beginning of the simulation, and
#    it cannot be placed if there is already an obstacle there (we just continue 
#    to next step if so).
# 6. Count how many loops we found this way.
def run_simulation(grid, sp):
    out_of_bounds = False
    loops = 0
    # Position is where the cell with a number betwenn 1 and 4 is located
    position = np.where(grid == 1) or np.where(grid == 2) or np.where(grid == 3) or np.where(grid == 4)
    position = [position[0][0], position[1][0]]
    # If no position is found, raise an error
    if not position:
        raise ValueError("No guard found in the grid.")
    
    step = 0
    prev = None
    with tqdm(total=5084) as pbar:
        while not out_of_bounds:
            if debug:
                print(step)
                if step == 49:
                    prev = position
                elif step == 50:
                    visualize_grid_state(grid, prev)
                step += 1
            e = evaluate_move(grid, position)
            if e == 0:
                # Initiate loop check
                loops += loop_check(grid, position, sp)
                # Nothing detected in front of guard
                position = advance_guard(grid)
            elif e == 1:
                # Guard is out of bounds
                out_of_bounds = True
                advance_guard(grid)
            elif e == 2:
                # Guard is facing an obstacle and has been rotated
                pass
            pbar.update(1)
    pbar.close()

    return loops
    
def main():
    # Get puzzle input
    grid = decode_input(input_file_path)
    start_pos = np.where(grid == 1) or np.where(grid == 2) or np.where(grid == 3) or np.where(grid == 4)
    start_pos = [start_pos[0][0], start_pos[1][0]]
    # Look for loops
    loops = run_simulation(grid, start_pos)
    # Print the result
    print("Number of possible loops: ", loops)

main()