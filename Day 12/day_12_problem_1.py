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
                row.append(char)
            terrain_map.append(row)
    return terrain_map


def on_the_map(map, row, col):
    return row >= 0 and row < len(map) and col >= 0 and col < len(map[0])

# Given a map of the terrain consisting of capital letters A-Z representing different regions
# Pass over the squares in the map and build up a dictionary of area and perimeter for each region
# The area is the number of squares in the region. Perimeter is defined by the number of up, down, left, right 
# neighbors for squares in the region that are not in the region. That means they are on the border of the region OR 
# they border another square type.
def compute_connected_regions(terrain_map):
    # This will keep track of what squares have been visited as part of any connected region.
    # Need this because have to do some BFS to find connected regions.
    visited = set()
    # Also need to keep track of connected regions.
    # This will contain dictionaries of square type, squares visited
    # (as a check mainly to make sure it adds up), 
    # area and perimeter for each connected region.
    connected_regions = []
    for row_index, row in enumerate(terrain_map):
        for col_index, square in enumerate(row):
            if (row_index, col_index) in visited:
                continue
            else:
                # going to do a variant of BFS to find the connected region
                # here the connected region is not simply the squares you can 
                # reach as neighbors, but the squares that are the same type.
                visited.add((row_index, col_index))
                connected_region = {}
                connected_region["square_type"] = square
                connected_region["area"] = 1
                connected_region["perimeter"] = 0
                connected_region["squares"] = set([(row_index, col_index)])
                queue = [(row_index, col_index)]
                while queue:
                    row, col = queue.pop(0)
                    for row_offset, col_offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        new_row = row + row_offset
                        new_col = col + col_offset
                        # Region on the edge of the map, add perimeter for that
                        if not on_the_map(terrain_map, new_row, new_col):
                            connected_region["perimeter"] += 1
                        else:
                            # Got back to something already visited; move on
                            if (new_row, new_col) in connected_region["squares"]:
                                continue
                            # Found a new neighbor of the same type
                            # Update area, add to connected region, add to visited, add to queue
                            if terrain_map[new_row][new_col] == square:
                                connected_region["area"] += 1
                                connected_region["squares"].add((new_row, new_col))
                                visited.add((new_row, new_col))
                                queue.append((new_row, new_col))
                            else:
                                # Found a neighbor of a different type; add to perimeter
                                connected_region["perimeter"] += 1
                connected_regions.append(connected_region)
    return connected_regions


def main():
    start_time = time.time()
    file_path = sys.argv[1]
    inputs = read_map(file_path)
    connected_regions = compute_connected_regions(inputs)
    total_price = 0
    for connected_region in connected_regions:
        total_price += connected_region["area"] * connected_region["perimeter"]
    
    # for region in areas:
    #     total_price += areas[region] * perimeters[region]
    print(total_price)
    # print(areas)
    # print(perimeters)
    # print(len(areas))
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")    



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_12_problem_1.py <file_path>")
    else:
        main()