import numpy as np
import os

def main():
    directory = os.path.dirname(os.path.realpath(__file__))
    input_file_path = os.path.join(directory, 'input.txt')
    file = open(input_file_path)
    safeLeveledReports = []
    count = 0
    while True:
        count +=1
        line = file.readline()
        if not line:
            break
        report = line.split(' ')

        report = [int(item) for item in report]
        np_report = np.asarray(report)
        diff = np.diff(np_report)
        if np.all((diff > 0) & (diff <= 3)) or np.all((diff >= -3) & (diff < 0)):
            safeLeveledReports.append(count)
        # COMMENT OUT FOR PART 1 ONLY --------------------------------------
        for i ,item in enumerate(report):
            copy = report.copy()
            copy.pop(i)
            np_copy = np.asarray(copy)
            np_diff = np.diff(np_copy)
            if np.logical_and(np_diff > 0, np_diff <= 3).all() or np.logical_and(np_diff >= -3, np_diff < 0).all():
                safeLeveledReports.append(count)
        # -------------------------------------------------------------------
    print(len(set(safeLeveledReports)))
    file.close()
    file2 = open(input_file_path)
    lines = file2.readlines()
    ids = list(set(safeLeveledReports))
    for i in range(0, len(ids)):
        print(lines[ids[i]-1], end = '')

main()