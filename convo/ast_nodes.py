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

class MethodCall(Expression):
    def __init__(self, object_name: str, method_name: str, arguments: List[Expression]):
        self.object_name = object_name
        self.method_name = method_name
        self.arguments = arguments
    
    def __repr__(self):
        return f"MethodCall({self.object_name!r}, {self.method_name!r}, {self.arguments!r})"

class ListLiteral(Expression):
    def __init__(self, elements: List[Expression]):
        self.elements = elements
    
    def __repr__(self):
        return f"ListLiteral({self.elements!r})"

class DictionaryLiteral(Expression):
    def __init__(self, pairs: List[tuple]):
        self.pairs = pairs  # List of (key, value) tuples
    
    def __repr__(self):
        return f"DictionaryLiteral({self.pairs!r})"

class IndexAccess(Expression):
    def __init__(self, object: Expression, index: Expression):
        self.object = object
        self.index = index
    
    def __repr__(self):
        return f"IndexAccess({self.object!r}, {self.index!r})"

class PropertyAccess(Expression):
    def __init__(self, object: Expression, property_name: str):
        self.object = object
        self.property_name = property_name
    
    def __repr__(self):
        return f"PropertyAccess({self.object!r}, {self.property_name!r})"

class ObjectInstantiation(Expression):
    def __init__(self, class_name: str, arguments: List[Expression]):
        self.class_name = class_name
        self.arguments = arguments
    
    def __repr__(self):
        return f"ObjectInstantiation({self.class_name!r}, {self.arguments!r})"

class AttributeAccess(Expression):
    def __init__(self, object: Expression, attribute: str):
        self.object = object
        self.attribute = attribute
    
    def __repr__(self):
        return f"AttributeAccess({self.object!r}, {self.attribute!r})"

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

class ForStatement(Statement):
    def __init__(self, variable: str, iterable: Expression, body: List[Statement]):
        self.variable = variable
        self.iterable = iterable
        self.body = body
    
    def __repr__(self):
        return f"ForStatement({self.variable!r}, {self.iterable!r}, {self.body!r})"

class BreakStatement(Statement):
    def __repr__(self):
        return "BreakStatement()"

class ContinueStatement(Statement):
    def __repr__(self):
        return "ContinueStatement()"

class ReturnStatement(Statement):
    def __init__(self, value: Optional[Expression] = None):
        self.value = value
    
    def __repr__(self):
        return f"ReturnStatement({self.value!r})"

class TryStatement(Statement):
    def __init__(self, try_block: List[Statement], catch_block: List[Statement], exception_var: Optional[str] = None):
        self.try_block = try_block
        self.catch_block = catch_block
        self.exception_var = exception_var
    
    def __repr__(self):
        return f"TryStatement({self.try_block!r}, {self.catch_block!r}, {self.exception_var!r})"

class ThrowStatement(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression
    
    def __repr__(self):
        return f"ThrowStatement({self.expression!r})"

class ImportStatement(Statement):
    def __init__(self, module_name: str, alias: Optional[str] = None):
        self.module_name = module_name
        self.alias = alias
    
    def __repr__(self):
        return f"ImportStatement({self.module_name!r}, {self.alias!r})"

class ObjectPropertyAssignment(Statement):
    def __init__(self, object_name: str, property_name: str, value: 'Expression'):
        self.object_name = object_name
        self.property_name = property_name
        self.value = value
    
    def __repr__(self):
        return f"ObjectPropertyAssignment({self.object_name!r}, {self.property_name!r}, {self.value!r})"

class ClassDefinition(Statement):
    def __init__(self, name: str, constructor_params: List[str], body: List[Statement]):
        self.name = name
        self.constructor_params = constructor_params
        self.body = body
    
    def __repr__(self):
        return f"ClassDefinition({self.name!r}, {self.constructor_params!r}, {self.body!r})"

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
