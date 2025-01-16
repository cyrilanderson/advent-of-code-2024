import sys
import time

square_types = ['.', '#', '^', 'v', '>', '<'], 

turn_result = {
    '^': '>',
    '>': 'v',
    'v': '<',
    '<': '^'
}

move_directions = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

def get_board(file_path):
    board = []
    with open(file_path, 'r') as file:
        for row in file:
            row = row.strip()
            row = list(row)
            board.append(row)
    # print(board)
    return board

def find_starting_position_and_direction(board):
    for row_index, row in enumerate(board):
        if '^' in row:
            col_index = row.index('^')
            char = '^'
            break
    #print(row_index, col_index, char)
    return row_index, col_index, char

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_2_problem_1.py <file_path>")
    else:
        start_time = time.time()
        file_path = sys.argv[1]
        board = get_board(file_path)
        num_visited = 0
        squares_visited = []
        row, col, direction = find_starting_position_and_direction(board)
        squares_visited.append((row, col))
        done = False
        while not done:
            row_offset, col_offset = move_directions[direction]
            next_row = row + row_offset
            next_col = col + col_offset
            # Next step is off the board
            # Done and don't update num_visited
            if next_row < 0 or next_col < 0 or next_row >= len(board) or next_col >= len(board[0]):
                done = True
            elif board[next_row][next_col] == '#':
                # turn
                # find the direction to turn to
                # Don't update num_visited. Just turn.
                direction = turn_result[direction]
            elif board[next_row][next_col] == '.':
                row = next_row
                col = next_col
                if (row, col) not in squares_visited:
                    squares_visited.append((row, col))
        num_visited = len(squares_visited)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.2f} seconds")    
        print(num_visited)
