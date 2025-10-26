"""AST Builder for the Toy Language.

This module transforms the parse tree from Lark into our AST nodes.
"""

from typing import cast

from lark import Token, Transformer

from ast_nodes import (
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

# Type alias for items that come from the parser (can be tokens or transformed nodes)
TransformerItem = Token | ASTNode


class ASTBuilder(Transformer[Token, ASTNode]):
    """Transforms the parse tree from Lark into our AST nodes."""

    def _extract_name(self, item: TransformerItem) -> str:
        """Extract string name from a Variable node or Token."""
        return item.name if isinstance(item, Variable) else str(item)

    def program(self, items: list[ASTNode]) -> Program:
        return Program(statements=items)

    def var_declaration(self, items: list[TransformerItem]) -> VarDeclaration:
        name = self._extract_name(items[0])
        value = cast(ASTNode, items[1])
        return VarDeclaration(name=name, value=value)

    def assignment(self, items: list[TransformerItem]) -> Assignment:
        name = self._extract_name(items[0])
        value = cast(ASTNode, items[1])
        return Assignment(name=name, value=value)

    def function_def(self, items: list[TransformerItem]) -> FunctionDef:
        name = self._extract_name(items[0])
        if len(items) == 3:  # name, parameters, body
            parameters = cast(list[str], items[1])
            body = cast(Block, items[2])
        else:  # name, body (no parameters)
            parameters = []
            body = cast(Block, items[1])
        return FunctionDef(name=name, parameters=parameters, body=body)

    def parameters(self, items: list[TransformerItem]) -> list[str]:
        """Extract parameter names from Variable nodes or Tokens."""
        return [self._extract_name(item) for item in items]

    def block(self, items: list[ASTNode]) -> Block:
        return Block(statements=items)

    def return_statement(self, items: list[TransformerItem]) -> ReturnStatement:
        value = cast(ASTNode, items[0]) if items else None
        return ReturnStatement(value=value)

    def if_statement(self, items: list[TransformerItem]) -> IfStatement:
        condition = cast(ASTNode, items[0])
        then_block = cast(Block, items[1])
        else_block = cast(Block, items[2]) if len(items) > 2 else None
        return IfStatement(condition=condition, then_block=then_block, else_block=else_block)

    def while_statement(self, items: list[TransformerItem]) -> WhileStatement:
        condition = cast(ASTNode, items[0])
        body = cast(Block, items[1])
        return WhileStatement(condition=condition, body=body)

    def expression_statement(self, items: list[TransformerItem]) -> ExpressionStatement:
        return ExpressionStatement(expression=cast(ASTNode, items[0]))

    # Binary operations - named rules from grammar
    def eq(self, items: list[ASTNode]) -> BinaryOp:
        return BinaryOp(operator="==", left=items[0], right=items[1])

    def neq(self, items: list[ASTNode]) -> BinaryOp:
        return BinaryOp(operator="!=", left=items[0], right=items[1])

    def lt(self, items: list[ASTNode]) -> BinaryOp:
        return BinaryOp(operator="<", left=items[0], right=items[1])

    def gt(self, items: list[ASTNode]) -> BinaryOp:
        return BinaryOp(operator=">", left=items[0], right=items[1])

    def add(self, items: list[ASTNode]) -> BinaryOp:
        return BinaryOp(operator="+", left=items[0], right=items[1])

    def sub(self, items: list[ASTNode]) -> BinaryOp:
        return BinaryOp(operator="-", left=items[0], right=items[1])

    def mul(self, items: list[ASTNode]) -> BinaryOp:
        return BinaryOp(operator="*", left=items[0], right=items[1])

    def div(self, items: list[ASTNode]) -> BinaryOp:
        return BinaryOp(operator="/", left=items[0], right=items[1])

    # Unary operations
    def neg(self, items: list[ASTNode]) -> UnaryOp:
        return UnaryOp(operator="-", operand=items[0])

    def function_call(self, items: list[TransformerItem]) -> FunctionCall:
        name = self._extract_name(items[0])
        arguments = cast(list[ASTNode], items[1]) if len(items) > 1 else []
        return FunctionCall(name=name, arguments=arguments)

    def arguments(self, items: list[ASTNode]) -> list[ASTNode]:
        return items

    def NUMBER(self, token: Token) -> Number:
        value = float(str(token))
        return Number(value=value)

    def STRING(self, token: Token) -> String:
        # Remove quotes from string
        string_value = str(token)[1:-1]
        return String(value=string_value)

    def BOOLEAN(self, token: Token) -> Boolean:
        value = str(token) == "true"
        return Boolean(value=value)

    def nil(self, items: list[TransformerItem]) -> Nil:
        return Nil()

    def NAME(self, token: Token) -> Variable:
        return Variable(name=str(token))
