import sys
import time
# from math import inf as infinity
# from heapq import heapify, heappop, heappush
#import re
# import itertools
# import collections

# Storing positions as complex numbers
# Real part is horizontal position, imaginary part is vertical position
def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    codes = []
    for line in lines:
        line = line.strip()
        codes.append(line)
    return codes
            
    
keypad_positions = {
    '0': 1 + 0j,
    'A': 2 + 0j,
    '1': 0 + 1j,
    '2': 1 + 1j,
    '3': 2 + 1j,
    '4': 0 + 2j,
    '5': 1 + 2j,
    '6': 2 + 2j,
    '7': 0 + 3j,
    '8': 1 + 3j,
    '9': 2 + 3j
}

dirpad_positions = {
    '^': 1 + 1j,
    'v': 1 + 0j,
    '<': 0 + 0j,
    '>': 2 + 0j,
    'A': 2 + 1j
}

# NOTE - fixed this based on guidance from Reddit post.
def compute_keypad_transition(startkey, endkey):
    startpos = keypad_positions[startkey]
    endpos = keypad_positions[endkey]
    
    displacement = endpos - startpos
    x = int(displacement.real)
    y = int(displacement.imag)

    # Going from left side of keypad to the bottom side of the keypad
    # To avoid the bottom left corner
    if startpos.real == 0 and endpos.imag == 0:
        return '>' * abs(x) +'v' * abs(y)
    # Going from bottom of keypad to the left side of the keypad
    if startpos.imag == 0 and endpos.real == 0:
        return '^' * abs(y) + '<' * abs(x)

    if x < 0: 
        horizontal = '<'
    elif x > 0:
        horizontal = '>'
    else:
        horizontal = ''
    if y < 0:
        vertical = 'v'
    elif y > 0:
        vertical = '^'
    else:
        vertical = ''

    if x > 0:
        return vertical * abs(y) + horizontal * abs(x)

    else:
        return horizontal * abs(x) + vertical * abs(y)

# NOTE - work on this based on guidance from Reddit post. I have my policy wrong
def compute_dirpad_transition(startkey, endkey):
    startpos = dirpad_positions[startkey]
    endpos = dirpad_positions[endkey]
    
    displacement = endpos - startpos
    x = int(displacement.real)
    y = int(displacement.imag)

    if startpos.real == 0:
        return '>' * abs(x) + 'v' * abs(y)
    if endpos.real == 0:
        return '^' * abs(y) + '<' * abs(x)

    if x < 0: 
        horizontal = '<'
    elif x > 0:
        horizontal = '>'
    else:
        horizontal = ''
    if y < 0:
        vertical = 'v'
    elif y > 0:
        vertical = '^'
    else:
        vertical = ''
    # If you're moving to the right, do right, THEN up/down. Need to avoid passing through 0,1 square
    if x > 0:
        return vertical * abs(y) + horizontal * abs(x)
    else:
        return horizontal * abs(x) + vertical * abs(y)

def compute_all_keypad_transitions(keypad_positions):
    return {(startkey, endkey): compute_keypad_transition(startkey, endkey) for startkey in keypad_positions for endkey in keypad_positions if startkey != endkey}   

def compute_all_dirpad_transitions(dirpad_positions):
    return {(startkey, endkey): compute_dirpad_transition(startkey, endkey) for startkey in dirpad_positions for endkey in dirpad_positions}

def code_to_keypad_transitions(code, keypad_transitions):
    initial_key = 'A'
    key_visits = initial_key + code
    transitions = zip(key_visits, key_visits[1:])
    return [keypad_transitions[transition] for transition in transitions]

def keypad_transitions_to_dirpad_presses(code_keypad_moves) -> None:
    dirpad_sequence = ''
    for move in code_keypad_moves:
        dirpad_sequence += move + 'A'
    return dirpad_sequence

def dirpad_presses_to_remote_dirpad_commands(dirpad_presses, dirpad_transitions):
    initial_dirpad = 'A'
    dirpad_key_visits = initial_dirpad + dirpad_presses
    transitions = zip(dirpad_key_visits, dirpad_key_visits[1:])
    remote_dirpad_sequence = ''
    for transition in transitions:
        remote_dirpad_sequence += dirpad_transitions[transition] + 'A'
    return remote_dirpad_sequence

    
def main():
    start_time = time.time()
    file_path = sys.argv[1]
    codes = read_input(file_path)
    print(f"Codes: {codes}")
    #code = codes[0]
    # code = '029A'
    # code_value = int(code[0:3])
    #print(f"Code: {code}")
    keypad_transitions = compute_all_keypad_transitions(keypad_positions)
    dirpad_transitions = compute_all_dirpad_transitions(dirpad_positions)
    #print(f"Dirpad transitions: {dirpad_transitions}")
    total = 0
    
    for code in codes:
        code_value = int(code[0:3])
        # For a code, computes the movements across the keypad to access all the buttons, starting from A
        # Makes use of the policy determined for how to move between keys
        code_keypad_transitions = code_to_keypad_transitions(code, keypad_transitions) 
        # From the movements needed across the keypad, works out the sequence of dirpad presses needed to move between keys on the keypad 
        # and also the A button presses to make the keypad robot press the keypad buttons
        code_dirpad_presses = keypad_transitions_to_dirpad_presses(code_keypad_transitions)
        # Transforms between the dirpad pressed by a dirpad robot and the remote dirpad commands needed to move between the buttons on the first dirpad 
        # and also press the buttons. Makes use of the policy determined for how to move between keys on the dirpad
        remote_dirpad_command_sequence = code_dirpad_presses
        for count in range(24):
            print(f"Count: round {count} of 24")
            remote_dirpad_command_sequence = dirpad_presses_to_remote_dirpad_commands(remote_dirpad_command_sequence, dirpad_transitions)
            print(f"Length of remote dirpad command sequence: {len(remote_dirpad_command_sequence)}")
        #remote_dirpad_command_sequence = dirpad_presses_to_remote_dirpad_commands(code_dirpad_presses, dirpad_transitions)
        #print(f"Remote dirpad command sequence for first code: {remote_dirpad_command_sequence}")
        final_remote_dirpad_command_sequence = dirpad_presses_to_remote_dirpad_commands(remote_dirpad_command_sequence, dirpad_transitions)
        #print(f"Final remote dirpad command sequence for first code: {final_remote_dirpad_command_sequence}")
        final_command_len = len(final_remote_dirpad_command_sequence)
        #print(f"Length of final remote dirpad command sequence: {len(final_remote_dirpad_command_sequence)}")
        score = code_value * final_command_len
        #print(f"Score: {score}")
        total += score
    print(f"Total: {total}")

    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time}")    



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_12_problem_1.py <file_path>")
    else:
        main()