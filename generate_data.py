import random
import math

class DataGenerator:
    """
    Generator for data points for natural language arithmetic.
    """
    def __init__(self):
        self.numbers = [
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
        # The order below defines precedence (in ascending order).
        self.operators = [
            {'meaning': ['-'], 'translation': 'minus', 'denotation': lambda x, y: x - y},
            {'meaning': ['+'], 'translation': 'plus', 'denotation': lambda x, y: x + y},
            {'meaning': ['*'], 'translation': 'times', 'denotation': lambda x, y: x * y},
            {'meaning': ['/'], 'translation': 'over', 'denotation': lambda x, y: x // y},
        ]


    def generate_expression(self, num_operations, allowed_operators=None):
        """
        Generates a single expression that contains the given number of operations.
        """
        if num_operations == 0:
            return random.sample(self.numbers, 1)[0]
        # Expressions will be of the type (OP EXP1 EXP2)
        if allowed_operators is None:
            allowed_operators = self.operators
        operator_index = random.randint(0, len(allowed_operators) - 1)
        operator = allowed_operators[operator_index]
        # Decide how many operators will be in each of EXP1 and EXP2
        random_value = random.random()
        num_operations_for_first = int(num_operations * random_value)
        num_operations_for_second = num_operations - num_operations_for_first - 1
        # The operations in the children will be the same as the operator already sampled, or one of a higher
        # precedence.
        first_argument = self.generate_expression(num_operations_for_first,
                                                  allowed_operators[operator_index:])
        second_argument = self.generate_expression(num_operations_for_second,
                                                   allowed_operators[operator_index:])
        return {"meaning": operator["meaning"] + first_argument["meaning"] + second_argument["meaning"],
                "translation": " ".join([first_argument["translation"], operator["translation"],
                                         second_argument["translation"]]),
                "denotation": operator["denotation"](first_argument["denotation"], second_argument["denotation"])}


    def generate_data(self,
                      num_expressions,
                      min_num_operations=1,
                      max_num_operations=10,
                      split_data=False,
                      train_proportion=0.8,
                      test_proportion=0.1):
        """
        Returns ``num_expressions`` expressions, containing number of operations in the range
        ``(min_num_operations, max_num_operations)``. Optionally, you can also have the data split into
        train, test, and dev sets, ans specify their proportions.
        """
        data = []
        while len(data) < num_expressions:
            num_operations = random.randint(min_num_operations, max_num_operations)
            try:
                expression = self.generate_expression(num_operations)
                data.append(expression)
            except ZeroDivisionError:
                pass

        if not split_data:
            return {"data": data}
        test_size = math.ceil(test_proportion * num_expressions)
        if train_proportion + test_proportion < 1.0:
            dev_size = math.ceil((1 - (train_proportion + test_proportion)) * num_expressions)
        else:
            dev_size = 0
        return {"test": data[:test_size],
                "dev": data[test_size:test_size+dev_size],
                "train": data[test_size+dev_size:]}
