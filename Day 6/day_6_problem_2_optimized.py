import sys
import copy
import time

square_types = ['.', '#', '^', 'v', '>', '<'] 

turn_result = {
    'U': 'R',
    'R': 'D',
    'D': 'L',
    'L': 'U'
}

direction_steps = {
    'U': (-1, 0),
    'R': (0, 1),
    'D': (1, 0),
    'L': (0, -1)
}

dir_char_to_direction = {
    '^': 'U',
    '>': 'R',
    'v': 'D',
    '<': 'L'
}

def get_board(file_path):
    board = []
    with open(file_path, 'r') as file:
        for row in file:
            row = row.strip()
            row = list(row)
            board.append(row)
    # for line in board:
    #     print(line)
    # print(board)
    return board

# NOTE: This fails and returns None if there is no direction char in the board
# Would require guard clause to handle this case in proper code
def find_starting_position_and_direction(board):
    for row_index, row in enumerate(board):
        for col_index, col in enumerate(row):
            if col in square_types[2:]:
                #print(col)
                direction = dir_char_to_direction[col]
                return row_index, col_index, direction
    
def rotate_90_degrees_right(direction):
    return turn_result[direction]

# Takes in a board, which is a 2d list of characters
# starting_position_direction is a tuple of the form (row, col)
# Direction is a string of 'U', 'R', 'D', 'L'
# Returns a list of tuples of the form (row, col, direction) representing the route
# This function assumes that the board is a normal board where you will finish by 
# exiting the board, with no loops
def find_default_route(board, starting_position_direction):
    route = []
    row, col, direction = starting_position_direction
    route.append((row, col, direction))
    # start_char = board[row][col]
    exit_board = False
    while not exit_board:
        # Look one step ahead
        row_offset, col_offset = direction_steps[direction]
        next_row = row + row_offset
        next_col = col + col_offset
        # Next step is off the board
        # Done and don't update num_visited
        if next_row < 0 or next_col < 0 or next_row >= len(board) or next_col >= len(board[0]):
            exit_board = True
        elif board[next_row][next_col] == '#':
            # turn
            # find the direction to turn to
            # Don't update num_visited. Just turn.
            direction = rotate_90_degrees_right(direction)
        else:
            row = next_row
            col = next_col
            route.append((row, col, direction))
        # Notes to self. So this is not really the route. If you look closely, 
        # there are steps missing. This is because it only tracks positions and not 
        # directions. And it only notes the first time the position is arrived at
        # And doesn't distinguish the direction of arrival.
        # However, for the simulation, the positions are enough to set the search space for obstacles
        # If you had the full route including directions at each step, it would optimize computation 
        # for the simulation. Instead of simulating from the start, can just enter the steps before the 
        # Have to be careful though, because it would only make sense to use the first time the position 
        # was reached with the first direction.Because the first time it hits the obstacle the path after is different
        # Could compute a list of tuples of the form (row, col, direction_first_visit, step_number) from the full route
    return route

# Runs a simulation trial of trying to find a loop with    
def simulate_trial(board, prior_steps, obstacle_pos):
    visited_positions_directions = set()
    row, col, direction = prior_steps[-1]
    obstacle_row, obstacle_col = obstacle_pos
    # Copy over prior steps before obstacle
    for waypoint in prior_steps:
        visited_positions_directions.add(waypoint)
    exit_board = False
    loop = False
    while not (exit_board or loop):
        row_offset, col_offset = direction_steps[direction]
        next_row = row + row_offset
        next_col = col + col_offset
        # Next step is off the board
        # Done and don't update num_visited
        if (next_row, next_col, direction) in visited_positions_directions:
            loop = True
            break
        elif next_row < 0 or next_col < 0 or next_row >= len(board) or next_col >= len(board[0]):
            exit_board = True
            break
        elif board[next_row][next_col] == '#' or (next_row, next_col) == (obstacle_row, obstacle_col):
            # turn
            # find the direction to turn to
            # Don't update num_visited. Just turn.
            direction = rotate_90_degrees_right(direction)
        else:
            row = next_row
            col = next_col
            visited_positions_directions.add((row, col, direction))
    return loop

# Organizes a route into a dictionary where keys are distinct positions
# and values are lists of tuples of the form (step, direction) where step is the step number
# and direction is the direction of arrival. The lists are in order of different visits to the square
# This dictionary makes it easy to get the number of distinct squares visited with len(dict)
def route_to_distinct_positions(route):
    distinct_positions = {}
    for step, waypoint in enumerate(route):
        row, col, direction = waypoint
        if (row, col) not in distinct_positions:
            distinct_positions[(row, col)] = [(step, direction)]
        else:
            distinct_positions[(row, col)].append((step, direction))
    # print(max([len(visits) for visits in distinct_positions.values()]))
    return distinct_positions


def print_board(board, route):
    new_board = copy.deepcopy(board)
    for row, col in route:
        new_board[row][col] = 'X'
    for line in new_board:
        result_string = ''.join(line)
        print(result_string)
    
def main():
    start_time = time.time()
    file_path = sys.argv[1]
    board = get_board(file_path)
    start_row, start_col, start_direction = find_starting_position_and_direction(board)
    # print(start_row, start_col, start_direction)
    default_route = find_default_route(board, (start_row, start_col, start_direction))
    distinct_positions_visited = route_to_distinct_positions(default_route)
    distinct_positions_wout_start = {position: visit for position, visit in distinct_positions_visited.items() if position != (start_row, start_col)}
    # Should be 5153
    print(len(distinct_positions_visited))
    #print_board(board, default_route)
    num_loops = 0
    for square in distinct_positions_wout_start:
        # Get the step number of the first visit to the square
        step_first_visit, _ = distinct_positions_wout_start[square][0]
        # Copy over the steps of original route up to just before the first visit to the square
        # Those steps from the route will stay the same and don't need to be simulated
        prior_steps = default_route[:step_first_visit]
        loop_sim_result = simulate_trial(board, prior_steps, square)
        if loop_sim_result:
            num_loops += 1
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")    
    # Should be 1711
    print(num_loops)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_2_problem_1.py <file_path>")
    else:
        main()