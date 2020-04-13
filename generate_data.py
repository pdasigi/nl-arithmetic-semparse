"""
Generates an arbitrary number of data points for natural language arithmetic.
"""
import random


NUMBERS = [
    {'meaning': ['0'], 'translation': 'zero', 'denotation': 0}, 
    {'meaning': ['1'], 'translation': 'one', 'denotation': 1}, 
    {'meaning': ['2'], 'translation': 'two', 'denotation': 2}, 
    {'meaning': ['3'], 'translation': 'three', 'denotation': 3}, 
    {'meaning': ['4'], 'translation': 'four', 'denotation': 4}, 
    {'meaning': ['5'], 'translation': 'five', 'denotation': 5}, 
    {'meaning': ['6'], 'translation': 'six', 'denotation': 6}, 
    {'meaning': ['7'], 'translation': 'seven', 'denotation': 7}, 
    {'meaning': ['8'], 'translation': 'eight', 'denotation': 8}, 
    {'meaning': ['9'], 'translation': 'nine', 'denotation': 9},
]
    
OPERATORS = [
    {'meaning': ['+'], 'translation': 'plus', 'denotation': lambda x, y: x + y},
    {'meaning': ['-'], 'translation': 'minus', 'denotation': lambda x, y: x - y},
    {'meaning': ['*'], 'translation': 'times', 'denotation': lambda x, y: x * y},
    {'meaning': ['/'], 'translation': 'over', 'denotation': lambda x, y: x // y},
]


def count_num_operations(expression):
    num_operations = 0
    for element in expression:
        if element in OPERATORS:
            num_operations += 1
    return num_operations


def generate_data(num_operations):
    if num_operations == 0:
        return random.sample(NUMBERS, 1)[0]
    # Expressions will be of the type (OP EXP1 EXP2)
    # TODO (pradeep): Precedence
    operator = random.sample(OPERATORS, 1)[0]
    # Decide how many operators will be in each of EXP1 and EXP2
    random_value = random.random()
    num_operations_for_first = int(num_operations * random_value)
    num_operations_for_second = num_operations - num_operations_for_first - 1
    first_argument = generate_data(num_operations_for_first)
    second_argument = generate_data(num_operations_for_second)
    return {"meaning": operator["meaning"] + first_argument["meaning"] + second_argument["meaning"],
            "translation": " ".join([first_argument["translation"], operator["translation"],
                                     second_argument["translation"]]),
            "denotation": operator["denotation"](first_argument["denotation"], second_argument["denotation"])}

if __name__ == "__main__":
    data = [generate_data(random.randint(1, 10)) for _ in range(100000)]
