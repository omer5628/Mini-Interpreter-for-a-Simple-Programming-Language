#omer vazana, id:318870102
#bar sonego , id:318678943
#ron benjamin , id:323906024
#Rachel yeholashet, id:207574203
import ast
import math
from functools import reduce

class Interpreter:
    def __init__(self):
        """Initialize the interpreter with an empty environment and operation mappings."""
        self.env = {}
        self.operations = {
            ast.Add: lambda a, b: a + b,
            ast.Sub: lambda a, b: a - b,
            ast.Mult: lambda a, b: a * b,
            ast.Div: lambda a, b: self.safe_divide(a, b),
            ast.Gt: lambda a, b: a > b,
            ast.Lt: lambda a, b: a < b,
            ast.Eq: lambda a, b: a == b,
            ast.GtE: lambda a, b: a >= b,
            ast.LtE: lambda a, b: a <= b,
            ast.NotEq: lambda a, b: a != b,
            ast.And: lambda a, b: a and b,
            ast.Or: lambda a, b: a or b,
            'sqrt': math.sqrt,
            ast.Mod: lambda a, b: a % b,
            ast.Pow: lambda a, b: a ** b,
            ast.FloorDiv: lambda a, b: a // b,
            'add': self.add,
            'sub': self.sub,
            'mul': self.mul,
            'div': self.div,
        }

    def safe_divide(self, a, b):
        """Safely perform division and handle division by zero."""
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return a / b

    def add(self, *args):
        if len(args) < 2:
            raise ValueError("The 'add' function requires at least two arguments.")
        return reduce(lambda x, y: x + y, args)


    def sub(self, *args):
        """Subtract multiple numbers. If only one argument is provided, return its negation."""
        if len(args) == 0:
            raise ValueError("The 'sub' function requires at least one argument.")
        elif len(args) == 1:
            return -args[0]
        else:
            return reduce(lambda x, y: x - y, args)

    def mul(self, *args):
        """Multiply multiple numbers."""
        if len(args) < 2:
            raise ValueError("The 'mul' function requires at least two arguments.")
        return reduce(lambda x, y: x * y, args)

    def div(self, *args):
        """Divide numbers. Requires at least two arguments."""
        if len(args) < 2:
            raise ValueError("The 'div' function requires at least two arguments.")
        return reduce(self.safe_divide, args)

    def execute(self, node):
        """Execute an AST node and return the result."""
        try:
            if isinstance(node, ast.Constant):
                return node.value  # Return constant value

            elif isinstance(node, ast.Name):
                return self.env.get(node.id)  # Retrieve variable value

            elif isinstance(node, ast.UnaryOp):
                op = node.op
                operand = self.execute(node.operand)
                if isinstance(op, ast.USub):
                    return -operand
                elif isinstance(op, ast.UAdd):
                    return +operand
                elif isinstance(op, ast.Not):
                    return not operand

            elif isinstance(node, ast.BinOp):
                return self.operations[type(node.op)](
                    self.execute(node.left),
                    self.execute(node.right)
                )

            elif isinstance(node, ast.BoolOp):
                values = [self.execute(val) for val in node.values]
                return reduce(self.operations[type(node.op)], values)

            elif isinstance(node, ast.Compare):
                left = self.execute(node.left)
                for op, right in zip(node.ops, node.comparators):
                    if not self.operations[type(op)](left, self.execute(right)):
                        return False
                    left = self.execute(right)
                return True

            elif isinstance(node, ast.Assign):
                value = self.execute(node.value)
                for target in node.targets:
                    self.assign(target, value)
                return value

            elif isinstance(node, ast.If):
                if self.execute(node.test):
                    return self.process_body(node.body)
                elif node.orelse:
                    return self.process_body(node.orelse)

            elif isinstance(node, ast.For):
                for elem in self.execute(node.iter):
                    self.env[node.target.id] = elem
                    self.process_body(node.body)
                return None

            elif isinstance(node, ast.While):
                while self.execute(node.test):
                    self.process_body(node.body)

            elif isinstance(node, ast.Attribute):
                obj = self.execute(node.value)
                return getattr(obj, node.attr)

            elif isinstance(node, ast.Call):
                func = self.execute(node.func)
                args = [self.execute(arg) for arg in node.args]

                if callable(func):
                    # If it's a callable function, call it
                    return func(*args)
                elif isinstance(func, ast.FunctionDef):
                    # If it's a function definition, call it
                    local_env = dict(self.env)
                    for arg_name, arg_value in zip(func.args.args, args):
                        local_env[arg_name.arg] = arg_value
                    return self.execute_function(func, local_env)

            elif isinstance(node, ast.FunctionDef):
                self.env[node.name] = node  # Store the function definition

            elif isinstance(node, ast.Return):
                return self.execute(node.value)

            elif isinstance(node, ast.List):
                return [self.execute(el) for el in node.elts]

            elif isinstance(node, ast.Tuple):
                return tuple(self.execute(el) for el in node.elts)

            elif isinstance(node, ast.Dict):
                return {self.execute(key): self.execute(value) for key, value in zip(node.keys, node.values)}

            elif isinstance(node, ast.Subscript):
                obj = self.execute(node.value)
                if isinstance(node.slice, ast.Index):
                    index = self.execute(node.slice.value)
                elif isinstance(node.slice, ast.Slice):
                    lower = self.execute(node.slice.lower) if node.slice.lower else None
                    upper = self.execute(node.slice.upper) if node.slice.upper else None
                    step = self.execute(node.slice.step) if node.slice.step else None
                    index = slice(lower, upper, step)
                else:
                    index = self.execute(node.slice)
                return obj[index]

            elif isinstance(node, ast.Slice):
                lower = self.execute(node.lower) if node.lower else None
                upper = self.execute(node.upper) if node.upper else None
                step = self.execute(node.step) if node.step else None
                return slice(lower, upper, step)

            elif isinstance(node, ast.AugAssign):
                target = node.target
                value = self.execute(node.value)
                op = type(node.op)
                if isinstance(target, ast.Name):
                    cur_val = self.env.get(target.id, 0)
                    new_val = self.operations[op](cur_val, value)
                    self.env[target.id] = new_val
                    return new_val
                elif isinstance(target, ast.Subscript):
                    obj = self.execute(target.value)
                    idx = self.execute(target.slice.value) if isinstance(target.slice, ast.Index) else self.execute(
                        target.slice)
                    cur_val = obj[idx]
                    new_val = self.operations[op](cur_val, value)
                    obj[idx] = new_val
                    return new_val
                else:
                    raise TypeError(f"Unsupported target type: {type(target)}")

            elif isinstance(node, ast.Expr):
                return self.execute(node.value)

            else:
                raise TypeError(f"Unsupported node type: {type(node)}")
        except Exception as e:
            print(f"Error occurred: {e}")
            return None

    def execute_function(self, func_node, local_env):
        """Execute a function node in its own environment."""
        old_env = self.env
        self.env = local_env
        try:
            result = self.process_body(func_node.body)
            return result
        finally:
            self.env = old_env

    def assign(self, target, value):
        """Assign a value to a target variable or subscript."""
        if isinstance(target, ast.Name):
            self.env[target.id] = value
        elif isinstance(target, ast.Subscript):
            obj = self.execute(target.value)
            if isinstance(target.slice, ast.Index):
                idx = self.execute(target.slice.value)
            elif isinstance(target.slice, ast.Slice):
                lower = self.execute(target.slice.lower) if target.slice.lower else None
                upper = self.execute(target.slice.upper) if target.slice.upper else None
                step = self.execute(target.slice.step) if target.slice.step else None
                idx = slice(lower, upper, step)
            else:
                idx = self.execute(target.slice)
            obj[idx] = value
        else:
            raise TypeError(f"Unsupported assignment target: {type(target)}")

    def process_body(self, body):
        """Process a sequence of statements and return the result of the last one."""
        result = None
        for stmt in body:
            result = self.execute(stmt)
            if isinstance(stmt, ast.Return):
                return result
        return result

    def parse_and_run(self, code):
        """Parse and execute a string of code."""
        tree = ast.parse(code)
        return self.process_body(tree.body)

    def repl(self):
        """Start an interactive REPL session."""
        print("Custom Interpreter REPL. Type 'exit' to quit.")
        while True:
            try:
                code = input(">>> ")
                if code.lower() in ["exit", "quit"]:
                    break
                result = self.parse_and_run(code)
                if result is not None:
                    print(result)
            except Exception as e:
                print(f"Error: {e}")


# Set up the environment
interpreter1 = Interpreter()
interpreter1.env.update({
    'math': math,
    'print': print,
    'len': len,
    'str': str,
    'int': int,
    'float': float,
    'list': list,
    'tuple': tuple,
    'dict': dict,
    'bool': bool,
    'range': range,
    'sum': sum,
    'min': min,
    'max': max,
    'add': interpreter1.add,
    'sub': interpreter1.sub,
    'mul': interpreter1.mul,
    'div': interpreter1.div,
})

def run_tests():
    """
    Run a series of unit tests to validate the interpreter's functionality.
    """
    tests = [
        {
            "input": "a = 10\nb = 5\nc = a + b * 2\nc",
            "expected": 20
        },
        {
            "input": "x = 10\ny = x / 2\ny",
            "expected": 5.0
        },
        {
            "input": "x = 10\ny = x // 3\ny",
            "expected": 3
        },
        {
            "input": "a = [1, 2, 3]\na.append(4)\na",
            "expected": [1, 2, 3, 4]
        },
        {
            "input": "a = (1, 2, 3)\na[0]",
            "expected": 1
        },
        {
            "input": "d = {'key': 'value'}\nd['key']",
            "expected": 'value'
        },
        {
            "input": "def square(x):\n    return x ** 2\ns = square(5)\ns",
            "expected": 25
        },
        {
            "input": "def greet(name):\n    return 'Hello, ' + name\ng = greet('Alice')\ng",
            "expected": 'Hello, Alice'
        },
        {
            "input": "def add(x, y):\n    return x + y\nresult = add(2, 3)\nresult",
            "expected": 5
        },
        {
            "input": "def factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n - 1)\nresult = factorial(4)\nresult",
            "expected": 24
        },
        {
            "input": "a = 10\nb = 0\nc = a / b",
            "expected_exception": ZeroDivisionError
        }
    ]

    for test in tests:
        print(f"Running test: {test['input']}")
        try:
            result = interpreter1.parse_and_run(test["input"])

            if "expected" in test:
                assert result == test["expected"], f"Failed: {test['input']}. Expected {test['expected']}, got {result}"
                print(f"Passed: {test['input']} - Result: {result}")

            elif "expected_exception" in test:
                print(f"Failed: {test['input']}. Expected exception {test['expected_exception']}, but no exception was raised.")

        except Exception as e:
            if "expected_exception" in test:
                assert isinstance(e, test["expected_exception"]), f"Failed: {test['input']}. Expected {test['expected_exception']}, got {type(e)}"
                print(f"Passed: {test['input']} - Expected Exception: {type(e)}")
            else:
                print(f"Unexpected Error: {e}")
                print(f"Failed: {test['input']}. Expected {test.get('expected', 'no error')}, got Error: {e}")

    print("All tests passed.")

if __name__ == "__main__":
    example_code = """
# Arithmetic and assignment
a = 10
b = 5
c = a + b * 2

# Unary operations
print("Not True:", not True)

# Conditionals
if c > 20:
    print("c is greater than 20")
else:
    print("c is not greater than 20")

# Loops and lists
nums = [1, 2, 3, 4, 5]
squares = []
for n in nums:
    squares.append(n ** 2)
print("Squares:", squares)

# While loop
counter = 0
while counter < 5:
    print(counter)
    counter += 1

# Dictionary usage
person = {"name": "bar", "age": 25}
print("Person:", person)

# Tuple usage
coords = (10, 20)
print("Coordinates:", coords)

# String operations
greeting = "Hello, " + person["name"] + "!"
print(greeting)

# Built-in functions
print("Length of squares:", len(squares))
print("Sum of squares:", sum(squares))

# Slicing
print("First three squares:", squares[:3])

# Boolean operations
is_adult = person["age"] >= 18 and person["name"] != ""
print("Is adult:", is_adult)
# Function definition
def add(x, y):
    z = x + y
    return z

result = add(2, 3)
print("result func:", result)

    """

    print("\nRunning example code:")
    interpreter1.parse_and_run(example_code)

    print("\nRunning unit tests:")
    run_tests()

    interpreter1.repl()
