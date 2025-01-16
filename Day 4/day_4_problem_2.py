import sys

# (1,-1): down-left, (-1,-1): up-left, (-1,1): up-right, (1,1): down-right
offsets = [(1, -1), (-1, -1), (-1, 1),  (1, 1)]
# same as offsets, clockwise from lower left
target_neighbor_sets =[
    ['M','M','S','S'],
    ['S','M','M','S'],
    ['S','S','M','M'],
    ['M','S','S','M']
]

# returns board as 2d array
def get_board(file_path):
    board = []
    with open(file_path, 'r') as file:
        for row in file:
            row = row.strip()
            row = list(row)
            board.append(row)
    return board

# returns row,col pairs for all 'A' characters, 
# in order, from upper left to lower right
def find_a_positions(board):
    positions = []
    for row_index, row in enumerate(board):
        for col_index, char in enumerate(row):
            if char == 'A':
                positions.append((row_index, col_index))
    return positions

def count_xmas(board, a_positions):
    xmas_count = 0
    for pos in a_positions:
        row, col = pos
        # Skip checking if 'A' is on the edge
        if row == 0 or row == len(board) - 1 or col == 0 or col == len(board[0]) - 1:
            continue
        # What are the values of the 4 corner neighbors of 'A'?, going from 
        # lower left to lower right, clockwise
        corner_neighbor_values = [board[row + offset[0]][col + offset[1]] for offset in offsets]
        if corner_neighbor_values in target_neighbor_sets:
            xmas_count += 1
    return xmas_count


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_2_problem_1.py <file_path>")
    else:
        xmas_count = 0
        file_path = sys.argv[1]
        board = get_board(file_path)
        a_positions = find_a_positions(board)
        xmas_count = count_xmas(board, a_positions)
        print("Xmas count:", xmas_count)
        #print(x_positions)
