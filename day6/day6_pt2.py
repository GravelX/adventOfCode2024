import os
import numpy as np
from matplotlib import pyplot as plt

#np.set_printoptions(threshold=sys.maxsize, linewidth=408)
directory = os.path.dirname(os.path.realpath(__file__))
input_file_path = os.path.join(directory, 'input.txt')

debug = True

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
    
def run_simulation(grid):
    out_of_bounds = False
    turn_pos = []
    # Position is where the cell with a number betwenn 1 and 4 is located
    position = np.where(grid == 1) or np.where(grid == 2) or np.where(grid == 3) or np.where(grid == 4)
    position = [position[0][0], position[1][0]]
    # If no position is found, raise an error
    if not position:
        raise ValueError("No guard found in the grid.")
    
    while not out_of_bounds:
        e = evaluate_move(grid, position)
        if e == 0:
            position = advance_guard(grid)
        elif e == 1:
            out_of_bounds = True
            advance_guard(grid)
        elif e == 2:
            turn_pos.append([position[0], position[1]]) # -1 because of the padding

    return turn_pos

def detect_loops(grid, corners, start_pos):
    loop_count = 0
    loops_data = [] # for visualization purposes
    # If a series of 3 turns can be placed on a single rectangle, then a loop is possible
    for i in range(len(corners)-3):
        # To detect that the 3 turns are on the same rectangle, we first need to check that the corners are aligned
        if ((corners[i][0] == corners[i+1][0]) or (corners[i][1] == corners[i+1][1]) and
            (corners[i+1][0] == corners[i+2][0]) or (corners[i+1][1] == corners[i+2][1])):
            # A loop cannot be created if the missing corner would need to be placed on the starting position.
            # Find the missing corner:
            # If the two first corners form a horizontal line
            if corners[i][0] == corners[i+1][0]:
                if corners[i+2][1] == corners[i][1]:
                    missing_corner = [corners[i+2][0], corners[i+1][1]]
                else:
                    missing_corner = [corners[i+2][0], corners[i][1]]
            # If the two first corners form a vertical line
            else:
                if corners[i+2][0] == corners[i][0]:
                    missing_corner = [corners[i+1][0], corners[i+2][1]]
                else:
                    missing_corner = [corners[i][0], corners[i+2][1]]

            # Determine position of the missing corner, and new obstacle position
            potential_obstacle = []
            # Top left corner
            if missing_corner[0] == min(corners[i][0], corners[i+2][0]) and missing_corner[1] == min(corners[i][1], corners[i+2][1]):
                # Then the new obstacle would need to be placed directly above the corner
                potential_obstacle = [missing_corner[0]-1, missing_corner[1]]
            # Top right corner
            elif missing_corner[0] == min(corners[i][0], corners[i+2][0]) and missing_corner[1] == max(corners[i][1], corners[i+2][1]):
                # Then the new obstacle would need to be placed directly right of the corner
                potential_obstacle = [missing_corner[0], missing_corner[1]+1]
            # Bottom right corner
            elif missing_corner[0] == max(corners[i][0], corners[i+2][0]) and missing_corner[1] == max(corners[i][1], corners[i+2][1]):
                # Then the new obstacle would need to be placed directly below the corner
                potential_obstacle = [missing_corner[0]+1, missing_corner[1]]
            # Bottom left corner
            elif missing_corner[0] == max(corners[i][0], corners[i+2][0]) and missing_corner[1] == min(corners[i][1], corners[i+2][1]):
                # Then the new obstacle would need to be placed directly left of the corner
                potential_obstacle = [missing_corner[0], missing_corner[1]-1]
            else:
                print("a:", corners[i], "\nb:", corners[i+1], "\nc:", corners[i+2], "\nd:", missing_corner)
                raise ValueError("Unexpected corner alignment detected.")
            
            if debug:
                rect = np.zeros(grid.shape)
                # Draw the 4 corners of rectangle formed by the 3 turns
                # Draw the boundary of the rectangle formed by the 3 turns
                # Top horizontal line
                rect[min(corners[i][0], corners[i+1][0], corners[i+2][0], missing_corner[0]), min(corners[i][1], corners[i+1][1], corners[i+2][1], missing_corner[1]):(max(corners[i][1], corners[i+1][1], corners[i+2][1], missing_corner[1]))+1] = -50
                # Bottom horizontal line
                rect[max(corners[i][0], corners[i+1][0], corners[i+2][0], missing_corner[0]), min(corners[i][1], corners[i+1][1], corners[i+2][1], missing_corner[1]):(max(corners[i][1], corners[i+1][1], corners[i+2][1], missing_corner[1]))+1] = -50
                # Left vertical line
                rect[min(corners[i][0], corners[i+1][0], corners[i+2][0], missing_corner[0]):(max(corners[i][0], corners[i+1][0], corners[i+2][0], missing_corner[0]))+1, min(corners[i][1], corners[i+1][1], corners[i+2][1], missing_corner[1])] = -50
                # Right vertical line
                rect[min(corners[i][0], corners[i+1][0], corners[i+2][0], missing_corner[0]):(max(corners[i][0], corners[i+1][0], corners[i+2][0], missing_corner[0]))+1, max(corners[i][1], corners[i+1][1], corners[i+2][1], missing_corner[1])] = -50
                # Draw all current obstacles
                rect[grid == -1] = 50
                # Draw the starting position
                rect[start_pos[0], start_pos[1]] = -100
                # Draw the new obstacle that will be placed
                rect[potential_obstacle[0], potential_obstacle[1]] = 200
                # Visualize the grid, and set size to 10x10 inches
                plt.figure(figsize=(10,10))
                plt.imshow(rect, cmap='viridis')

            if debug: print("That rectangle was...", end=" ")
            
            # Finally, make sure that there are no existing obstacles on the boundary formed by the 4 corners
            # Check top horizontal line
            if np.any(grid[min(corners[i][0], corners[i+1][0], corners[i+2][0], missing_corner[0]), min(corners[i][1], corners[i+1][1], corners[i+2][1], missing_corner[1]):(max(corners[i][1], corners[i+1][1], corners[i+2][1], missing_corner[1]))+1] == -1):
                if debug: 
                    print("blocked by top horizontal line.")
                    plt.title("Invalid Loop - Top Horizontal Line")
                    plt.show()
                continue
            # Check bottom horizontal line
            if np.any(grid[max(corners[i][0], corners[i+1][0], corners[i+2][0], missing_corner[0]), min(corners[i][1], corners[i+1][1], corners[i+2][1], missing_corner[1]):(max(corners[i][1], corners[i+1][1], corners[i+2][1], missing_corner[1]))+1] == -1):
                if debug: 
                    print("blocked by top horizontal line.")
                    plt.title("Invalid Loop - Bottom Horizontal Line")
                    plt.show()
                continue
            # Check left vertical line
            if np.any(grid[min(corners[i][0], corners[i+1][0], corners[i+2][0], missing_corner[0]):(max(corners[i][0], corners[i+1][0], corners[i+2][0], missing_corner[0]))+1, min(corners[i][1], corners[i+1][1], corners[i+2][1], missing_corner[1])] == -1):
                if debug: 
                    print("blocked by top horizontal line.")
                    plt.title("Invalid Loop - Left Vertical Line")
                    plt.show()
                continue
            # Check right vertical line            
            if np.any(grid[min(corners[i][0], corners[i+1][0], corners[i+2][0], missing_corner[0]):(max(corners[i][0], corners[i+1][0], corners[i+2][0], missing_corner[0]))+1, max(corners[i][1], corners[i+1][1], corners[i+2][1], missing_corner[1])] == -1):
                if debug: 
                    print("blocked by top horizontal line.")
                    plt.title("Invalid Loop - Right Vertical Line")
                    plt.show()
                continue
            
            # Check if the new obstacle would be placed on the starting position
            # (Could also watch not to create on border, but visual inspection shows that it's not happening)
            if not potential_obstacle == start_pos:
                loops_data.append([corners[i], corners[i+2]])
                loop_count += 1
                if debug: 
                    print("valid!")
                    plt.title("Valid Loop! (#%d)" % loop_count)
                    plt.show()
            elif debug:
                print("blocked by starting position")
                plt.title("Invalid Loop - Starting Position")
                plt.show()

    return loop_count, loops_data

def vizualize(grid, data):
    # First, highlight the color of the obstacles
    grid[grid == -1] = 80
    # Then, highlight the color of the loops, using both opposite corners of the rectangles
    for corners in data:
        color = np.random.randint(150, 201)
        corner1 = [min(corners[0][0], corners[1][0]), min(corners[0][1], corners[1][1])]
        corner2 = [max(corners[0][0], corners[1][0]), max(corners[0][1], corners[1][1])]
        # Draw the outline of the rectangle
        grid[corner1[0]:corner2[0]+1, corner1[1]] = color
        grid[corner1[0]:corner2[0]+1, corner2[1]] = color
        grid[corner1[0], corner1[1]:corner2[1]+1] = color
        grid[corner2[0], corner1[1]:corner2[1]+1] = color
    # Visualize the grid
    plt.imshow(grid, cmap='viridis')
    plt.show()
    
def main():
    # Get puzzle input
    grid = decode_input(input_file_path)
    start_pos = np.where(grid == 1) or np.where(grid == 2) or np.where(grid == 3) or np.where(grid == 4)
    start_pos = [start_pos[0][0], start_pos[1][0]]
    # Run the simulation to find all pivot points
    corners = run_simulation(grid)
    # Calculate the number of possible loops
    loops, data = detect_loops(grid, corners, start_pos)
    # Visualize the grid with the loops
    vizualize(grid, data)
    # Print the result
    print("Number of possible loops: ", loops)

main()