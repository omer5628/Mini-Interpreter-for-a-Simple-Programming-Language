# Mini-Interpreter for a Custom Programming Language

## Project Overview
This project involves the design and implementation of a mini-interpreter for a custom programming language using Python. The interpreter demonstrates fundamental principles of syntax, semantics, and interpreter design. It supports variable assignments, arithmetic operations, conditionals, loops, and custom functions, making it a powerful tool for learning and experimentation.

---

## Key Features

### Language Specification
- **Arithmetic Operators:**
  - Addition (`+`), Subtraction (`-`), Multiplication (`*`), Division (`/`), Integer Division (`//`), Modulo (`%`), and Exponentiation (`**`).
- **Logical Operators:**
  - `and`, `or`, `not`.
- **Custom Functions for Operations:**
  - `Add(x, y, ...)` → Addition.
  - `Sub(x, y, ...)` → Subtraction.
  - `Mul(x, y, ...)` → Multiplication.
  - `Div(x, y, ...)` → Division with error handling for division by zero.
- **Variables:**
  - Assign values to variables using the `=` operator.
- **Conditionals:**
  - `if-else` statements for branching.
- **Loops:**
  - `for` and `while` loops.
- **Custom Functions:**
  - Define reusable blocks of code with `def` (similar to Python).

### Execution Modes
1. **Direct Code Execution:**
   - Use the `parse_and_run` method to execute code strings.
2. **Interactive REPL Mode:**
   - Engage with the interpreter interactively using the `repl()` function.

### Error Handling
- The interpreter gracefully handles runtime errors, such as division by zero or invalid function arguments, without terminating the entire program.

---

## Implementation Details

### Design Choices
- **AST-Based Parsing:**
  - Utilized Python's `ast` module to parse and analyze the code into an abstract syntax tree (AST).
  - Facilitates structured and efficient execution.
- **Operator Mapping:**
  - Operators are implemented as a dictionary of lambda functions for modular and extendable design.
- **Dynamic Environment:**
  - Variables and function definitions are stored in a dynamic environment to manage state effectively.

### Challenges
1. **Dynamic Environment Management:**
   - Managing variable scope and custom function definitions required careful handling of context.
2. **Support for AST Nodes:**
   - Extended support for various AST node types, such as `BoolOp`, `BinOp`, `Compare`, etc.
3. **Error Handling:**
   - Ensuring comprehensive error messages for invalid operations while maintaining program flow.

---

## Usage Instructions

### Setup
1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```
2. Navigate to the project directory:
   ```bash
   cd mini-interpreter
   ```
3. Ensure Python is installed (version 3.8 or higher).

### Running the Interpreter
1. **Interactive REPL Mode:**
   ```bash
   python Finalproject.py
   ```
   - Type your custom code interactively.
   - Exit by typing `exit` or `quit`.

2. **Execute Example Code:**
   - Edit the `example_code` string in `Finalproject.py` to include your code.
   - Run the script to see the output.

3. **Run Unit Tests:**
   - Use the `run_tests` function in the script to validate functionality.

---

## Examples
### Example Code
```python
# Arithmetic and assignment
a = 10
b = 5
c = a + b * 2

# Conditionals
if c > 20:
    print("c is greater than 20")
else:
    print("c is not greater than 20")

# Loops and functions
def square(x):
    return x ** 2

squares = []
for i in range(5):
    squares.append(square(i))
print("Squares:", squares)
```

### Example Output
```
c is not greater than 20
Squares: [0, 1, 4, 9, 16]
```

---

## Future Enhancements
1. **Additional Data Types:**
   - Support for advanced data types like multi-dimensional arrays and sets.
2. **Advanced Error Handling:**
   - Enhance error reporting for syntax and runtime issues.
3. **Performance Optimization:**
   - Optimize memory usage for recursive functions and nested loops.
4. **Language Extensions:**
   - Introduce object-oriented features like classes and methods.

---
## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
