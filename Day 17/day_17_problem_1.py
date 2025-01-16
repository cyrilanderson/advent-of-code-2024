import sys
import time
import re
# import itertools
# import collections

int_to_instruction = {
    0: 'adv',
    1: 'bxl',
    2: 'bst',
    3: 'jnz',
    4: 'bxc',
    5: 'out',
    6: 'bdv',
    7: 'cdv'
}


def get_program(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Split the content into lines
    lines = content.strip().split('\n')
    
    # Extract register values
    register_a = int(lines[0].split(': ')[1])
    register_b = int(lines[1].split(': ')[1])
    register_c = int(lines[2].split(': ')[1])
    
    # Extract program values
    program_line = lines[4]
    program = list(map(int, program_line.split(': ')[1].split(',')))
    return register_a, register_b, register_c, program

def int_to_binary(number):
    return bin(number)

def route_instruction(opcode, operand):
        
    switcher = {
    'adv': adv, 
    'bxl': bxl,
    'bst': bst,
    'jnz': jnz,
    'bxc': bxc,
    'out': out,
    'bdv': bdv,
    'cdv': cdv
    }
    
    instruction_name = int_to_instruction[opcode]
    return switcher.get(instruction_name)(operand)

def operand_to_combo_operand(operand):
    if operand in [0, 1, 2, 3]:
        return operand
    elif operand == 4:
        return a
    elif operand == 5:
        return b
    elif operand == 6:
        return c

def adv(operand):
    global a
    combo_op = operand_to_combo_operand(operand)
    a = a >> combo_op

def bxl(operand):
    global b
    b = b ^ operand

def bst(operand):
    global b
    combo_op = operand_to_combo_operand(operand)
    mask = 0b111 
    b = combo_op & mask

def jnz(operand):
    global a, instr_ptr
    if a == 0:
        return 0
    else:
        instr_ptr = operand
        return 1
def bxc(operand):
    global b,c
    b = b ^ c

def out(operand):
    global output
    combo_op = operand_to_combo_operand(operand)
    mask = 0b111
    result = combo_op & mask
    if output == "":
        output += str(result)
    else:
        output +="," + str(result)

def bdv(operand):
    global a, b
    combo_op = operand_to_combo_operand(operand)
    b = a >> combo_op

def cdv(operand):
    global a,c
    combo_op = operand_to_combo_operand(operand)
    c = a >> combo_op


def main():
    start_time = time.time()
    file_path = sys.argv[1]
    global a, b, c
    global instr_ptr
    global output
    a, b, c, program = get_program(file_path)
    output = ""
    
    print(f"Register A: {a}")
    print(f"Register B: {b}")
    print(f"Register C: {c}")
    print(f"Program: {program}")

    instr_ptr = 0
    while instr_ptr < len(program) - 1:
        opcode = program[instr_ptr]
        operand = program[instr_ptr + 1]
        if opcode != 3:
            route_instruction(opcode, operand)
        else:
            jump = jnz(operand)
            if jump:
                continue
        instr_ptr += 2
        
        
    print(f"Output: {output}")
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_17_problem_1.py <file_path>")
    else:
        main()