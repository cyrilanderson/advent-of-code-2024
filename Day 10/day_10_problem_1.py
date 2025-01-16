import sys
import time
# import itertools
# import collections


def read_map(file_path):
    terrain_map = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            row = []
            for char in line:
                row.append(int(char))
            terrain_map.append(row)
    return terrain_map

def find_zeroes(terrain_map):
    zeroes = []
    for row_index, row in enumerate(terrain_map):
        for col_index, col in enumerate(row):
            if col == 0:
                zeroes.append((row_index, col_index))
    return zeroes

# Given a map of the terrain consisting of a 2d list of digits from 0 to 9,
# and given a row, col pair where the digit is 0,
# find the number of multistep paths made up only of moves up, down, left, right 
# where the number goes up by exactly 1 at each step and ends at a nine. 
# The score goes up by one for each distinct square with a 9 you can reach from your starting point.
def find_trailhead_score(terrain_map, zero):
    visited = set()
    row, col = zero
    score = 0
    visited.add(zero)
    queue = [(row, col)]
    while queue:
        row, col = queue.pop(0)
        if terrain_map[row][col] == 9:
            score += 1
        for row_offset, col_offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row = row + row_offset
            new_col = col + col_offset
            if new_row >= 0 and new_row < len(terrain_map) and new_col >= 0 and new_col < len(terrain_map[0]) and terrain_map[new_row][new_col] == terrain_map[row][col] + 1 and (new_row, new_col) not in visited:
                visited.add((new_row, new_col))
                queue.append((new_row, new_col))
    return score
    




def main():
    start_time = time.time()
    file_path = sys.argv[1]
    terrain_map = read_map(file_path)
    zeroes = find_zeroes(terrain_map)
    map_score = 0
    for zero in zeroes:
        map_score += find_trailhead_score(terrain_map, zero)
    print(map_score)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")    



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_9_problem_1.py <file_path>")
    else:
        main()