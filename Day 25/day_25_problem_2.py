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
    # print(f"Instruction: {instruction_name}")
    # print(f"Operand: {operand}")
    # if instruction_name in ['adv', 'bst', 'out', 'bdv', 'cdv']:
    #     print(f"Combo operand: {operand_to_combo_operand(operand)}")
    # print()
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

# Integer divides the value in register A by 
# 2**operand and stores the result in register A
# If operand is 0-3, the operand is used as is
# 4-6 use the value in register A, B, C respectively
def adv(operand):
    global a
    combo_op = operand_to_combo_operand(operand)
    a >>= combo_op

# Bitwise XOR the value in register B with the operand
# and stores the result in register B
# Bitwise XOR gives 1 if the bits are different
def bxl(operand):
    global b
    b ^= operand

# Value in register B mod 8 is stored in register B
def bst(operand):
    global b
    combo_op = operand_to_combo_operand(operand)
    mask = 0b111 
    b = combo_op & mask

# If the value in register A is NOT 0, jump to the instruction #
def jnz(operand):
    global a, instr_ptr
    if a == 0:
        return 0
    else:
        instr_ptr = operand
        return 1

# Bitwise XOR the value in register B with the value in register C
# and stores the result in register B
def bxc(operand):
    global b,c
    b ^= c

# The lowest 3 bits of the operand (mod 8) are stored in the output
# Uses the combo operand 
# If operand in [0, 1, 2, 3], the operand is used as is
# If the operand is 4,5,6 the value in register A,B,C is used respectively
def out(operand):
    global output
    combo_op = operand_to_combo_operand(operand)
    mask = 0b111
    result = combo_op & mask
    output.append(result)

# Integer divides the value in register A by 
# 2**operand and stores the result in register B
# If operand is 0-3, the operand is used as is
# 4-6 use the value in register A, B, C respectively
def bdv(operand):
    global a, b
    combo_op = operand_to_combo_operand(operand)
    b = a >> combo_op

# Integer divides the value in register A by 
# 2**operand and stores the result in register C
# If operand is 0-3, the operand is used as is
# 4-6 use the value in register A, B, C respectively
def cdv(operand):
    global a,c
    combo_op = operand_to_combo_operand(operand)
    c = a >> combo_op

def run_program(program, a_value):
    global instr_ptr
    global a
    global output
    instr_ptr = 0
    a = a_value
    output = []
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
    return output

def recursive_try_a_value(program, a_val, idx):
    for num in range(8):
        # print(f"a_val: {a_val}, num: {num}")
        next_a_val = (a_val << 3) | num
        # print(f"Next A value: {next_a_val}")
        result = run_program(program, next_a_val)
        # print(f"Output: {result}")
        if result[0] == program[idx]:
            if idx == 0:
                return next_a_val
            else:
                test = recursive_try_a_value(program, next_a_val, idx - 1)
                if test == None:
                    continue
                else:
                    return test
    return None           



def main():
    start_time = time.time()
    file_path = sys.argv[1]
    global a, b, c
    global instr_ptr
    global output
    a, b, c, program = get_program(file_path)
    print(f"Program: {program}")
    target_a = recursive_try_a_value(program, 0, len(program) - 1)
    print(f"Target A: {target_a}")
    # for a_value in range(0, 8**4):
    #     run_program(program, a_value)
    #     print(f"Initial A value: {oct(a_value)}, Output: {output}")
    
    # run_program(program, 56256477)
    # print(f"Output: {output}")
    # print(f"Register A: {a}")
    # print(f"Register B: {b}")
    # print(f"Register C: {c}")
    # print(f"Program: {program}")
    # print()

    
    
    # instr_ptr = 0
    # while instr_ptr < len(program) - 1:
    #     opcode = program[instr_ptr]
    #     operand = program[instr_ptr + 1]
    #     if opcode != 3:
    #         route_instruction(opcode, operand)
    #     else:
    #         jump = jnz(operand)
    #         if jump:
    #             continue
    #     instr_ptr += 2
        
        
    # print(f"Output: {output}")
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_17_problem_1.py <file_path>")
    else:
        main()