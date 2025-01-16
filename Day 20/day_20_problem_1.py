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
def find_shortest_path(racetrack, start, end):
    visited = {start: None}
    queue = [(start, None, 0)]
    
    while queue:
        pos, _, steps = queue.pop(0)
        if pos == end:
            break
        for offset in offsets:
            new_pos = pos + offset
            if new_pos in racetrack and is_open_space(racetrack, new_pos) and new_pos not in visited:
                visited[new_pos] = pos
                queue.append((new_pos, pos, steps + 1))
    
    path = []
    path_waypoints = set()
    pos = end
    while pos != None:
        path = [pos] + path
        path_waypoints.add(pos)
        pos = visited[pos]   
    return path, path_waypoints

# Given a racetrack, start, end, and a best legal path, find all possible "cheat" paths 
# that are shorter than the best legal path and by how much
# A "cheat" path is one that goes through a one square wide wall 
# You are allowed to cheat once and onyl once in the race
def find_cheat_paths(racetrack, path, path_waypoints):
    cheat_scores = []
    # Iterate over the path. Don't consider the start and end points
    for idx, square in enumerate(path[: -1]):
        if idx != 0:
            previous_square = path[idx - 1]
        else:
            previous_square = None
        next_square = path[idx + 1]
        for offset in offsets:
            neighbor_square = square + offset
            if neighbor_square == previous_square or neighbor_square == next_square:
                continue
            square_after = square + 2 * offset
            # Check if the two squares adjoining are a wall and then something on the path
            if is_wall(racetrack, neighbor_square) and square_after in path_waypoints:
                    tunnel_advantage = path.index(square_after) - idx - 2
                    if tunnel_advantage >= 100:
                        cheat_scores.append(tunnel_advantage)
    return cheat_scores


def main():
    start_time = time.time()
    file_path = sys.argv[1]
    racetrack, start, end, dims = get_racetrack(file_path)
    #print_racetrack(racetrack, dims)

    path, path_waypoints = find_shortest_path(racetrack, start, end)
    #print(f"Shortest path: {path}")
    print(f"Length of shortest path: {len(path)}")
    #print_racetrack_with_path(racetrack, path, dims)

    best_cheats = find_cheat_paths(racetrack, path, path_waypoints)  
    #print(f"Best cheats: {best_cheats}")
    print(f"Number of cheats that save > 100: {len(best_cheats)}")
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time}")    



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_12_problem_1.py <file_path>")
    else:
        main()