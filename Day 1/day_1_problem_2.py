import sys

def extract_columns(file_path):
    column1 = []
    column2 = []

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()  # Split by any whitespace (spaces or tabs)
            if len(parts) == 2:
                column1.append(int(parts[0]))
                column2.append(int(parts[1]))

    return column1, column2

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_1_problem_1.py <file_path>")
    else:
        file_path = sys.argv[1]
        col1, col2 = extract_columns(file_path)
        # col1.sort()
        # col2.sort()
        # print("Column 1:", col1)
        # print("Column 2:", col2)
        similarity_score = sum([value * col2.count(value) for value in col1])
        print("Similarity:", similarity_score)