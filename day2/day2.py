import os

directory = os.path.dirname(os.path.realpath(__file__))
input_file_path = os.path.join(directory, 'input.txt')
# Read file
with open(input_file_path, 'r') as file:
    lines = file.readlines()

def analyse_reports(problem_dampener):
    # Analyse each reports
    safe_reports = 0
    for line in lines:
        # Split the report
        levels = [int(level) for level in line.strip().split()]

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
    rule_break = False
    safe = True
    ascending = report[0][1] > report[0][0]

    # Crawl through each level of the report and detect rule breaks
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
                # Special case: >3 diff on last end: error can be ignored
                if (i == len(report[0])-1) and (abs(diff) > 3):
                    return safe
                
                # Special case: >3 diff on before last end
                # If removing self instead would cause the report to be safe, then report is safe
                if ((i == len(report[0])-2) and (abs(diff) > 3)) and (abs(report[0][i+1] - report[0][i-1]) < 3):
                    return safe
                
                # >3 diff but default remove wouldnt work
                if (abs(diff) > 3) and (abs(report[0][i] - report[0][-2]) < 3):
                    del report[0][i]
                    report[1] = False
                    return analyse_levels(report)
                
                # Direction inversion where default handling would cause a pair of levels of equal value
                if (report[0][i] == report[0][i-2]):
                    # Begining of the report
                    if (i == 2):
                        del report[0][i-2]
                        report[1] = False
                        return analyse_levels(report)
                    # End of the report
                    elif (i == len(report[0])-1):
                        del report[0][i]
                        report[1] = False
                        return analyse_levels(report)
                    
                # Direction inversion where default handling would also cause direction inversion
                # Ascending
                if ascending and diff < 0 and i > 2:
                    if report[0][i] - report[0][i-2] < 0:
                        del report[0][i]
                        report[1] = False
                        return analyse_levels(report)
                # Descending
                elif not ascending and diff > 0 and i > 2:
                    if report[0][i] - report[0][i-2] > 0:
                        del report[0][i]
                        report[1] = False
                        return analyse_levels(report)
                    
                # Default error handling
                del report[0][i-1]
                report[1] = False
                return analyse_levels(report)
            else:
                safe = False
                break
    return safe

# Print the result for part 1
print("Safe reports (without the Problem Dampener): ", analyse_reports(False))

# Print the result for part 2
print("   Safe reports (with the Problem Dampener): ", analyse_reports(True))