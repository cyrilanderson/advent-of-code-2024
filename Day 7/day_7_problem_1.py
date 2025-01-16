import sys
from itertools import product

operators = ['+', '*']

def process_string(input_string):
    # Split the string at the colon
    parts = input_string.split(':')
    
    # Extract the number before the colon and convert it to an integer
    answer = int(parts[0].strip())
    
    # Extract the numbers after the colon, split by spaces, and convert to a list of integers
    inputs_without_operators = list(map(int, parts[1].strip().split()))
    
    return answer, inputs_without_operators

def operator_combinations_iterator(num_operators, operators):
    return product(operators, repeat=num_operators)

def evaluate_expression(inputs_without_operators, operator_combination):
    current_answer = inputs_without_operators[0]
    for i in range(len(operator_combination)):
        if operator_combination[i] == '+':
            current_answer += inputs_without_operators[i + 1]
        elif operator_combination[i] == '*':
            current_answer *= inputs_without_operators[i + 1]
    return current_answer

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day_7_problem_1.py <file_path>")
    else:
        file_path = sys.argv[1]
        total = 0
        with open(file_path, 'r') as file:
            for row in file:
                row = row.strip()
                answer, inputs_without_operators = process_string(row)
                operator_combinations = operator_combinations_iterator(len(inputs_without_operators) - 1, operators)
                for operator_combination in operator_combinations:
                    current_answer = evaluate_expression(inputs_without_operators, operator_combination)
                    # current_answer = inputs_without_operators[0]
                    # for i in range(len(operator_combination)):
                    #     if operator_combination[i] == '+':
                    #         current_answer += inputs_without_operators[i + 1]
                    #     elif operator_combination[i] == '*':
                    #         current_answer *= inputs_without_operators[i + 1]
                    if current_answer == answer:
                        total += answer
                        break
        print(total)
