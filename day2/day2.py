import os

directory = os.path.dirname(os.path.realpath(__file__))
input_file_path = os.path.join(directory, 'input.txt')
# Read file
with open(input_file_path, 'r') as file:
    lines = file.readlines()

def analyse_reports(problem_dampener):
    # Analyse each reports
    safe_reports = 0
    for report in lines:
        # Split the report
        levels = [int(level) for level in report.strip().split()]

        # Create report object
        report = []
        report.append(levels)           # Int[]: Data
        report.append(problem_dampener) # Bool: Can be dampened

        # Increment counter if the report is deemed safe
        if analyse_levels(report):
            safe_reports += 1
    
    # Return the number of safe reports
    return safe_reports

def analyse_levels(report):
    #print("Considering report: ", report)
    rule_break = False
    safe = True
    ascending = report[0][1] > report[0][0]

    for i in range(1, len(report[0])):
        diff = report[0][i] - report[0][i-1]
        if ascending:
            if not (0 < diff <= 3):
                rule_break = True
        else:
            if not (-3 <= diff < 0):
                rule_break = True

        # Manage rule breaks
        if rule_break:
            # If can be dampened
            if report[1]:
                del report[0][i-1]
                report[1] = False
                return analyse_levels(report)
            else:
                safe = False
                #print("Broke rule:", report)
                break
    #print("--> Deemed", "Safe" if safe else "Unsafe")
    return safe

# Print the result for part 1
print("Safe reports without the Problem Dampener: ", analyse_reports(False))

# Print the result for part 2
print("Safe reports with the Problem Dampener: ", analyse_reports(True))