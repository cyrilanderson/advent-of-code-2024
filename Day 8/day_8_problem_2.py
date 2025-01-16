import sys
from itertools import combinations

# antenna characters can be uppercase letters, lowercase letters, or digits
antenna_chars_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


def get_board(file_path):
    board = []
    with open(file_path, 'r') as file:
        for row in file:
            row = row.strip()
            board.append(row)
    # print(board)
    return board

def displacement(square1, square2):
    return square2[0] - square1[0], square2[1] - square1[1]

def add_vectors(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]

def get_antinodes_for_pair(square1, square2, antinodes):
    displacement_vector = displacement(square1, square2)
    neg_displacement_vector = (-displacement_vector[0], -displacement_vector[1])
    p1 = (square1[0], square1[1])
    p2 = (square2[0], square2[1])
    # while p1 is on the board
    while not(p1[0] < 0 or p1[0] >= len(board) or p1[1] < 0 or p1[1] >= len(board[0])):
        antinodes.add(p1)
        p1 = add_vectors(p1, neg_displacement_vector)
    # while p2 is on the board
    while not(p2[0] < 0 or p2[0] >= len(board) or p2[1] < 0 or p2[1] >= len(board[0])):
        antinodes.add(p2)
        p2 = add_vectors(p2, displacement_vector)
    return antinodes    

# find all antennas on the board
def find_antennas(board):
    antennas = {char: set() for char in antenna_chars_string}
    for row_index, row in enumerate(board):
        for col_index, col in enumerate(row):
            if col in antenna_chars_string:
                antennas[col].add((row_index, col_index))
    return antennas



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_2_problem_1.py <file_path>")
    else:
        file_path = sys.argv[1]
        board = get_board(file_path)
        antennas_list = find_antennas(board)
        antinodes =set()
        # add antenna pairs to antinodes
        # for antenna_type in antennas_list:
        #     for antenna_coord in antennas_list[antenna_type]:
        #         antinodes.add(antenna_coord)
        # add antinodes on each side for each pair of antennas
        for antenna_type in antennas_list:
            pairs_list = combinations(antennas_list[antenna_type], 2)
            for pair in pairs_list:
                antinodes = get_antinodes_for_pair(pair[0], pair[1], antinodes)
    print(len(antinodes))