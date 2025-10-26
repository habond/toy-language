"""Environment for variable and function scoping."""

from collections.abc import Callable
from typing import Optional, Union

from ast_nodes import Block

# Type alias for runtime values (includes built-in functions as callables)
RuntimeValue = Union[float, str, bool, None, "Function", Callable[..., "RuntimeValue"]]


class ReturnException(Exception):
    """Exception used to implement return statements."""

    def __init__(self, value: RuntimeValue) -> None:
        self.value = value
        super().__init__()


class Environment:
    """Represents a variable scope with support for nested scopes."""

    def __init__(self, parent: Optional["Environment"] = None) -> None:
        self.parent = parent
        self.values: dict[str, RuntimeValue] = {}

    def define(self, name: str, value: RuntimeValue) -> None:
        """Define a new variable in the current scope."""
        self.values[name] = value

    def get(self, name: str) -> RuntimeValue:
        """Get a variable value, searching parent scopes if needed."""
        if name in self.values:
            return self.values[name]

        if self.parent is not None:
            return self.parent.get(name)

        raise NameError(f"Undefined variable: '{name}'")

    def set(self, name: str, value: RuntimeValue) -> None:
        """Set a variable value, searching parent scopes if needed."""
        if name in self.values:
            self.values[name] = value
            return

        if self.parent is not None:
            self.parent.set(name, value)
            return

        raise NameError(f"Undefined variable: '{name}'")


class Function:
    """Represents a user-defined function."""

    def __init__(self, name: str, parameters: list[str], body: Block, closure: Environment) -> None:
        self.name = name
        self.parameters = parameters
        self.body = body
        self.closure = closure  # The environment where the function was defined

    def __repr__(self) -> str:
        return f"<function {self.name}>"
