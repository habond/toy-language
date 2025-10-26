"""Main entry point for the Toy Language interpreter."""

import sys
from pathlib import Path

from lark import Lark

from src.ast_builder import ASTBuilder
from src.ast_nodes import Program
from src.interpreter import Interpreter


def load_grammar() -> str:
    """Load the grammar file."""
    with open("grammar.lark") as f:
        return f.read()


def run_toy_file(file_path: str) -> None:
    """Run a .toy file."""
    # Check if file exists
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)

    # Check if it's a .toy file
    if path.suffix != ".toy":
        print(f"Warning: File '{file_path}' does not have a .toy extension.", file=sys.stderr)

    # Read the source code
    try:
        with open(path) as f:
            code = f.read()
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}", file=sys.stderr)
        sys.exit(1)

    # Parse the source code
    try:
        grammar = load_grammar()
        parser = Lark(grammar, start="program")
        parse_tree = parser.parse(code)
    except Exception as e:
        print(f"Parse error: {e}", file=sys.stderr)
        sys.exit(1)

    # Build AST
    try:
        ast_builder = ASTBuilder()
        ast = ast_builder.transform(parse_tree)
    except Exception as e:
        print(f"AST build error: {e}", file=sys.stderr)
        sys.exit(1)

    # Interpret
    try:
        interpreter = Interpreter()
        if isinstance(ast, Program):
            interpreter.interpret(ast)
        else:
            raise TypeError(f"Expected Program, got {type(ast)}")
    except Exception as e:
        print(f"Runtime error: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python run.py <file.toy>", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]
    run_toy_file(file_path)


if __name__ == "__main__":
    main()
