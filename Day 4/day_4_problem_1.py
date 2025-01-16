import sys

search_chars = ['X', 'M', 'A', 'S']
# (0,1): right, (1,0): down, (0,-1): left, (-1,0): up, 
# (1,1): down-right, (-1,-1): up-left, (1,-1): down-left, (-1,1): up-right
offsets = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

# returns board as 2d array
def get_board(file_path):
    board = []
    with open(file_path, 'r') as file:
        for row in file:
            row = row.strip()
            row = list(row)
            board.append(row)
    return board

# returns row,col pairs for all 'X' characters, 
# in order, from upper left to lower right
def find_x_positions(board):
    positions = []
    for row_index, row in enumerate(board):
        for col_index, char in enumerate(row):
            if char == 'X':
                positions.append((row_index, col_index))
    return positions

def count_xmas(board, x_positions):
    xmas_count = 0
    for pos in x_positions:
        xmas_count += count_xmas_from_pos(board, pos)
    return xmas_count

def count_xmas_from_pos(board, pos):
    xmas_count = 0
    for offset in offsets:
        xmas_count += find_xmas_in_direction(board, pos, offset)
    return xmas_count

def find_xmas_in_direction(board, pos, offset):
    row, col = pos
    row_offset, col_offset = offset
    found = True
    for c in search_chars[1:]:
        row += row_offset
        col += col_offset
        if  row < 0 or col < 0 or row >= len(board) or col >= len(board[0]) or board[row][col] != c:
            found = False
            break
    if found:
        return 1
    else:   
        return 0


# def find_instructions_in_line(line):
#     pattern = r"mul\(\d+,\d+\)|do\(\)|don't\(\)"
#     instructions = re.findall(pattern, line)
#     return instructions


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_2_problem_1.py <file_path>")
    else:
        xmas_count = 0
        file_path = sys.argv[1]
        board = get_board(file_path)
        x_positions = find_x_positions(board)
        xmas_count = count_xmas(board, x_positions)
        print("Xmas count:", xmas_count)
        #print(x_positions)
