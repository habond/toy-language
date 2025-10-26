"""AST Node definitions for the Toy Language interpreter."""

from dataclasses import dataclass


@dataclass
class ASTNode:
    """Base class for all AST nodes."""

    pass


# Literals and values
@dataclass
class Number(ASTNode):
    value: float


@dataclass
class String(ASTNode):
    value: str


@dataclass
class Boolean(ASTNode):
    value: bool


@dataclass
class Nil(ASTNode):
    pass


@dataclass
class Variable(ASTNode):
    name: str


# Binary operations
@dataclass
class BinaryOp(ASTNode):
    operator: str
    left: ASTNode
    right: ASTNode


# Unary operations
@dataclass
class UnaryOp(ASTNode):
    operator: str
    operand: ASTNode


# Statements
@dataclass
class VarDeclaration(ASTNode):
    name: str
    value: ASTNode


@dataclass
class Assignment(ASTNode):
    name: str
    value: ASTNode


@dataclass
class Block(ASTNode):
    statements: list[ASTNode]


@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_block: Block
    else_block: Block | None


@dataclass
class WhileStatement(ASTNode):
    condition: ASTNode
    body: Block


@dataclass
class ReturnStatement(ASTNode):
    value: ASTNode | None


@dataclass
class ExpressionStatement(ASTNode):
    expression: ASTNode


# Functions
@dataclass
class FunctionDef(ASTNode):
    name: str
    parameters: list[str]
    body: Block


@dataclass
class FunctionCall(ASTNode):
    name: str
    arguments: list[ASTNode]


@dataclass
class Program(ASTNode):
    statements: list[ASTNode]
