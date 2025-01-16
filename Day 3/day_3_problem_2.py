import sys
import re

def extract_rows(file_path):
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            lines.append(line)
    return lines

def find_instructions_in_line(line):
    pattern = r"mul\(\d+,\d+\)|do\(\)|don't\(\)"
    instructions = re.findall(pattern, line)
    return instructions


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_2_problem_1.py <file_path>")
    else:
        file_path = sys.argv[1]
        lines = extract_rows(file_path)
        total = 0
        # The initialization of mult_enabled should be at start and not on each line.
        # That made the difference.
        mult_enabled = True
        for line in lines:
            line_instructions = find_instructions_in_line(line)
            for instruction in line_instructions:
                if instruction == "do()":
                    mult_enabled = True
                elif instruction == "don't()":
                    mult_enabled = False
                elif mult_enabled:
                    parts = instruction[4:-1].split(",")
                    total += int(parts[0]) * int(parts[1])

    print("Total:", total)
