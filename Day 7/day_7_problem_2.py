import sys
from itertools import product

operators = ['+', '*', "||"]
# operators = ['+', '*']

def process_string(input_string):
    # Split the string at the colon
    parts = input_string.split(':')
    # Extract the number before the colon and convert it to an integer
    answer = int(parts[0].strip())
    # Extract the numbers after the colon, split by spaces, and convert to a list of integers
    inputs_without_operators = list(map(int, parts[1].strip().split()))
    return answer, inputs_without_operators

def generate_operator_sequences(num_operators, operators):
    return product(operators, repeat=num_operators)

def perform_computation(num1, num2, operator):
    if operator == '+':
        return num1 + num2
    elif operator == '*':
        return num1 * num2
    elif operator == "||":
        return int(str(num1)+str(num2))

def evaluate_expression(inputs_list, operator_list, accumulated_value):
    first_number = inputs_list[0]
    first_operator = operator_list[0]
    accumulated_value = perform_computation(accumulated_value, first_number, first_operator)
    if len(inputs_without_operators) == 1:
        return accumulated_value
    else:
        return evaluate_expression(inputs_list[1:], operator_list[1:], accumulated_value)


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
                operator_combinations = generate_operator_sequences(len(inputs_without_operators) - 1, operators)
                for operator_combination in operator_combinations:
                    operator_list = list(operator_combination)
                    first_number = inputs_without_operators[0]
                    current_answer = evaluate_expression(inputs_without_operators[1:], operator_list, first_number)
                    if current_answer == answer:
                        total += answer
                        break
        print(total)
