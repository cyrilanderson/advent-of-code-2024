import sys
import time
import re


def read_input(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Split the content into groups using blank lines as delimiters
    groups = content.strip().split('\n\n')

    # Process each group
    keys_and_locks = []
    for group in groups:
        lines = group.strip().split('\n')
        if len(lines) != 7:
            print(f"Warning: Found a group with {len(lines)} lines instead of 7.")
        else:
            keys_and_locks.append(lines)
    locks = [item for item in keys_and_locks if item[0] == "#####"]
    keys = [item for item in keys_and_locks if item[0] == "....."]

    # for lock in locks:
    #     print(lock)

    # for key in keys:
    #     print(key)
    return keys, locks

def convert_to_num_list(key_or_lock):
    num_list = [0, 0, 0, 0, 0]
    for row in key_or_lock:
        for idx, char in enumerate(row):
            if char == "#":
                num_list[idx] += 1
    return num_list

def evaluate_keys_locks(keys, locks):
    matches = 0
    for lock in locks:
        lock_num_list = convert_to_num_list(lock)
        for key in keys:
            key_num_list = convert_to_num_list(key)
            compare = [lock_num_list[idx] + key_num_list[idx] <= 7 for idx in range(5)]
            if all(compare):
                matches += 1
    return matches

def main():
    start_time = time.time()
    file_path = sys.argv[1]
    keys, locks = read_input(file_path)
    matches = evaluate_keys_locks(keys, locks)
    print(f"Matches: {matches}")
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_17_problem_1.py <file_path>")
    else:
        main()