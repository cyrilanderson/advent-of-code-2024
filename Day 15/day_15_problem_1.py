import sys
import time
import re
# import itertools
# import collections

def get_warehouse_and_robot_info(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Split the content into two sections using a blank line as the delimiter
    sections = content.split('\n\n')
    
    if len(sections) != 2:
        raise ValueError("The file does not contain exactly two sections separated by a blank line.")
    
    section1 = sections[0].strip().split('\n')
    section2 = sections[1].strip().split('\n')
    
    # Process section 1
    warehouse_contents, start_position = get_warehouse_map(section1)
    
    # Process section 2
    robot_moves_data = get_moves(section2)
    
    return warehouse_contents, start_position, robot_moves_data


def get_warehouse_map(lines):
    warehouse_contents = {}
    for row_idx, line in enumerate(lines):
        for col_idx, char in enumerate(line):
            position = row_idx + col_idx * 1j
            warehouse_contents[position] = char
            if char == "@":
                robot_start = position
    return warehouse_contents, robot_start


def get_moves(lines):
    # Implement the specific processing for section 2
    moves = []
    prev = None
    move_next_dir = ()
    for line in lines:
        for char in line:
            if prev is None:
                prev = char
                move_next_dir = (char, 1)
            else:
                if char == prev:
                    move_next_dir = (char, move_next_dir[1] + 1)
                else:
                    moves.append(move_next_dir)
                    prev = char
                    move_next_dir = (char, 1)
    moves.append(move_next_dir)
    return moves

def update_warehouse(warehouse_contents, robot_position, robot_move):
    move_dir = get_direction_offset(robot_move[0])
    # print(f"Move direction: {robot_move[0]}")
    # print(f"Offset: {move_dir}")
    # print(f"Number of steps: {robot_move[1]}")
    move_dist = robot_move[1]
    for _ in range(move_dist):
        robot_position, warehouse_contents, blocked = move_once(warehouse_contents, robot_position, move_dir)
        if blocked:
            break
    return warehouse_contents, robot_position

def get_direction_offset(char):
    if char == "^":
        return -1 + 0j
    if char == "v":
        return 1 + 0j
    if char == ">":
        return 0 + 1j
    if char == "<":
        return 0 - 1j

def move_once(warehouse_contents, robot_position, move_dir):
    blocked = False
    next_pos = robot_position + move_dir
    next_char = warehouse_contents[next_pos]
    # Can't move if next position is a wall
    # This seems to be working
    if next_char == "#":
        blocked = True
    # Box pushing logic applies. Need to look ahead farther
    elif next_char == "O":
        # You need to keep track of how many boxes are in your way, 
        # look ahead farther to see if there is open space to push to
        # And need to do the shifting of boxes
        positions_to_shift = [robot_position, next_pos]
        subsequent_pos = next_pos
        subsequent_char = next_char
        while subsequent_char == "O":
            subsequent_pos += move_dir
            subsequent_char = warehouse_contents[subsequent_pos]
            if subsequent_char == "#":
                blocked = True
                break
            elif subsequent_char == ".":
                break
            else:
                # subsequent_char is another box
                positions_to_shift.append(subsequent_pos)
        if not blocked:
            robot_position += move_dir
            warehouse_contents = shift_items(warehouse_contents, positions_to_shift, move_dir)
    else:
        # Next char is open space. Can just move into it.
        # Seems to be working
        warehouse_contents[robot_position] = "."
        robot_position = next_pos
        warehouse_contents[robot_position] = "@"
        

    # if blocked:
    #     print(f"Blocked at position {next_pos}")
    return robot_position, warehouse_contents, blocked


# Shifts the contents of warehouse at a set of positions once in a given direction
def shift_items(warehouse_contents, positions, direction):
    old_contents = [warehouse_contents[position] for position in positions]
    for position in positions:
        warehouse_contents[position] = "."
    for position, content in zip(positions, old_contents):
        new_position = position + direction
        warehouse_contents[new_position] = content
    return warehouse_contents

def compute_gps_sum(box_positions):
    return sum([100 * int(pos.real) + int(pos.imag) for pos in box_positions])

def print_warehouse(warehouse_contents):
    print(f"Printing warehouse contents:")
    min_real = int(min([pos.real for pos in warehouse_contents.keys()]))
    max_real = int(max([pos.real for pos in warehouse_contents.keys()]))
    min_imag = int(min([pos.imag for pos in warehouse_contents.keys()]))
    max_imag = int(max([pos.imag for pos in warehouse_contents.keys()]))
    for real in range(min_real, max_real + 1):
        row = ""
        for imag in range(min_imag, max_imag + 1):
            row += warehouse_contents[real + imag * 1j]
        print(row)

def main():
    start_time = time.time()
    file_path = sys.argv[1]
    # WORKING
    warehouse_contents, robot_start_pos, moves = get_warehouse_and_robot_info(file_path)
    # walls = warehouse_data["walls"]
    # boxes = warehouse_data["boxes"]
    #WORKING
    print(f"Robot start position: {robot_start_pos}")
    
    # testing/troubleshooting
    robot_position = robot_start_pos
    print_warehouse(warehouse_contents)
    print(f"Movements: {moves}")

    

    for move in moves:
        warehouse_contents, robot_position = update_warehouse(warehouse_contents, robot_position, move)
    
    # test_moves = moves[0:5]
    # for move in test_moves:
    #     warehouse_contents, robot_position = update_warehouse(warehouse_contents, robot_position, move)
    #     print_warehouse(warehouse_contents)
    print_warehouse(warehouse_contents)
    final_box_positions = [pos for pos, char in warehouse_contents.items() if char == "O"]
    gps_score = compute_gps_sum(final_box_positions)
    print(f"GPS score: {gps_score}")
    # print(f"Robot start position: {robot_start_pos}")
    # print(f"Warehouse contents {warehouse_contents}")
    # print(f"Walls {walls}")
    # print(f"Boxes {boxes}")
    # print(f"Robot moves {moves}")
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time}")    



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_12_problem_1.py <file_path>")
    else:
        main()