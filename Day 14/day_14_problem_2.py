import sys
import time
import re
# import itertools
# import collections


def get_robots_info(file_path):
    # I am using a list here instead of a set
    # Not because the order of robots is important
    # But because I'm going to want to be able to sort them
    # And sets are unordered
    # I'm not going to need to do any searches on this data
    # Just going to 
    robots_info = set()
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            pattern = r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)'
            match = re.search(pattern, line)
            if match:
                p1, p2, v1, v2 = match.groups()
                p1, p2, v1, v2 = int(p1), int(p2), int(v1), int(v2)
                #print(p1, p2, v1, v2)  # Output: 10 66 -15 38
                initial_position = p1 + p2 * 1j
                velocity = v1 + v2 * 1j
                robots_info.add((initial_position, velocity))
            else:
                continue
    return robots_info

def robot_update(robot, time_steps):
    position, velocity = robot
    new_position = position + time_steps * velocity
    # I need to do a wraparound thing with modulo when it gets to the walls
    # Space is 101 wide and 103 tall
    # So I need to do modulo 101 and modulo 103
    new_position = new_position.real % 101 + new_position.imag % 103 * 1j
    return new_position

def horizontal_variance(robots):
    mean = sum([robot.real for robot in robots]) / len(robots)
    variance = sum([(robot.real - mean) ** 2 for robot in robots]) / len(robots)
    return variance

# Takes the list of robot positions and prints the positions to the console
# in a grid format
# Print a 103 x 101 grid
# Each robot is represented by an 'X'
# The grid is represented by a '.'
def print_grid(robots):
    for row in range(103):
        for col in range(101):
            if (col + row * 1j) in robots:
                print('X', end='')
            else:
                print('.', end='')
        print()

def main():
    start_time = time.time()
    file_path = sys.argv[1]
    robots_inputs = get_robots_info(file_path)
    max_cycles = 101 * 103  # 103 is the height of the grid and 101 is the width
    min_variance = float('inf')
    min_variance_cycle = 0
    # cycles = []
    min_variance_robots = set()
    for cycle in range(max_cycles):
        robots = {robot_update(robot, cycle) for robot in robots_inputs}
        variance = horizontal_variance(robots)
        if variance < min_variance:
            min_variance = variance
            min_variance_cycle = cycle
            min_variance_robots = {robot for robot in robots}
    #final_robot_positions = [robot_update(robot, 100) for robot in robots_inputs]
    print(f"Min Cycle: {min_variance_cycle}")
    print(f"Min Variance: {min_variance}")
    print_grid(min_variance_robots)
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time}")
        



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_12_problem_1.py <file_path>")
    else:
        main()