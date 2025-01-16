import sys
import time
# import re
# import itertools
# import collections

# Relevant powers of two
# 32 = 2**5
# 64 = 2**6
# 2048 = 2**11
# 16777216 = 2**24

# dict where keys are sequences of 4 consecutive changes and the sum of the prices at the end of
# the first appearances of the sequence across the buyers
sequences_and_prices = {}


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

# This is not yet correct. Need to distinguish between the sequence having appeared before with another buyer vs for the same buyer
# Want only the frust occurence for each buyer but want to keep running total across buyers
def generate_secrets_sequences_prices(initial_value, n):
    sequences_for_this_buyer = set()
    secret = initial_value
    initial_price = secret % 10
    last_four_deltas = []
    last = initial_price
    for _ in range(4):
        secret = generate_secret(secret)
        price = secret % 10
        delta = price - last
        last_four_deltas.append(delta)    
        # Now update last for the next round
        last = price
    # We only want this tuple of deltas to be added to the global dict if it is the first time it appears for this buyer
    # Because only the first appearance counts for triggering a buy
    # We add the sequence to a set of sequences visible with this buyer so it doesn't get counted again
    sequence = tuple(last_four_deltas)
    if sequence not in sequences_for_this_buyer:
        sequences_for_this_buyer.add(sequence)
        if sequence not in sequences_and_prices:
            sequences_and_prices[sequence] = last
        else:
            sequences_and_prices[sequence] += last
    
    for _ in range(n - 4):
        secret = generate_secret(secret)
        price = secret % 10
        delta = price - last
        last_four_deltas.pop(0)
        last_four_deltas.append(delta)
        last = price
        sequence = tuple(last_four_deltas)
        if sequence not in sequences_for_this_buyer:
            sequences_for_this_buyer.add(sequence)
            if sequence not in sequences_and_prices:
                sequences_and_prices[sequence] = last
            else:
                sequences_and_prices[sequence] += last


def main():
    start_time = time.time()
    file_path = sys.argv[1]
    initial_values = get_initial_values(file_path)
    num_buyers = len(initial_values)
    print(f"Number of buyers: {num_buyers}")
    # test = 123
    # test_result = generate_secret(test)
    # print(f"Test result: {test_result}")
    # test_result = generate_secret(test_result)
    # print(f"Next test result: {test_result}")
    for initial_value in initial_values:
        generate_secrets_sequences_prices(initial_value, 2000)
    #secrets = [generate_secrets_sequences_prices(initial_value, 2000) for initial_value in initial_values]
    profit = max(sequences_and_prices.values())
    print(f"Profit: {profit}")
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_17_problem_1.py <file_path>")
    else:
        main()