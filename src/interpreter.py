"""Interpreter for the Toy Language.

This module evaluates the AST and executes the program.
"""

from .ast_nodes import (
    Assignment,
    ASTNode,
    BinaryOp,
    Block,
    Boolean,
    ExpressionStatement,
    FunctionCall,
    FunctionDef,
    IfStatement,
    Nil,
    Number,
    Program,
    ReturnStatement,
    String,
    UnaryOp,
    VarDeclaration,
    Variable,
    WhileStatement,
)
from .environment import Environment, Function, ReturnException, RuntimeValue


class Interpreter:
    """Evaluates the AST and executes the program."""

    def __init__(self) -> None:
        self.global_env = Environment()
        self._setup_builtins()

    def _setup_builtins(self) -> None:
        """Define built-in functions."""
        self.global_env.define("print", self._builtin_print)

    def _builtin_print(self, *args: RuntimeValue) -> None:
        """Built-in print function."""
        output = " ".join(self._value_to_string(arg) for arg in args)
        print(output)

    def _value_to_string(self, value: RuntimeValue) -> str:
        """Convert a runtime value to a string representation."""
        if value is None:
            return "nil"
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, float):
            # Display integers without decimal point
            if value.is_integer():
                return str(int(value))
            return str(value)
        elif isinstance(value, str):
            # Handle escape sequences in strings
            return value.encode().decode('unicode_escape')
        elif isinstance(value, Function):
            return repr(value)
        else:
            return str(value)

    def _is_truthy(self, value: RuntimeValue) -> bool:
        """Determine if a value is truthy."""
        return not (value is None or value is False)

    def interpret(self, ast: Program) -> None:
        """Interpret a program."""
        self.eval_program(ast, self.global_env)

    def eval_program(self, node: Program, env: Environment) -> None:
        """Evaluate a program node."""
        for statement in node.statements:
            self.eval(statement, env)

    def eval(self, node: ASTNode, env: Environment) -> RuntimeValue:
        """Evaluate an AST node."""
        if isinstance(node, (Number, String, Boolean)):
            return node.value

        elif isinstance(node, Nil):
            return None

        elif isinstance(node, Variable):
            return env.get(node.name)

        elif isinstance(node, BinaryOp):
            return self.eval_binary_op(node, env)

        elif isinstance(node, UnaryOp):
            return self.eval_unary_op(node, env)

        elif isinstance(node, VarDeclaration):
            value = self.eval(node.value, env)
            env.define(node.name, value)
            return None

        elif isinstance(node, Assignment):
            value = self.eval(node.value, env)
            env.set(node.name, value)
            return None

        elif isinstance(node, Block):
            return self.eval_block(node, env)

        elif isinstance(node, IfStatement):
            return self.eval_if(node, env)

        elif isinstance(node, WhileStatement):
            return self.eval_while(node, env)

        elif isinstance(node, ReturnStatement):
            value = self.eval(node.value, env) if node.value else None
            raise ReturnException(value)

        elif isinstance(node, ExpressionStatement):
            return self.eval(node.expression, env)

        elif isinstance(node, FunctionDef):
            func = Function(node.name, node.parameters, node.body, env)
            env.define(node.name, func)
            return None

        elif isinstance(node, FunctionCall):
            return self.eval_function_call(node, env)

        else:
            raise RuntimeError(f"Unknown node type: {type(node)}")

    def _check_numeric_operands(
        self, operator: str, left: RuntimeValue, right: RuntimeValue
    ) -> tuple[float, float]:
        """Verify operands are numeric and return them, or raise TypeError."""
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise TypeError(f"Cannot {operator} {type(left).__name__} and {type(right).__name__}")
        return left, right

    def eval_binary_op(self, node: BinaryOp, env: Environment) -> RuntimeValue:
        """Evaluate a binary operation."""
        left = self.eval(node.left, env)
        right = self.eval(node.right, env)

        if node.operator == "+":
            if isinstance(left, str) or isinstance(right, str):
                # String concatenation
                return self._value_to_string(left) + self._value_to_string(right)
            left_num, right_num = self._check_numeric_operands("add", left, right)
            return left_num + right_num

        elif node.operator == "-":
            left_num, right_num = self._check_numeric_operands("subtract", left, right)
            return left_num - right_num

        elif node.operator == "*":
            left_num, right_num = self._check_numeric_operands("multiply", left, right)
            return left_num * right_num

        elif node.operator == "/":
            left_num, right_num = self._check_numeric_operands("divide", left, right)
            if right_num == 0:
                raise ZeroDivisionError("Division by zero")
            return left_num / right_num

        elif node.operator == "<":
            left_num, right_num = self._check_numeric_operands("compare", left, right)
            return left_num < right_num

        elif node.operator == ">":
            left_num, right_num = self._check_numeric_operands("compare", left, right)
            return left_num > right_num

        elif node.operator == "==":
            return left == right

        elif node.operator == "!=":
            return left != right

        else:
            raise RuntimeError(f"Unknown binary operator: {node.operator}")

    def eval_unary_op(self, node: UnaryOp, env: Environment) -> RuntimeValue:
        """Evaluate a unary operation."""
        operand = self.eval(node.operand, env)

        if node.operator == "-":
            if isinstance(operand, (int, float)):
                return -operand
            else:
                raise TypeError(f"Cannot negate {type(operand).__name__}")
        else:
            raise RuntimeError(f"Unknown unary operator: {node.operator}")

    def eval_block(self, node: Block, env: Environment) -> RuntimeValue:
        """Evaluate a block of statements."""
        # Blocks don't create new scopes - they use the current environment
        # (function calls and other constructs manage their own scopes)
        result: RuntimeValue = None
        for statement in node.statements:
            result = self.eval(statement, env)
        return result

    def eval_if(self, node: IfStatement, env: Environment) -> RuntimeValue:
        """Evaluate an if statement."""
        condition = self.eval(node.condition, env)

        if self._is_truthy(condition):
            return self.eval(node.then_block, env)
        elif node.else_block:
            return self.eval(node.else_block, env)

        return None

    def eval_while(self, node: WhileStatement, env: Environment) -> RuntimeValue:
        """Evaluate a while loop."""
        while True:
            condition = self.eval(node.condition, env)
            if not self._is_truthy(condition):
                break
            self.eval(node.body, env)

        return None

    def eval_function_call(self, node: FunctionCall, env: Environment) -> RuntimeValue:
        """Evaluate a function call."""
        func = env.get(node.name)

        # Evaluate arguments
        args = [self.eval(arg, env) for arg in node.arguments]

        # Check if it's a built-in function
        if callable(func) and not isinstance(func, Function):
            return func(*args)

        # User-defined function
        if not isinstance(func, Function):
            raise TypeError(f"'{node.name}' is not a function")

        # Check argument count
        if len(args) != len(func.parameters):
            raise TypeError(
                f"{func.name}() takes {len(func.parameters)} arguments but {len(args)} were given"
            )

        # Create new environment for function execution
        func_env = Environment(parent=func.closure)

        # Bind parameters to arguments
        for param, arg in zip(func.parameters, args, strict=True):
            func_env.define(param, arg)

        # Execute function body
        try:
            self.eval(func.body, func_env)
            return None  # If no explicit return, return nil
        except ReturnException as ret:
            return ret.value
