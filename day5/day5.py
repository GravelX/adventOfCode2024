import os

directory = os.path.dirname(os.path.realpath(__file__))
input_file_path = os.path.join(directory, 'input.txt')
# Read file
with open(input_file_path, 'r') as file:
    lines = file.readlines()

# Decompose the input
rules = []
updates = []
eor = False
for line in lines:
    if line == "\n":
        eor = True
    elif not eor:
        # Create rule
        parsed = [int(x) for x in line.split('|')]
        rules.append(parsed)
    else:
        # Create updates
        updates.append([int(x) for x in line.split(',')])

def check_update(update):
    # Verify if the update is valid
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            if update.index(rule[0]) > update.index(rule[1]):
                return False
    return True

def reorder_update(update):
    # Reorder the update
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            if update.index(rule[0]) > update.index(rule[1]):
                update[update.index(rule[0])], update[update.index(rule[1])] = update[update.index(rule[1])], update[update.index(rule[0])]

def main():
    valid_mids = 0 # Part 1 counter
    invalid_mids = 0 # Part 2 counter
    for update in updates:
        # Verify if the update is valid
        if check_update(update):
            # If valid, increment the counter with the center element
            valid_mids += update[len(update)//2]
        else:
            # If invalid, reorder then increment the other counter with the center element
            while not check_update(update):
                reorder_update(update)
            invalid_mids += update[len(update)//2]

    # Print the result for part 1
    print("Sum of middle pages (valid):", valid_mids)
    # Print the result for part 2
    print("Sum of middle pages (invalid):", invalid_mids)

main()