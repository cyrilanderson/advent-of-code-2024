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

def get_antinodes_for_pair(square1, square2, antinodes):
    displacement_vector = displacement(square1, square2)
    if not(square2[0] + displacement_vector[0] < 0 or square2[0] + displacement_vector[0] >= len(board)) and not(square2[1] + displacement_vector[1] < 0 or square2[1] + displacement_vector[1] >= len(board[0])):
        antinodes.add((square2[0] + displacement_vector[0], square2[1] + displacement_vector[1]))
    if not(square1[0] - displacement_vector[0] < 0 or square1[0] - displacement_vector[0] >= len(board)) and not(square1[1] - displacement_vector[1] < 0 or square1[1] - displacement_vector[1] >= len(board[0])):
        antinodes.add((square1[0] - displacement_vector[0], square1[1] - displacement_vector[1]))
    return antinodes    

def find_antennas(board):
    antennas = {char: set() for char in antenna_chars_string}
    for row_index, row in enumerate(board):
        for col_index, col in enumerate(row):
            if col in antenna_chars_string:
                antennas[col].add((row_index, col_index))
    return antennas

def main():
    file_path = sys.argv[1]
    board = get_board(file_path)
    antennas_list = find_antennas(board)
    antinodes =set()
    for antenna_type in antennas_list:
        pairs_list = combinations(antennas_list[antenna_type], 2)
        for pair in pairs_list:
            antinodes = get_antinodes_for_pair(pair[0], pair[1], antinodes)
    print(len(antinodes))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_2_problem_1.py <file_path>")
    else:
        main()
        
