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

def update_warehouse(warehouse_contents, robot_position, robot_move, boxes):
    move_dir = get_direction_offset(robot_move[0])
    # print(f"Move direction: {robot_move[0]}")
    # print(f"Offset: {move_dir}")
    # print(f"Number of steps: {robot_move[1]}")
    move_dist = robot_move[1]
    for _ in range(move_dist):
        robot_position, warehouse_contents, blocked, boxes = move_once(warehouse_contents, robot_position, move_dir, boxes)
        if blocked:
            break
    return warehouse_contents, robot_position, boxes

def get_direction_offset(char):
    if char == "^":
        return -1 + 0j
    if char == "v":
        return 1 + 0j
    if char == ">":
        return 0 + 1j
    if char == "<":
        return 0 - 1j

def move_once(warehouse_contents, robot_position, move_dir, boxes):
    blocked = False
    next_pos = robot_position + move_dir
    next_char = warehouse_contents[next_pos]
    # Can't move if next position is a wall
    if next_char == "#":
        blocked = True
    # Box pushing logic applies. Need to look ahead farther
    elif next_char in ["[", "]"]:
        
        positions_to_shift = {robot_position, next_pos, boxes[next_pos]}
        queue = [next_pos, boxes[next_pos]]
        while queue:
            current_pos = queue.pop(0)
            next_pos = current_pos + move_dir
            next_char = warehouse_contents[next_pos]
            if next_char in ["[", "]"] and next_pos not in positions_to_shift:
                positions_to_shift.update([next_pos, boxes[next_pos]])
                queue.append(next_pos)
                queue.append(boxes[next_pos])
            elif next_char == "#":
                blocked = True
                break
            elif next_char == ".":
                continue

        if not blocked:
            robot_position += move_dir
            warehouse_contents, boxes = shift_items(warehouse_contents, positions_to_shift, move_dir, boxes)
    else:
        # Next char is open space. Can just move into it.
        # Seems to be working
        warehouse_contents[robot_position] = "."
        robot_position = next_pos
        warehouse_contents[robot_position] = "@"
        

    # if blocked:
    #     print(f"Blocked at position {next_pos}")
    return robot_position, warehouse_contents, blocked, boxes


# Shifts the contents of warehouse at a set of positions once in a given direction
# This will have to work a little differently for the second part
def shift_items(warehouse_contents, positions, direction, boxes):
    old_contents = [warehouse_contents[position] for position in positions]
    for position in positions:
        warehouse_contents[position] = "."
    box_updates = {}
    for position, content in zip(positions, old_contents):
        new_position = position + direction
        warehouse_contents[new_position] = content
        if position in boxes:
            box_updates[new_position] = boxes[position] + direction
            del boxes[position]
            # the partner box square will get updated in its own iteration
    boxes.update(box_updates)
    return warehouse_contents, boxes

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

def resize_warehouse(warehouse_contents):
    min_real = int(min([pos.real for pos in warehouse_contents.keys()]))
    max_real = int(max([pos.real for pos in warehouse_contents.keys()]))
    min_imag = int(min([pos.imag for pos in warehouse_contents.keys()]))
    max_imag = int(max([pos.imag for pos in warehouse_contents.keys()]))
    new_warehouse = {}
    boxes = {}
    for real in range(min_real, max_real + 1):
        for imag in range(min_imag, max_imag + 1):
            pos = real + imag * 1j
            new_pos1 = real + imag * 2*  1j
            new_pos2 = real + (2 * imag + 1) * 1j
            if warehouse_contents[pos] == ".":
                new_warehouse[new_pos1] = "."
                new_warehouse[new_pos2] = "."
            elif warehouse_contents[pos] == "#":
                new_warehouse[new_pos1] = "#"
                new_warehouse[new_pos2] = "#"
            elif warehouse_contents[pos] == "@":
                new_warehouse[new_pos1] = "@"
                new_warehouse[new_pos2] = "."
                robot_position = new_pos1
            elif warehouse_contents[pos] == "O":
                new_warehouse[new_pos1] = "["
                new_warehouse[new_pos2] = "]"
                # Keeping track of adjacency structure to know the partner of each box
                boxes[new_pos1] = new_pos2
                boxes[new_pos2] = new_pos1
    return new_warehouse, robot_position, boxes

            

def main():
    start_time = time.time()
    file_path = sys.argv[1]
    # WORKING
    warehouse_contents, robot_start_pos, moves = get_warehouse_and_robot_info(file_path)
    print_warehouse(warehouse_contents)
    # walls = warehouse_data["walls"]
    # boxes = warehouse_data["boxes"]
    #WORKING
    print(f"Robot start position: {robot_start_pos}")
    
    # testing/troubleshooting
    robot_position = robot_start_pos
    #print(f"Movements: {moves}")

    warehouse_contents, robot_position, boxes = resize_warehouse(warehouse_contents)
    print(f"New robot position: {robot_position}")
    print_warehouse(warehouse_contents)

    for move in moves:
        warehouse_contents, robot_position, boxes = update_warehouse(warehouse_contents, robot_position, move, boxes)
    
    # Earlier testing of moves and warehouse update
    # test_moves = moves[0:5]
    # for move in test_moves:
    #     warehouse_contents, robot_position = update_warehouse(warehouse_contents, robot_position, move)
    #     print_warehouse(warehouse_contents)

    print_warehouse(warehouse_contents)
    final_box_positions = [pos for pos, char in warehouse_contents.items() if char == "["]
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