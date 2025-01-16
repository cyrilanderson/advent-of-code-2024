import sys
import time
import re
# import itertools
# import collections


def get_robots_info(file_path):
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

def vertical_variance(robots):
    mean = sum([robot.imag for robot in robots]) / len(robots)
    variance = sum([(robot.imag - mean) ** 2 for robot in robots]) / len(robots)
    return variance


def gcd_extended(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = gcd_extended(b % a, a)
        return (g, y - (b // a) * x, x)

def find_min_var_iteration_x(robots):
    # Find the robots with the minimum variance in the x direction
    min_variance = float('inf')
    min_variance_cycle = 0
    for cycle in range(101):
        new_robots = {robot_update(robot, cycle) for robot in robots}
        variance = horizontal_variance(new_robots)
        if variance < min_variance:
            min_variance = variance
            min_variance_cycle = cycle
    return min_variance_cycle

def find_min_var_iteration_y(robots):
    # Find the robots with the minimum variance in the y direction
    min_variance = float('inf')
    min_variance_cycle = 0
    for cycle in range(103):
        new_robots = {robot_update(robot, cycle) for robot in robots}
        variance = vertical_variance(new_robots)
        if variance < min_variance:
            min_variance = variance
            min_variance_cycle = cycle
    return min_variance_cycle

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


# This is an optimized version of the day 14 part 2 solution that uses some number theory 
# to find the cycle that minimizes the variance in the x and y directions
# The solution is based on the Chinese Remainder Theorem
# The Chinese Remainder Theorem states that if you have a system of congruences
# x = a1 (mod n1)
# x = a2 (mod n2)
# ...   
# x = ak (mod nk)
# where the ni are pairwise coprime, then there is a unique solution modulo N = n1 * n2 * ... * nk
# The solution is given by x = a1 * N1 * y1 + a2 * N2 * y2 + ... + ak * Nk * yk (mod N)
# where Nj = N / nj and yj is the modular inverse of Nj modulo nj
# In this case, we have two congruences
# x = a1 (mod n1)
# x = a2 (mod n2)
# where n1 = 101 and n2 = 103
# The x-es on the grid repeats every 101 and the y's every 103
# The solution is given by x = a1 * n2 * y1 + a2 * n1 * y2 (mod N)
# where N = n1 * n2 = 101 * 103 = 10303
# The modular inverse of 103 modulo 101 is 51
# The modular inverse of 101 modulo 103 is 51
# The solution is given by x = a1 * n2 * y1 + a2 * n1 * y2 (mod N)
# where y1 = 51 and y2 = 51
# The solution is given by x = a1 * 103 * 51 + a2 * 101 * 51 (mod N)
# The solution is given by x = a1 * 5253 + a2 * 5151 (mod N)
# The solution is given by x = a1 * 5253 + a2 * 5151 (mod 10303)
# Can compute a1 = 77 and a2 = 18
# The solution is given by x = 77 * 5253 + 18 * 5151 (mod 10303)
# The solution is given by x = 407181 + 92898 (mod 10303)
# The solution is given by x = 500079 (mod 10303)
def main():
    start_time = time.time()
    file_path = sys.argv[1]
    robots_inputs = get_robots_info(file_path)
    max_cycles = 101 * 103  # 103 is the height of the grid and 101 is the width
    min_var_cycle_x = find_min_var_iteration_x(robots_inputs)
    min_x_var = horizontal_variance({robot_update(robot, min_var_cycle_x) for robot in robots_inputs})
    print(f"Min Cycle X: {min_var_cycle_x}, Min X Var: {min_x_var}")
    min_var_cycle_y = find_min_var_iteration_y(robots_inputs)
    min_y_var = vertical_variance({robot_update(robot, min_var_cycle_y) for robot in robots_inputs})
    print(f"Min Cycle Y: {min_var_cycle_y}, Min Y Var: {min_y_var}")
    mod1 = 101
    mod2 = 103
    # Note here that the greatest common divisor of 101 and 103 is 1
    gcd, x, y = gcd_extended(mod1, mod2)
    # This is related to the Chinese Remainder Theorem
    cycle = (min_var_cycle_x * mod2 * y + min_var_cycle_y * mod1 * x) % max_cycles
    robots_updated = {robot_update(robot, cycle) for robot in robots_inputs}
    h_var, v_var = horizontal_variance(robots_updated), vertical_variance(robots_updated)
    print(f"Min Cycle: {cycle}")
    print(f"Min Variance X: {h_var}, Min Variance Y: {v_var}")
    print_grid(robots_updated)
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time}")    
    



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_12_problem_1.py <file_path>")
    else:
        main()