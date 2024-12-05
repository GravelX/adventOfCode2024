import os

directory = os.path.dirname(os.path.realpath(__file__))
input_file_path = os.path.join(directory, 'debug_reports.txt')
# Read file
with open(input_file_path, 'r') as file:
    my_lines = file.readlines()
input_file_path = os.path.join(directory, 'correct_reports.txt')
# Read file
with open(input_file_path, 'r') as file:
    correct_lines = file.readlines()

my_lines = [line.strip() for line in my_lines]
correct_lines = [line.strip() for line in correct_lines]

for report in correct_lines:
    if report not in my_lines:
        print(report)