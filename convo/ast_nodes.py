"""
Abstract Syntax Tree node definitions for the Convo programming language
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional

class ASTNode(ABC):
    """Base class for all AST nodes"""
    pass

class Expression(ASTNode):
    """Base class for all expressions"""
    pass

class Statement(ASTNode):
    """Base class for all statements"""
    pass

# Expressions
class Literal(Expression):
    def __init__(self, value: Any):
        self.value = value
    
    def __repr__(self):
        return f"Literal({self.value!r})"

class Identifier(Expression):
    def __init__(self, name: str):
        self.name = name
    
    def __repr__(self):
        return f"Identifier({self.name!r})"

class BinaryOp(Expression):
    def __init__(self, left: Expression, operator: str, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __repr__(self):
        return f"BinaryOp({self.left!r}, {self.operator!r}, {self.right!r})"

class UnaryOp(Expression):
    def __init__(self, operator: str, operand: Expression):
        self.operator = operator
        self.operand = operand
    
    def __repr__(self):
        return f"UnaryOp({self.operator!r}, {self.operand!r})"

class FunctionCall(Expression):
    def __init__(self, name: str, arguments: List[Expression]):
        self.name = name
        self.arguments = arguments
    
    def __repr__(self):
        return f"FunctionCall({self.name!r}, {self.arguments!r})"

# Statements
class SayStatement(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression
    
    def __repr__(self):
        return f"SayStatement({self.expression!r})"

class LetStatement(Statement):
    def __init__(self, name: str, value: Expression):
        self.name = name
        self.value = value
    
    def __repr__(self):
        return f"LetStatement({self.name!r}, {self.value!r})"

class FunctionDefinition(Statement):
    def __init__(self, name: str, parameters: List[str], body: List[Statement]):
        self.name = name
        self.parameters = parameters
        self.body = body
    
    def __repr__(self):
        return f"FunctionDefinition({self.name!r}, {self.parameters!r}, {self.body!r})"

class CallStatement(Statement):
    def __init__(self, function_call: FunctionCall):
        self.function_call = function_call
    
    def __repr__(self):
        return f"CallStatement({self.function_call!r})"

class IfStatement(Statement):
    def __init__(self, condition: Expression, then_block: List[Statement], else_block: Optional[List[Statement]] = None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block or []
    
    def __repr__(self):
        return f"IfStatement({self.condition!r}, {self.then_block!r}, {self.else_block!r})"

class WhileStatement(Statement):
    def __init__(self, condition: Expression, body: List[Statement]):
        self.condition = condition
        self.body = body
    
    def __repr__(self):
        return f"WhileStatement({self.condition!r}, {self.body!r})"

class Block(Statement):
    def __init__(self, statements: List[Statement]):
        self.statements = statements
    
    def __repr__(self):
        return f"Block({self.statements!r})"

class Program(ASTNode):
    def __init__(self, statements: List[Statement]):
        self.statements = statements
    
    def __repr__(self):
        return f"Program({self.statements!r})"
