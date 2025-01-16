import sys
import time
from math import inf as infinity
from heapq import heapify, heappop, heappush
#import re
# import itertools
# import collections

def get_maze(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    maze = {}
    open_positions = set()
    for row_idx, line in enumerate(lines):
        for col_idx, char in enumerate(line.strip()):
            position = row_idx + col_idx * 1j
            maze[position] = char
            if char == "S":
                start_position = position
                open_positions.add(position)
            elif char == ".":
                open_positions.add(position)
            elif char == "E":
                end_position = position
                open_positions.add(position)
            else:
                continue
    return maze, open_positions, start_position, end_position


initial_direction = 0 + 1j
offsets = [-1 + 0j, 1 + 0j, 0 + 1j, 0 - 1j]

# Given two directions in offsets, return the number of 90 degree turns, 
# whether clockwise or counterclockwise, to get from the first direction to the second
def get_number_turns(dir1, dir2):
    if dir1 == dir2:
        return 0
    elif dir1 == -dir2:
        return 2
    else:
        return 1

def print_maze(maze):
    print(f"Printing warehouse contents:")
    min_real = int(min([pos.real for pos in maze.keys()]))
    max_real = int(max([pos.real for pos in maze.keys()]))
    min_imag = int(min([pos.imag for pos in maze.keys()]))
    max_imag = int(max([pos.imag for pos in maze.keys()]))
    for real in range(min_real, max_real + 1):
        row = ""
        for imag in range(min_imag, max_imag + 1):
            row += maze[real + imag * 1j]
        print(row)

def complex_to_tuple(complex_num):
    return (int(complex_num.real), int(complex_num.imag))

def tuple_to_complex(tup):
    return tup[0] + tup[1] * 1j

def djikstra(open_positions, start_pos, end_pos, start_dir):
    # Djikstra's algorithm
    distances = {(pos, dir): infinity for pos in open_positions for dir in offsets}
    dir = start_dir
    distances[(start_pos, dir)] = 0

    visited = set()
    pq = [(0, (complex_to_tuple(start_pos), complex_to_tuple(dir)))]
    heapify(pq)
    while pq:
        _, cur_pos_and_dir = heappop(pq)
        curr_pos_tup, curr_dir_tup = cur_pos_and_dir
        current_pos = tuple_to_complex(curr_pos_tup)
        current_dir = tuple_to_complex(curr_dir_tup)
        if (current_pos, current_dir) in visited:
            continue
        visited.add((current_pos, current_dir))
        # if current_pos == end_pos:
        #     break
        for offset in offsets:
            new_pos = current_pos + offset
            if new_pos in open_positions:
                new_dir = offset
                turns = get_number_turns(current_dir, new_dir)
                tentative_distance = distances[(current_pos, current_dir)] + 1 + 1000 * turns
                if tentative_distance < distances[(new_pos, offset)]:
                    distances[(new_pos, offset)] = tentative_distance
                    heappush(pq, (tentative_distance, (complex_to_tuple(new_pos), complex_to_tuple(offset))))
                
    predecessors = {(pos,dir):[] for pos,dir in visited}
    
    for (pos, dir), distance in distances.items():
        possible_predecessors = [(pos - dir, previous_dir) for previous_dir in offsets]
        deltas = [1 + 1000 * get_number_turns(previous_dir, dir) for previous_dir in offsets]
        for predecessor, delta in zip(possible_predecessors, deltas):
            if predecessor in visited and distances[predecessor] + delta == distance:
                predecessors[(pos, dir)].append(predecessor)
    
    return distances, predecessors


def waypoints_in_best_paths(predecessors, start_pos, start_dir, end_pos, end_dir):
    visited = {(end_pos, end_dir)}
    stack = [(end_pos, end_dir)]
    while stack:
        current = stack[-1]
        if current == (start_pos, start_dir):
            #paths.append(stack.copy())
            stack.pop()
        else:
            preds_to_explore = [predecessor for predecessor in predecessors[current] if predecessor not in visited]
            if preds_to_explore:
                stack.append(preds_to_explore[0])
                visited.add(preds_to_explore[0])
            else:
                stack.pop()
    return visited

def main():
    start_time = time.time()
    file_path = sys.argv[1]
    # WORKING
    maze, open_positions, start_pos, end_pos = get_maze(file_path)
    #print_maze(maze)
    direction = initial_direction
    # print(f"Start position: {start_pos}")
    # print(f"End position: {end_pos}")
    distances, predecessors = djikstra(open_positions, start_pos, end_pos, direction)
    endpoints = {(end_pos, dir): distances[(end_pos, dir)]  for dir in offsets}
    end_pos, end_dir = min(endpoints, key=endpoints.get)
    #shortest_to_endpoints = distances[(end_pos, end_dir)]
    best_paths_waypoints = waypoints_in_best_paths(predecessors, start_pos, direction, end_pos, end_dir)
    distinct_positions = set([pos for pos, _ in best_paths_waypoints])
    print(f"Number of distinct positions: {len(distinct_positions)}")
    #print(end_pos, end_dir, shortest_to_endpoints)
    #print(f"Distances to endpoints: {end_dists}")
    #print(f"Predecessors: {predecessors}")
    #print(f"Distances: {distances}")
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time}")    



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_12_problem_1.py <file_path>")
    else:
        main()