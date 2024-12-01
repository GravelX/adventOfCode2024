import os

directory = os.path.dirname(os.path.realpath(__file__))
input_file_path = os.path.join(directory, 'input.txt')
# Read file
with open(input_file_path, 'r') as file:
    lines = file.readlines()

# Create lists
a = []
b = []
# Populate the lists
for line in lines:
    items = line.split()
    a.append(int(items[0]))
    b.append(int(items[1]))

# ------------------- Part 1 -------------------
# Sort the lists
a.sort()
b.sort()

# Calculate distances
total_distance = 0
for i in range(len(a)):
    total_distance += abs(a[i] - b[i])

# Print the result for part 1
print("Distance score: ", total_distance)

# ------------------- Part 2 -------------------
# Compute similarity score
similarity_score = 0
for id in a:
    similarity_score += id*b.count(id)

# Print the result for part 2
print("Similarity score: ", similarity_score)