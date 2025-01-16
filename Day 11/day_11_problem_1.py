import sys
import time
# import itertools
# import collections


def read_input_string(file_path):
    with open(file_path, 'r') as file:
        line = file.readline().strip()
        # split line on spaces
        return line.split()

def is_even_length(string):
    return len(string) % 2 == 0

def remove_leading_zeroes(string):
    while len(string) >= 2 and string[0] == '0':
        string = string[1:]
    return string

def split_even_length_string(string):
    if not is_even_length(string):
        return None
    return [string[:len(string) // 2], string[len(string) // 2:]]

cache = {
    '0': ['1'],
    '1': ['2024'],
    '2': ['4048'],
    '4': ['9196'],
    '2024': ['20', '24'],
    '4048': ['40', '48'],
    '9196': ['91', '96']
}

# returns a list of strings
def blink_single_string(string):
    if string in cache:
        return cache[string]
    elif is_even_length(string):
        splits = split_even_length_string(string)
        splits[1] = remove_leading_zeroes(splits[1])
        result = splits
    else:
        new_string = str(2024 * int(string))
        result = [new_string]
    cache[string] = result
    return result

def blink_string_list(string_list, num_iterations):
    print(f"num_iterations: {num_iterations}")
    result = []
    for string in string_list:
        result.extend(blink_single_string(string))
    if num_iterations > 1:
        return blink_string_list(result, num_iterations - 1)
    return result

def main():
    start_time = time.time()
    file_path = sys.argv[1]
    inputs = read_input_string(file_path)
    #inputs  = ['125', '17']
    iterations = 25
    blinked = blink_string_list(inputs, iterations)
    print(len(blinked))
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")    



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_9_problem_1.py <file_path>")
    else:
        main()