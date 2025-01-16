import sys
import time
import re
# import itertools
# import collections


def get_machines_info(file_path):
    machines_info = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        section = []
        for line in lines:
            line = line.strip()
            if line:
                section.append(line)
                if len(section) == 3:
                    machines_info.append(section)
                    section = []
            else:
                if section:
                    machines_info.append(section)
                    section = []
        if section:  # In case the last section is not followed by a blank line
            machines_info.append(section)
    return machines_info

def extract_machine_info(machine_info):
    pattern = r'X[+=](\d+), Y[+=](\d+)'
    extracted_info = []
    for line in machine_info:
        match = re.search(pattern, line)
        if match:
            x, y = match.groups()
            extracted_info.append((int(x), int(y)))
    return extracted_info

def solve_machine(machine_info):
    a = machine_info[0][0]
    b = machine_info[1][0]
    c = machine_info[0][1]
    d = machine_info[1][1]
    r = machine_info[2][0]
    s = machine_info[2][1]
    determinant = a * d - b * c
    if determinant != 0:
        button_A_presses = (r * d - b * s) / determinant
        button_B_presses = (a * s - r * c) / determinant
        if 0 < button_A_presses <= 100 and 0 < button_B_presses <= 100:
            tokens = 3 * button_A_presses + button_B_presses
            if tokens.is_integer():
                return int(tokens)
            else:
                return 0
        else:
            return 0
    else:
        return 0


def main():
    start_time = time.time()
    file_path = sys.argv[1]
    machines_inputs = get_machines_info(file_path)
    tokens = 0
    for machine in machines_inputs:
        extracted_info = extract_machine_info(machine)
        tokens += solve_machine(extracted_info)
    print(f"Tokens: {tokens}")
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time}")    



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_12_problem_1.py <file_path>")
    else:
        main()