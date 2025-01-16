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
    r = machine_info[2][0] + 10**13
    s = machine_info[2][1] + 10**13
    determinant = a * d - b * c
    if determinant != 0:
        button_A_denom = r * d - b * s
        button_B_denom = a * s - r * c
        if button_A_denom % determinant == 0 and button_B_denom % determinant == 0:
            button_A_presses = button_A_denom // determinant
            button_B_presses = button_B_denom // determinant
            if 0 < button_A_presses and 0 < button_B_presses:
                tokens = 3 * button_A_presses + button_B_presses
                return tokens
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