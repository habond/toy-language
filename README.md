# Toy Programming Language

A minimal imperative programming language interpreter with support for functions, closures, variables, and control flow. This project demonstrates the implementation of a complete interpreter pipeline: lexing, parsing, AST construction, and tree-walking evaluation.

Built with Python, Lark parser generator, and comprehensive type hints for educational purposes.

## Features

- Variables with `let` declarations and reassignment
- Functions with parameters, return values, and closures
- Recursive function calls
- Control flow: `if/else` conditionals, `while` loops
- Data types: numbers (float), strings, booleans, nil
- Operators: arithmetic (+, -, *, /), comparison (<, >), equality (==, !=), unary negation (-)
- Single-line comments with `//`
- String concatenation with `+` operator
- Built-in `print()` function with multi-argument support

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

**Numbers**: Integers and floats (stored internally as floats)
```
let integer = 42;
let decimal = 3.14;
let negative = -17;
let expression = -(10 + 5);  // Unary negation
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

### Built-in Functions

**print()**: Outputs values to the console (accepts multiple arguments)

```
print("Hello, World!");
print("Sum:", 10 + 5);
print("Multiple", "arguments", "separated", "by", "spaces");

let x = 42;
print("The answer is", x);  // Output: The answer is 42
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

### Comments

Single-line comments start with `//`:

```
// This is a comment
let x = 42;  // Comments can also go at the end of lines

// Multi-line comments are not supported
// Use multiple single-line comments instead
```

### String Concatenation

Strings can be concatenated using the `+` operator:

```
let name = "Alice";
let greeting = "Hello, " + name + "!";
print(greeting);  // Output: Hello, Alice!

// Numbers are automatically converted to strings when concatenating
let age = 25;
print(name + " is " + age + " years old");
```

## Example Programs

The [examples/](examples/) directory contains working programs that demonstrate various features:

- **[hello_world.toy](examples/hello_world.toy)** - Basic print statement
- **[functions.toy](examples/functions.toy)** - Function definitions and calls
- **[loops.toy](examples/loops.toy)** - While loops and conditionals
- **[fibonacci.toy](examples/fibonacci.toy)** - Recursive and iterative Fibonacci implementations
- **[closures.toy](examples/closures.toy)** - Demonstrates closure and lexical scoping

Below are additional examples showing the language capabilities:

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
print(result);  // Output: 120
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
print(result);  // Output: 55
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
print(result);  // Output: 42
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

### Closures

Functions capture their defining environment, enabling closures:

```
fn make_counter() {
    let count = 0;

    fn increment() {
        count = count + 1;
        return count;
    }

    return increment;
}

let counter = make_counter();
print(counter());  // Output: 1
print(counter());  // Output: 2
print(counter());  // Output: 3
```

## Implementation

This repository includes a fully functional interpreter written in Python with complete type hints:

### Architecture

The interpreter is organized into separate, focused modules following clean architecture principles:

```
toy-language/
├── src/                    # Core interpreter implementation
│   ├── ast_nodes.py       # AST node definitions using dataclasses
│   ├── ast_builder.py     # Transforms Lark parse trees into AST
│   ├── environment.py     # Variable scoping and closures
│   └── interpreter.py     # AST evaluation engine
├── examples/              # Example .toy programs
├── grammar.lark           # Lark grammar specification
├── run.py                 # CLI entry point
└── toy                    # Executable wrapper script
```

**Key Components:**

- **[src/ast_nodes.py](src/ast_nodes.py)** - AST node definitions using dataclasses for type safety
- **[src/ast_builder.py](src/ast_builder.py)** - Transforms Lark parse trees into typed AST nodes
- **[src/environment.py](src/environment.py)** - Variable scoping with lexical closures and function objects
- **[src/interpreter.py](src/interpreter.py)** - AST evaluation engine with runtime execution
- **[grammar.lark](grammar.lark)** - Lark grammar specification defining the language syntax
- **[run.py](run.py)** - Command-line entry point for running .toy files
- **[toy](toy)** - Bash wrapper script that manages virtual environment and runs programs

### Features Implemented

✅ **Parsing**: Lark-based parser with full grammar support
✅ **AST Building**: Type-safe transformation from parse trees to AST
✅ **Evaluation**: Complete AST interpreter with proper semantics
✅ **Lexical Scoping**: Nested environments with closure support
✅ **Functions**: First-class functions with closures
✅ **Built-ins**: `print()` function with multi-argument support
✅ **Error Handling**: Type errors, name errors, division by zero
✅ **Type Safety**: Full mypy strict mode compliance
✅ **Code Quality**: Formatted and linted with Ruff

### Running the Interpreter

The easiest way to run Toy programs is using the `toy` wrapper script:

```bash
# Run a .toy program (automatically sets up venv and dependencies)
./toy examples/hello_world.toy

# Try other examples
./toy examples/fibonacci.toy
./toy examples/closures.toy
```

Alternatively, you can use Python directly:

```bash
# Install dependencies manually
pip install -r requirements.txt

# Run with Python
python3 run.py examples/hello_world.toy
```

### Creating Programs

Create a file with the `.toy` extension and write your program:

```bash
# Create a new program
cat > hello.toy << 'EOF'
let x = 42;
print("The answer is:");
print(x);
EOF

# Run it
./toy hello.toy
```

### Development Tools

The project includes development tools configured in [pyproject.toml](pyproject.toml):

```bash
# Format code
ruff format src/ run.py

# Lint code
ruff check src/ run.py

# Type check
mypy src/ run.py
```

All code passes strict type checking with mypy and follows PEP 8 style guidelines.

### Project Structure

The project follows a clean separation of concerns:

- **Parser Layer** ([grammar.lark](grammar.lark)) - Defines syntax and produces parse trees
- **AST Layer** ([src/ast_nodes.py](src/ast_nodes.py), [src/ast_builder.py](src/ast_builder.py)) - Type-safe abstract syntax tree
- **Runtime Layer** ([src/environment.py](src/environment.py)) - Manages scoping and closures
- **Execution Layer** ([src/interpreter.py](src/interpreter.py)) - Evaluates the AST
- **CLI Layer** ([run.py](run.py), [toy](toy)) - Command-line interface and tooling

### Technical Details

**Parser**: Uses Lark with an LALR(1) parser for efficient parsing of the grammar defined in [grammar.lark](grammar.lark).

**AST Nodes**: All AST nodes are immutable dataclasses defined in [ast_nodes.py](ast_nodes.py), providing type safety and clarity.

**Scoping**: Implements lexical scoping with closures. Functions capture their defining environment, allowing proper closure semantics.

**Type System**: Dynamically typed at runtime but with comprehensive type annotations throughout the codebase. Runtime type checking prevents invalid operations (e.g., cannot add a string and number without explicit conversion).

**Error Messages**: Provides clear error messages for:
- Parse errors (syntax errors)
- Name errors (undefined variables)
- Type errors (invalid operations)
- Zero division errors

**Execution Model**: Tree-walking interpreter that directly evaluates the AST without compilation or bytecode generation.

### Possible Extensions

Potential features for future development:

- **Control Flow**: `for` loops, `break`, `continue` statements
- **Operators**: Modulo `%`, less-than-or-equal `<=`, greater-than-or-equal `>=`, logical AND `&&`, OR `||`, NOT `!`
- **Data Structures**: Arrays/lists, objects/dictionaries, tuples
- **Advanced Functions**: Lambda/anonymous functions, higher-order functions
- **String Features**: String interpolation, escape sequences, multi-line strings
- **Modules**: Import/export system, module namespaces
- **OOP**: Classes, objects, inheritance, methods
- **Error Handling**: Exception handling with try/catch/finally
- **Standard Library**: Math functions, string utilities, file I/O
- **Optimization**: Bytecode compilation, constant folding, tail call optimization

The current implementation provides a solid foundation for adding these features.
