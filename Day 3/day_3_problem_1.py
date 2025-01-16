import sys
import re

def extract_rows(file_path):
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            lines.append(line)
    return lines

# Takes in a string
# Searches through for substrings of the pattern "mul\([0-9]+,[0-9]+\)" and returns a list of tuples of the numbers

def find_mults_in_line(line):
    pattern = r"mul\((\d+),(\d+)\)"
    matches = re.findall(pattern, line)
    tuples = [(int(match[0]), int(match[1])) for match in matches]
    return tuples


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_2_problem_1.py <file_path>")
    else:
        file_path = sys.argv[1]
        lines = extract_rows(file_path)
        total = 0
        for line in lines:
            mult_tuples = find_mults_in_line(line)
            for pair in mult_tuples:
                total += pair[0] * pair[1]
        print("Total:", total)
