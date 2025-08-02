"""
Abstract Syntax Tree node definitions for the Convo programming language

This module defines the AST node hierarchy with clear separation between:
- Expressions: Nodes that evaluate to values
- Statements: Nodes that perform actions
- CompoundStatements: Statements that contain other statements
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional, Union

class ASTNode(ABC):
    """Base class for all AST nodes"""
    
    @property
    def location(self) -> tuple:
        """Get the source location (line, column) of this node"""
        return getattr(self, '_location', (0, 0))
    
    @location.setter
    def location(self, value: tuple):
        """Set the source location (line, column) of this node"""
        self._location = value

class Expression(ASTNode):
    """Base class for all expressions - nodes that evaluate to values"""
    pass

class Statement(ASTNode):
    """Base class for all statements - nodes that perform actions"""
    pass

class CompoundStatement(Statement):
    """Base class for statements that contain other statements"""
    pass

# ========== EXPRESSION NODES ==========
# Expressions are nodes that evaluate to values

# Literal Values
class Literal(Expression):
    """Represents literal values like strings, numbers, booleans"""
    def __init__(self, value: Any):
        self.value = value
    
    def __repr__(self):
        return f"Literal({self.value!r})"

class BooleanLiteral(Literal):
    """Represents boolean literals (true/false)"""
    def __init__(self, value: bool):
        super().__init__(value)
    
    def __repr__(self):
        return f"BooleanLiteral({self.value})"

class NumberLiteral(Literal):
    """Represents numeric literals (integers and floats)"""
    def __init__(self, value: Union[int, float]):
        super().__init__(value)
    
    def __repr__(self):
        return f"NumberLiteral({self.value})"

class StringLiteral(Literal):
    """Represents string literals"""
    def __init__(self, value: str):
        super().__init__(value)
    
    def __repr__(self):
        return f"StringLiteral({self.value!r})"

class NullLiteral(Literal):
    """Represents null/none values"""
    def __init__(self):
        super().__init__(None)
    
    def __repr__(self):
        return "NullLiteral()"

# Identifiers and References
class Identifier(Expression):
    """Represents variable and function name references"""
    def __init__(self, name: str):
        self.name = name
    
    def __repr__(self):
        return f"Identifier({self.name!r})"

# Operators and Operations
class BinaryOp(Expression):
    """Represents binary operations like +, -, *, /, ==, etc."""
    def __init__(self, left: Expression, operator: str, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __repr__(self):
        return f"BinaryOp({self.left!r}, {self.operator!r}, {self.right!r})"

class UnaryOp(Expression):
    """Represents unary operations like not, -, +"""
    def __init__(self, operator: str, operand: Expression):
        self.operator = operator
        self.operand = operand
    
    def __repr__(self):
        return f"UnaryOp({self.operator!r}, {self.operand!r})"

class ConditionalExpression(Expression):
    """Represents ternary conditional expressions: condition ? true_expr : false_expr"""
    def __init__(self, condition: Expression, true_expr: Expression, false_expr: Expression):
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr
    
    def __repr__(self):
        return f"ConditionalExpression({self.condition!r}, {self.true_expr!r}, {self.false_expr!r})"

# Function and Method Calls
class FunctionCall(Expression):
    """Represents function calls"""
    def __init__(self, name: str, arguments: List[Expression]):
        self.name = name
        self.arguments = arguments
    
    def __repr__(self):
        return f"FunctionCall({self.name!r}, {self.arguments!r})"

class MethodCall(Expression):
    """Represents method calls on objects"""
    def __init__(self, object_name: str, method_name: str, arguments: List[Expression]):
        self.object_name = object_name  # Keep old format
        self.object_expr = Identifier(object_name) if isinstance(object_name, str) else object_name  # New format
        self.method_name = method_name
        self.arguments = arguments
    
    def __repr__(self):
        return f"MethodCall({self.object_name!r}, {self.method_name!r}, {self.arguments!r})"

# Collection Literals

# Collection Literals
class ListLiteral(Expression):
    """Represents list literals [1, 2, 3]"""
    def __init__(self, elements: List[Expression]):
        self.elements = elements
    
    def __repr__(self):
        return f"ListLiteral({self.elements!r})"

class DictionaryLiteral(Expression):
    """Represents dictionary literals {"key": "value"}"""
    def __init__(self, pairs: List[tuple]):
        self.pairs = pairs  # List of (key_expr, value_expr) tuples
    
    def __repr__(self):
        return f"DictionaryLiteral({self.pairs!r})"

class TupleLiteral(Expression):
    """Represents tuple literals (1, 2, 3)"""
    def __init__(self, elements: List[Expression]):
        self.elements = elements
    
    def __repr__(self):
        return f"TupleLiteral({self.elements!r})"

# Access Operations
class IndexAccess(Expression):
    """Represents index access operations: array[index]"""
    def __init__(self, object: Expression, index: Expression):
        self.object = object
        self.object_expr = object  # New alias
        self.index = index
    
    def __repr__(self):
        return f"IndexAccess({self.object!r}, {self.index!r})"

class PropertyAccess(Expression):
    """Represents property access: object.property"""
    def __init__(self, object: Expression, property_name: str):
        self.object = object
        self.object_expr = object  # New alias
        self.property_name = property_name
    
    def __repr__(self):
        return f"PropertyAccess({self.object!r}, {self.property_name!r})"

class SliceAccess(Expression):
    """Represents slice access: array[start:end]"""
    def __init__(self, object_expr: Expression, start: Optional[Expression], end: Optional[Expression]):
        self.object_expr = object_expr
        self.start = start
        self.end = end
    
    def __repr__(self):
        return f"SliceAccess({self.object_expr!r}, {self.start!r}, {self.end!r})"

class ListComprehension(Expression):
    """Represents list comprehensions: [expr for var in iterable if condition]"""
    def __init__(self, transform_expr: Expression, variable: str, iterable: Expression, condition: Optional[Expression] = None):
        self.transform_expr = transform_expr  # Expression to transform each item
        self.variable = variable              # Loop variable name
        self.iterable = iterable             # Collection to iterate over
        self.condition = condition           # Optional filter condition
    
    def __repr__(self):
        condition_repr = f", {self.condition!r}" if self.condition else ""
        return f"ListComprehension({self.transform_expr!r}, {self.variable!r}, {self.iterable!r}{condition_repr})"

# Object Creation
class ObjectInstantiation(Expression):
    """Represents object instantiation: new ClassName with args"""
    def __init__(self, class_name: str, arguments: List[Expression]):
        self.class_name = class_name
        self.arguments = arguments
    
    def __repr__(self):
        return f"ObjectInstantiation({self.class_name!r}, {self.arguments!r})"

# Function Expressions
class LambdaExpression(Expression):
    """Represents lambda/anonymous functions"""
    def __init__(self, parameters: List[str], body: Expression):
        self.parameters = parameters
        self.body = body
    
    def __repr__(self):
        return f"LambdaExpression({self.parameters!r}, {self.body!r})"

# Legacy aliases for compatibility
AttributeAccess = PropertyAccess

# ========== STATEMENT NODES ==========
# Statements are nodes that perform actions

# Simple Statements
class ExpressionStatement(Statement):
    """Represents an expression used as a statement"""
    def __init__(self, expression: Expression):
        self.expression = expression
    
    def __repr__(self):
        return f"ExpressionStatement({self.expression!r})"

class SayStatement(Statement):
    """Represents print/output statements"""
    def __init__(self, expression: Expression):
        self.expression = expression
    
    def __repr__(self):
        return f"SayStatement({self.expression!r})"

# Variable Assignment Statements
class LetStatement(Statement):
    """Represents variable declarations and assignments"""
    def __init__(self, name: str, value: Expression):
        self.name = name
        self.value = value
    
    def __repr__(self):
        return f"LetStatement({self.name!r}, {self.value!r})"

class AssignmentStatement(Statement):
    """Represents variable reassignment"""
    def __init__(self, target: str, value: Expression):
        self.target = target
        self.value = value
    
    def __repr__(self):
        return f"AssignmentStatement({self.target!r}, {self.value!r})"

class CompoundAssignmentStatement(Statement):
    """Represents compound assignment operators like +=, -=, *=, /="""
    def __init__(self, target: str, operator: str, value: Expression):
        self.target = target
        self.operator = operator  # "+", "-", "*", "/", etc.
        self.value = value
    
    def __repr__(self):
        return f"CompoundAssignmentStatement({self.target!r}, {self.operator!r}, {self.value!r})"

class PropertyAssignmentStatement(Statement):
    """Represents property assignment: object.property = value"""
    def __init__(self, object_name: str, property_name: str, value: Expression):
        # Keep old format for compatibility
        if isinstance(object_name, str):
            self.object_name = object_name
            self.object_expr = Identifier(object_name)
        else:
            self.object_expr = object_name
            self.object_name = str(object_name)
        self.property_name = property_name
        self.value = value
    
    def __repr__(self):
        return f"PropertyAssignmentStatement({self.object_name!r}, {self.property_name!r}, {self.value!r})"

class IndexAssignmentStatement(Statement):
    """Represents index assignment: array[index] = value"""
    def __init__(self, object_expr: Expression, index: Expression, value: Expression):
        self.object_expr = object_expr
        self.index = index
        self.value = value
    
    def __repr__(self):
        return f"IndexAssignmentStatement({self.object_expr!r}, {self.index!r}, {self.value!r})"

# Function and Call Statements
class CallStatement(Statement):
    """Represents function calls used as statements"""
    def __init__(self, function_call: FunctionCall):
        self.function_call = function_call
    
    def __repr__(self):
        return f"CallStatement({self.function_call!r})"

class FunctionDefinition(Statement):
    """Represents function definitions"""
    def __init__(self, name: str, parameters: List[str], body: List[Statement]):
        self.name = name
        self.parameters = parameters
        self.body = body
    
    def __repr__(self):
        return f"FunctionDefinition({self.name!r}, {self.parameters!r}, {self.body!r})"

# Control Flow Statements
class ReturnStatement(Statement):
    """Represents return statements"""
    def __init__(self, value: Optional[Expression] = None):
        self.value = value
    
    def __repr__(self):
        return f"ReturnStatement({self.value!r})"

class BreakStatement(Statement):
    """Represents break statements"""
    def __repr__(self):
        return "BreakStatement()"

class ContinueStatement(Statement):
    """Represents continue statements"""
    def __repr__(self):
        return "ContinueStatement()"

class PassStatement(Statement):
    """Represents pass/no-op statements"""
    def __repr__(self):
        return "PassStatement()"

# ========== COMPOUND STATEMENT NODES ==========
# Compound statements contain other statements

class IfStatement(CompoundStatement):
    """Represents conditional statements"""
    def __init__(self, condition: Expression, then_block: List[Statement], else_block: Optional[List[Statement]] = None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block or []
    
    def __repr__(self):
        return f"IfStatement({self.condition!r}, {self.then_block!r}, {self.else_block!r})"

class WhileStatement(CompoundStatement):
    """Represents while loop statements"""
    def __init__(self, condition: Expression, body: List[Statement]):
        self.condition = condition
        self.body = body
    
    def __repr__(self):
        return f"WhileStatement({self.condition!r}, {self.body!r})"

class ForStatement(CompoundStatement):
    """Represents for loop statements"""
    def __init__(self, variable: str, iterable: Expression, body: List[Statement]):
        self.variable = variable
        self.iterable = iterable
        self.body = body
    
    def __repr__(self):
        return f"ForStatement({self.variable!r}, {self.iterable!r}, {self.body!r})"

class ForIndexStatement(CompoundStatement):
    """Represents indexed for loop statements (For item at index in collection)"""
    def __init__(self, item_var: str, index_var: str, iterable: Expression, body: List[Statement]):
        self.item_var = item_var
        self.index_var = index_var
        self.iterable = iterable
        self.body = body
    
    def __repr__(self):
        return f"ForIndexStatement({self.item_var!r}, {self.index_var!r}, {self.iterable!r}, {self.body!r})"

class ForUnpackStatement(CompoundStatement):
    """Represents unpacking for loop statements (For key, value in collection)"""
    def __init__(self, variables: List[str], iterable: Expression, body: List[Statement]):
        self.variables = variables
        self.iterable = iterable
        self.body = body
    
    def __repr__(self):
        return f"ForUnpackStatement({self.variables!r}, {self.iterable!r}, {self.body!r})"

class TryStatement(CompoundStatement):
    """Represents try-catch exception handling"""
    def __init__(self, try_block: List[Statement], catch_block: List[Statement], exception_var: Optional[str] = None):
        self.try_block = try_block
        self.catch_block = catch_block
        self.exception_var = exception_var
    
    def __repr__(self):
        return f"TryStatement({self.try_block!r}, {self.catch_block!r}, {self.exception_var!r})"

class WithStatement(CompoundStatement):
    """Represents with/context manager statements"""
    def __init__(self, context_expr: Expression, variable: Optional[str], body: List[Statement]):
        self.context_expr = context_expr
        self.variable = variable
        self.body = body
    
    def __repr__(self):
        return f"WithStatement({self.context_expr!r}, {self.variable!r}, {self.body!r})"

class ClassDefinition(CompoundStatement):
    """Represents class definitions"""
    def __init__(self, name: str, constructor_params: List[str], body: List[Statement], parent_class: Optional[str] = None):
        self.name = name
        self.constructor_params = constructor_params
        self.body = body
        self.parent_class = parent_class
    
    def __repr__(self):
        return f"ClassDefinition({self.name!r}, {self.constructor_params!r}, {self.body!r}, {self.parent_class!r})"

class Block(CompoundStatement):
    """Represents a block of statements"""
    def __init__(self, statements: List[Statement]):
        self.statements = statements
    
    def __repr__(self):
        return f"Block({self.statements!r})"

# ========== SPECIAL STATEMENT NODES ==========

class ThrowStatement(Statement):
    """Represents throw/raise exception statements"""
    def __init__(self, expression: Expression):
        self.expression = expression
    
    def __repr__(self):
        return f"ThrowStatement({self.expression!r})"

class ImportStatement(Statement):
    """Represents import statements"""
    def __init__(self, module_name: str, alias: Optional[str] = None):
        self.module_name = module_name
        self.alias = alias
    
    def __repr__(self):
        return f"ImportStatement({self.module_name!r}, {self.alias!r})"

class FromImportStatement(Statement):
    """Represents from...import statements"""
    def __init__(self, module_name: str, imports: List[str], aliases: Optional[List[str]] = None):
        self.module_name = module_name
        self.imports = imports
        self.aliases = aliases or []
    
    def __repr__(self):
        return f"FromImportStatement({self.module_name!r}, {self.imports!r}, {self.aliases!r})"

# ========== ROOT NODE ==========

class Program(ASTNode):
    """Represents the root of the AST - a complete program"""
    def __init__(self, statements: List[Statement]):
        self.statements = statements
    
    def __repr__(self):
        return f"Program({self.statements!r})"

# ========== LEGACY COMPATIBILITY ==========
# Keep old names for backward compatibility

ObjectPropertyAssignment = PropertyAssignmentStatement
