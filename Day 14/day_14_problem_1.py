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
    robots_info = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            pattern = r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)'
            match = re.search(pattern, line)
            if match:
                p1, p2, v1, v2 = match.groups()
                p1, p2, v1, v2 = int(p1), int(p2), int(v1), int(v2)
                print(p1, p2, v1, v2)  # Output: 10 66 -15 38
                initial_position = p1 + p2 * 1j
                velocity = v1 + v2 * 1j
                robots_info.append((initial_position, velocity))
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

def main():
    start_time = time.time()
    file_path = sys.argv[1]
    robots_inputs = get_robots_info(file_path)
    final_robot_positions = [robot_update(robot, 100) for robot in robots_inputs]
    # min_row = min([robot.imag for robot in final_robot_positions])
    # max_row = max([robot.imag for robot in final_robot_positions])
    # min_col = min([robot.real for robot in final_robot_positions])
    # max_col = max([robot.real for robot in final_robot_positions])
    num_robots = len(final_robot_positions)
    print(f"Number of robots: {num_robots}")
    middle_row_num = 51
    middle_col_num = 50
    # print(f"Min Row: {min_row}")    
    # print(f"Max Row: {max_row}")
    # print(f"Min Col: {min_col}")
    # print(f"Max Col: {max_col}")
    #print(f"Final Robot Positions: {final_robot_positions}")
    upper = [robot for robot in final_robot_positions if robot.imag < middle_row_num]
    lower = [robot for robot in final_robot_positions if robot.imag > middle_row_num]
    # print(f"Upper: {upper}, Num: {len(upper)}")
    # print(f"Lower: {lower}, Num: {len(lower)}")
    # print(f"Max im in upper: {max([robot.imag for robot in upper])}")
    # print(f"Min im in lower: {min([robot.imag for robot in lower])}")
    upper_left = [robot for robot in upper if robot.real < middle_col_num]
    upper_right = [robot for robot in upper if robot.real > middle_col_num]
    lower_left = [robot for robot in lower if robot.real < middle_col_num]
    lower_right = [robot for robot in lower if robot.real > middle_col_num]
    middle_boundary_items = [robot for robot in final_robot_positions if robot.real == middle_col_num or robot.imag == middle_row_num]
    # print(f"Upper Left: {upper_left}")
    # print(f"Upper Right: {upper_right}")
    # print(f"Lower Left: {lower_left}")
    # print(f"Lower Right: {lower_right}")
    # print(f"Middle Boundary Items: {middle_boundary_items}")
    count_ur = len(upper_right)
    #print(f"Count UR: {count_ur}")
    count_ll = len(lower_left)
    #print(f"Count LL: {count_ll}")
    count_ul = len(upper_left)
    #print(f"Count UL: {count_ul}")
    count_lr = len(lower_right)
    #print(f"Count LR: {count_lr}")
    sum = count_ur + count_ll + count_ul + count_lr
    #print(f"Sum: {sum}")
    product = count_ur * count_ll * count_ul * count_lr
    print(f"Product: {product}")
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time}")    



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_12_problem_1.py <file_path>")
    else:
        main()