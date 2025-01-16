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
    route.append((row, col))
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
        elif board[next_row][next_col] == '.':
            row = next_row
            col = next_col
            if (row, col) not in route:
                route.append((row, col))
    return route

# Runs a simulation trial of trying to find a loop with    
def simulate_trial(board, start_pos, starting_dir, obstacle_pos):
    visited_positions_directions = set()
    row, col = start_pos
    direction = starting_dir
    obstacle_row, obstacle_col = obstacle_pos
    start_char = board[row][col]
    visited_positions_directions.add((row, col, direction))
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
        elif board[next_row][next_col] in ['.', start_char]:
            row = next_row
            col = next_col
            if (row, col, direction) not in visited_positions_directions:
                visited_positions_directions.add((row, col, direction))
    return loop

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
    #print_board(board, default_route)
    num_loops = 0
    for square in default_route[1:]:
        loop_sim_result = simulate_trial(board, (start_row, start_col), start_direction, square)
        if loop_sim_result:
            num_loops += 1
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")    
    print(num_loops)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_2_problem_1.py <file_path>")
    else:
        main()