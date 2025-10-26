# Toy Programming Language

A minimal imperative programming language with functions, variables, and basic control flow. This language is designed as a learning project for understanding lexing, parsing, and evaluation.

## Features

- Variables with `let` declarations
- Functions with parameters and return values
- Control flow: `if/else`, `while`
- Data types: numbers, strings, booleans, nil
- Operators: arithmetic (+, -, *, /), comparison (<, >, ==, !=)
- Comments with `//`

## Syntax Guide

### Variables

Variables must be declared with `let` before use:

```
let x = 10;
let name = "Alice";
let is_ready = true;
```

You can reassign variables after declaration:

```
x = 20;
name = "Bob";
```

### Data Types

**Numbers**: Integers and floats
```
let integer = 42;
let decimal = 3.14;
let negative = -17;
```

**Strings**: Text in single or double quotes
```
let greeting = "Hello, World!";
let message = 'Single quotes work too';
```

**Booleans**: `true` and `false`
```
let is_active = true;
let is_completed = false;
```

**Nil**: Represents absence of a value
```
let nothing = nil;
```

### Operators

**Arithmetic**: `+`, `-`, `*`, `/`
```
let sum = 10 + 5;
let difference = 10 - 5;
let product = 10 * 5;
let quotient = 10 / 5;
```

**Comparison**: `<`, `>`, `==`, `!=`
```
let is_greater = 10 > 5;
let is_equal = 10 == 10;
let is_not_equal = 10 != 5;
let is_less = 5 < 10;
```

### Functions

Define functions with the `fn` keyword:

```
fn greet(name) {
    return "Hello, " + name;
}

fn add(a, b) {
    return a + b;
}

fn no_params() {
    return 42;
}
```

Call functions with parentheses:

```
let result = add(5, 3);
let message = greet("Alice");
```

### Control Flow

**If/Else**:
```
if (x > 10) {
    print("x is greater than 10");
} else {
    print("x is 10 or less");
}
```

**While Loop**:
```
let i = 0;
while (i < 5) {
    print(i);
    i = i + 1;
}
```

## Example Programs

### Factorial Function

```
fn factorial(n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

let result = factorial(5);
print(result);  // 120
```

### Count to Ten

```
let i = 1;
while (i < 11) {
    print(i);
    i = i + 1;
}
```

### Sum of Numbers

```
fn sum_to_n(n) {
    let total = 0;
    let i = 1;
    while (i < n + 1) {
        total = total + i;
        i = i + 1;
    }
    return total;
}

let result = sum_to_n(10);
print(result);  // 55
```

### Fibonacci Sequence

```
fn fibonacci(n) {
    if (n < 2) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

let i = 0;
while (i < 10) {
    print(fibonacci(i));
    i = i + 1;
}
```

### Maximum of Two Numbers

```
fn max(a, b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

let result = max(42, 17);
print(result);  // 42
```

### Temperature Converter

```
fn celsius_to_fahrenheit(celsius) {
    return celsius * 9 / 5 + 32;
}

fn fahrenheit_to_celsius(fahrenheit) {
    return (fahrenheit - 32) * 5 / 9;
}

let temp_c = 25;
let temp_f = celsius_to_fahrenheit(temp_c);
print("25°C is " + temp_f + "°F");

let temp_f2 = 77;
let temp_c2 = fahrenheit_to_celsius(temp_f2);
print("77°F is " + temp_c2 + "°C");
```

## Implementation

This repository includes a fully functional interpreter written in Python with complete type hints:

### Architecture

- **[ast_nodes.py](ast_nodes.py)** - AST node definitions using dataclasses
- **[environment.py](environment.py)** - Variable scoping and function closures
- **[interpreter.py](interpreter.py)** - Parser transformer (ASTBuilder) and interpreter (Interpreter)
- **[main.py](main.py)** - Entry point with example program
- **[grammar.lark](grammar.lark)** - Lark grammar specification

### Features Implemented

✅ **Parse**: Lark parser with grammar-based AST generation
✅ **Evaluate**: Full AST evaluation with proper type checking
✅ **Environment**: Lexical scoping with closure support
✅ **Built-ins**: Built-in `print()` function
✅ **Error Handling**: Type errors, name errors, division by zero
✅ **Type Safety**: Full mypy strict mode compliance with no `Any` types
✅ **Code Quality**: Formatted and linted with Ruff

### Running the Interpreter

```bash
# Install dependencies
pip install -r requirements.txt

# Run the example program
python main.py
```

### Development Tools

The project includes linting and formatting configured in [pyproject.toml](pyproject.toml):

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type check
mypy .
```

### Example Program

The interpreter can execute programs like this:

```python
// Factorial function
fn factorial(n) {
    if (n < 2) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

let result = factorial(5);
print("Factorial of 5 is:");
print(result);  // Output: 120
```

### Possible Extensions

- Add `for` loops for convenience
- Add arrays/lists for data collections
- Add more operators (%, <=, >=, &&, ||, !)
- String interpolation
- More data types (objects/dictionaries)
- Lambda functions
- Import/module system
- Classes and objects
- Exception handling (try/catch)
- Break and continue statements
