import sys

def extract_rows(file_path):
    lines = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            parts = line.split()  # Split by any whitespace (spaces or tabs)
            parts = [int(part) for part in parts]
            lines.append(parts)
    return lines

def is_safe(line):
    neighbors = list(zip(line, line[1:]))
    return all(pair[1] - pair[0] in [1,2,3] for pair in neighbors) or all(pair[1] - pair[0] in [-1,-2,-3] for pair in neighbors)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_2_problem_1.py <file_path>")
    else:
        file_path = sys.argv[1]
        lines = extract_rows(file_path)
        count = 0
        for line in lines:
            if is_safe(line):
                count += 1
        print("Safe rows:", count)
