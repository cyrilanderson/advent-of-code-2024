import sys
import re
import time


def read_towels_info(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().split('\n')
    
    section1 = ""
    designs = []
    section = 1
    
    for line in lines:
        line = line.strip()
        if line == '':
            section = 2
            continue
        
        if section == 1:
            section1 += ' ' + line
        else:
            designs.append(line)

    towels = section1.strip().split(', ')
    return towels, designs

def validate_design(towels, design):
    #print(f"Validating design: {design}")
    possible_towels = towels
    #intermediate_match_results = []
    design_length = len(design)
    for idx, char in enumerate(design):
        is_last_char = idx == design_length - 1
        # print(f"In loop: {idx}")
        # print(f"Validating char: {char}")
        possible_towels = [towel for towel in possible_towels if towel[idx] == char]
        #print(f"Possible towels: {possible_towels}")
        for towel in possible_towels:
            if len(towel) == idx + 1:
                #print(f"Found an intermediate match: {towel}")
                possible_towels.remove(towel)
                if is_last_char:
                    return True
                else:
                    intermediate_result = validate_design(towels, design[idx + 1:])
                    if intermediate_result:
                        return True
                    else:
                        break
        if len(possible_towels) == 0 or is_last_char:
            return False
        
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_2_problem_1.py <file_path>")
    else:
        start_time = time.time()
        file_path = sys.argv[1]
        towels, designs = read_towels_info(file_path)
        design_validity_count = 0
        for design in designs:
            #print(f"Trying design: {design}")
            result = validate_design(towels, design)
            #print(f"Result: {result}")
            if result:
                design_validity_count += 1

        print(f"Valid designs: {design_validity_count}")
        # starts_with_r = [towel for towel in towels if towel[0] == 'r']
        # print(f"Starts with r: {starts_with_r}")
        end_time = time.time()
        print(f"Elapsed time: {end_time - start_time}")
        
        
