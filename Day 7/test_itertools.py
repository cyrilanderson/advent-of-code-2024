from itertools import product

def generate_combinations(num, possibilities):
    return product(possibilities, repeat=num)
    

possibilities = ["*", "+"]
num = 4
for combination in generate_combinations(num, possibilities):
    print(list(combination))
