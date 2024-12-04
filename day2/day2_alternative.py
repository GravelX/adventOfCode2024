import os

directory = os.path.dirname(os.path.realpath(__file__))
input_file_path = os.path.join(directory, 'input.txt')
# Read file
with open(input_file_path, 'r') as file:
    lines = file.readlines()

def analyse_report(level, err_permitted):
    safe = True
    direction = "Not set"

    for i in range(1, len(level)):
        diff = level[i] - level[i-1]

        if diff == 0:
            if err_permitted:
                del level[i-1]
                return analyse_report(level, False)
            else:
                safe = False
                break
        else:
            if direction == "Not set":
                direction = "Ascending" if diff > 0 else "Descending"
            
            if (direction == "Ascending" and diff < 0) or (direction == "Descending" and diff > 0):
                if err_permitted:
                    del level[i-1]
                    return analyse_report(level, False)
                else:
                    safe = False
                    break
            elif abs(diff) > 3:
                if err_permitted:
                    del level[i-1]
                    return analyse_report(level, False)
                else:
                    safe = False
                    break
    return safe

def analyse_reports(dampening):
    safe_reports = 0
    for report in lines:
        # Split the report
        level = [int(number) for number in report.strip().split()]

        if analyse_report(level, dampening):
            safe_reports += 1
    return safe_reports

print("Safe reports (Pt1): ", analyse_reports(False))
print("Safe reports (Pt2): ", analyse_reports(True))