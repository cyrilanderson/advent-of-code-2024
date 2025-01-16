import sys
import time


# Storing positions as complex numbers
# Real part is horizontal position, imaginary part is vertical position
# Given a file path, create a dict of positions as complex numbers for keys and square contents for values
# Return the dict and also the start and end positions
# Squares are marked as '.' for open positions, '#' for walls, 'S' for start, and 'E' for end
def get_racetrack(file_path):
    racetrack = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        height = len(lines)
        width = len(lines[0].strip())
        dims = (width, height)
    for line_idx, line in enumerate(lines):
        line = line.strip()
        for char_idx, char in enumerate(line):
            pos = char_idx + line_idx * 1j
            if char == "#":
                racetrack[pos] = "#"
            elif char == ".":
                racetrack[pos] = "."
            elif char == "S":
                racetrack[pos] = "S"
                start_pos = pos
            elif char == "E":
                racetrack[pos] = "E"
                end_pos = pos

    return racetrack, start_pos, end_pos, dims


offsets = [-1 + 0j, 1 + 0j, 0 + 1j, 0 - 1j]

def print_racetrack(racetrack, dims):
    width, height = dims
    print(f"Printing racetrack:")
    for nrow in range(height):
        row = ""
        for ncol in range(width):
            z = ncol + nrow * 1j
            row += racetrack[z]
        print(row)

def print_racetrack_with_path(racetrack, path, dims):
    width, height = dims
    print(f"Printing racetrack with path:")
    for nrow in range(height):
        row = ""
        for ncol in range(width):
            z = ncol + nrow * 1j
            if racetrack[z] == "S":
                row += "S"
            elif racetrack[z] == "E":
                row += "E"
            elif z in path:
                row += "O"
            else:
                row += racetrack[z]
        print(row)

def is_open_space(racetrack, pos):
    return racetrack[pos] == "." or racetrack[pos] == "S" or racetrack[pos] == "E"

def is_wall(racetrack, pos):
    return racetrack[pos] == "#"

# Given a racetrack, returns a list of waypoints along the path from start to end as well as the length of the path
# Use a modified BFS that tracks the distance with the node points
def find_path(racetrack, start, end):
    visited = {start}
    queue = [(start, 0)]
    waypoints_by_node = {start: 0}
    waypoints_list = [start]
    
    while queue:
        pos, steps = queue.pop(0)
        if pos == end:
            break
        for offset in offsets:
            new_pos = pos + offset
            if new_pos in racetrack and is_open_space(racetrack, new_pos) and new_pos not in visited:
                visited.add(new_pos)
                queue.append((new_pos, steps + 1))
                waypoints_by_node[new_pos] = steps + 1
                waypoints_list.append(new_pos)
    
    
    return waypoints_list, waypoints_by_node

# Given two positions, return the Manhattan distance between them
def manhattan_distance(pos1, pos2):
    return abs(pos1.real - pos2.real) + abs(pos1.imag - pos2.imag)

# Given a racetrack, start, end, and a best legal path, find all possible "cheat" paths 
# that are shorter than the best legal path and by how much
# A "cheat" path is one that goes through a one square wide wall 
# You are allowed to cheat once and onyl once in the race
def count_best_cheat_paths(waypoints_list, waypoints_by_position, cheat_steps):
    best_cheats_count = 0
    # Iterate over the path. Don't consider the start and end points
    for idx,pos in enumerate(waypoints_list):
        for hor_offset in range(-cheat_steps, cheat_steps + 1):
            for ver_offset in range(abs(hor_offset) - cheat_steps, cheat_steps - abs(hor_offset) + 1):
                offset = hor_offset + ver_offset * 1j
                new_pos = pos + offset
                dist = manhattan_distance(pos, new_pos)
                    # Check if the new path is shorter than the best path
                if new_pos in waypoints_by_position and dist >= 2:
                    # advantage of cheat is difference in waypoint number - distance
                    advantage = waypoints_by_position[new_pos] - idx - dist
                    if advantage >= 100:
                        best_cheats_count += 1
                    # If so, increment the count
    return best_cheats_count


def main():
    start_time = time.time()
    file_path = sys.argv[1]
    racetrack, start, end, dims = get_racetrack(file_path)
    #print_racetrack(racetrack, dims)
    # print(f"Start: {start}, End: {end}")
    print(f"Dimensions: {dims}")

    waypoints_list, waypoints_by_pos = find_path(racetrack, start, end)
    #print(f"Shortest path: {path}")
    print(f"Length of  path: {len(waypoints_list)}")
    # print(f"Waypoints by node: {waypoints_by_pos}")
    #print_racetrack_with_path(racetrack, waypoints_by_pos, dims)
    cheat_steps = 20
    best_cheats_count = count_best_cheat_paths(waypoints_list, waypoints_by_pos, cheat_steps)  
    #print(f"Best cheats: {best_cheats}")
    print(f"Number of cheats that save > 100: {best_cheats_count}")
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time}")    



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_12_problem_1.py <file_path>")
    else:
        main()