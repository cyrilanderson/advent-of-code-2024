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
    print(f"Number of lines: {len(lines)}")
    bytes = []
    for line in lines:
        line = line.strip()
        coords = line.split(",")
        x = int(coords[0])
        y = int(coords[1])
        bytes.append(x + y * 1j)
    bytes_to_use = bytes[:1024]
    print(f"Number of bytes to use: {len(bytes_to_use)}")
    #print(f"Bytes: {bytes}")
    print(f"Number of bytes: {len(bytes)}")
    open_positions = {x + y * 1j for x in range(71) for y in range(71) if x + y * 1j not in bytes_to_use}
    print(f"Number of open positions: {len(open_positions)}")
    return bytes_to_use, open_positions 

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


def find_minimum_steps(open_positions, bytes, start_pos, end_pos):
    visited = {start_pos}
    queue = [(start_pos, 0)]
    while queue:
        pos, steps = queue.pop(0)
        if pos == end_pos:
            return steps
        for offset in offsets:
            new_pos = pos + offset
            if new_pos in open_positions and new_pos not in bytes and new_pos not in visited:
                visited.add(new_pos)
                queue.append((new_pos, steps + 1))
    return -1




def main():
    start_time = time.time()
    file_path = sys.argv[1]
    bytes, open_positions = read_input(file_path)
    print_memory_space(open_positions, bytes)
    # print(f"Open positions: {len(open_positions)}")
    # print(f"Bytes: {len(bytes)}")
    start_pos = 0 + 0 * 1j
    end_pos = 70 + 70 * 1j
    steps = find_minimum_steps(open_positions, bytes, start_pos, end_pos)
    print(f"Minimum steps: {steps}")
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time}")    



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_12_problem_1.py <file_path>")
    else:
        main()