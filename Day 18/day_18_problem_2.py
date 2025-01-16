import sys
import time
import itertools

# Storing positions as complex numbers
# Real part is horizontal position, imaginary part is vertical position
def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    #print(f"Number of lines: {len(lines)}")
    bytes = []
    for line in lines:
        line = line.strip()
        coords = line.split(",")
        x = int(coords[0])
        y = int(coords[1])
        bytes.append(x + y * 1j)
    bytes_for_path = bytes[:1024]
    open_positions = {x + y * 1j for x in range(71) for y in range(71) if x + y * 1j not in bytes_for_path}
    return bytes, open_positions

offsets = [-1 + 0j, 1 + 0j, 0 + 1j, 0 - 1j]

def print_memory_space(open_positions, bytes):
    print(f"Printing memory space:")
    for nrow in range(71):
        row = ""
        for ncol in range(71):
            z = ncol + nrow * 1j
            if z in open_positions:
                row += "."
            elif z in bytes:
                row += "#"
        print(row)


def find_path(bytes_included, start_pos, end_pos):
    visited = {start_pos}
    queue = [start_pos]
    while queue:
        pos = queue.pop(0)
        position = pos
        if position == end_pos:
            return 1
        for offset in offsets:
            new_pos = position + offset
            x = int(new_pos.real)
            y = int(new_pos.imag)
            if 0 <= x <= 70 and 0 <= y <= 70 and new_pos not in bytes_included and new_pos not in visited:
                visited.add(new_pos)
                queue.append(new_pos)
    return 0

# The insight here. Up to a certain item in the sequence of bytes, the path is free
# After that item, the path is blocked.
# So, we can use binary search to find the critical byte in much fewer steps.
# This runs in a bit over 1 sec
def find_critical_byte(bytes, start_pos, end_pos):
    lower = 1023
    upper = len(bytes) - 1
    while lower <= upper:
        middle = (lower + upper) // 2
        bytes_included = bytes[:middle + 1]
        is_path_free = find_path(bytes_included, start_pos, end_pos)
        if is_path_free:
            lower = middle + 1
        else:
            upper = middle - 1
    return int(bytes[lower].real), int(bytes[lower].imag)
    
    # Remains of straight-up search through all the options sequentially until there is no path.
    # Runs about 600 sec ~ 10 mins.
    # bytes_included = bytes[:counter]
    # open_positions = {x + y * 1j for x in range(71) for y in range(71) if x + y * 1j not in bytes_included}
    # for counter in range(1024, len(bytes)):
    #     print(f"Counter: {counter}")
    #     bytes_included = bytes[:counter]
    #     added_byte = bytes[counter]
    #     # print(f"Added byte: {added_byte}")
    #     if added_byte in visited:
    #         is_path_free, _ = find_path(bytes_included, start_pos, end_pos)
    #         if is_path_free:
    #             continue
    #         else:
    #             x,y = int(added_byte.real), int(added_byte.imag)
    #             return x,y
    #     else:
    #         continue

# def find_critical_byte(bytes, paths_layers, visited):
#     for counter in range(1024, len(bytes)):
#         byte = bytes[counter]
#         if byte in visited:
#             layer = visited[byte]
#             positions_in_layer = paths_layers[layer][0]
#             num_positions_in_layer = len(positions_in_layer)
#             paths_layers[layer][1] += 1
#             if paths_layers[layer][1] == num_positions_in_layer:
#                 print(counter)
#                 return int(byte.real), int(byte.imag)
            


    
def main():
    start_time = time.time()
    file_path = sys.argv[1]
    bytes, open_positions = read_input(file_path)
    #print_memory_space(open_positions, bytes)
    # print(f"Open positions: {len(open_positions)}")
    # print(f"Bytes: {len(bytes)}")
    start_pos = 0 + 0 * 1j
    end_pos = 70 + 70 * 1j
    x_crit, y_crit = find_critical_byte(bytes, start_pos, end_pos)
    print(f"Critical byte: {x_crit},{y_crit}")
    #steps = find_minimum_steps(open_positions, bytes, start_pos, end_pos)
    #print(f"Minimum steps: {steps}")
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time}")    



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_12_problem_1.py <file_path>")
    else:
        main()