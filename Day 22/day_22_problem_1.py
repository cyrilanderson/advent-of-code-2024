import sys
import time
import re
# import itertools
# import collections

# Relevant powers of two
# 32 = 2**5
# 64 = 2**6
# 2048 = 2**11
# 16777216 = 2**24


def get_initial_values(file_path):
    initial_values = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip()
        initial_values.append(int(line))
    return initial_values
    
# take xor
def mix(num1, num2):
    return num1 ^ num2

# modulo 2**24
def prune(num):
    return num & 0b111111111111111111111111


def generate_secret(initial_value):
    secret = initial_value
    # first step
    secret = mix(secret, secret << 6)
    secret = prune(secret)
    # second step
    secret = mix(secret, secret >> 5)
    secret = prune(secret)
    # third step
    secret = mix(secret, secret << 11)
    secret = prune(secret)
    return secret

def generate_nth_secret(initial_value, n):
    secret = initial_value
    for _ in range(n):
        secret = generate_secret(secret)
    return secret

def main():
    start_time = time.time()
    file_path = sys.argv[1]
    initial_values = get_initial_values(file_path)
    # test = 123
    # test_result = generate_secret(test)
    # print(f"Test result: {test_result}")
    # test_result = generate_secret(test_result)
    # print(f"Next test result: {test_result}")
    secrets = [generate_nth_secret(initial_value, 2000) for initial_value in initial_values]
    total = sum(secrets)
    print(f"Total: {total}")
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_17_problem_1.py <file_path>")
    else:
        main()