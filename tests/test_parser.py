"""
Tests for the Convo parser
"""

from convo.lexer import Lexer
from convo.parser import Parser
from convo.ast_nodes import *

def test_say_statement():
    """Test parsing Say statements"""
    lexer = Lexer('Say "Hello"')
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert len(ast.statements) == 1
    statement = ast.statements[0]
    assert isinstance(statement, SayStatement)
    assert isinstance(statement.expression, Literal)
    assert statement.expression.value == "Hello"

def test_let_statement():
    """Test parsing Let statements"""
    lexer = Lexer('Let name be "Alice"')
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert len(ast.statements) == 1
    statement = ast.statements[0]
    assert isinstance(statement, LetStatement)
    assert statement.name == "name"
    assert isinstance(statement.value, Literal)
    assert statement.value.value == "Alice"

def test_binary_expression():
    """Test parsing binary expressions"""
    lexer = Lexer('Say 5 + 3')
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    statement = ast.statements[0]
    assert isinstance(statement, SayStatement)
    assert isinstance(statement.expression, BinaryOp)
    assert statement.expression.operator == "+"
    assert statement.expression.left.value == 5
    assert statement.expression.right.value == 3

def test_function_definition():
    """Test parsing function definitions"""
    code = '''Define greet with name:
    Say "Hello, " + name'''
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert len(ast.statements) == 1
    statement = ast.statements[0]
    assert isinstance(statement, FunctionDefinition)
    assert statement.name == "greet"
    assert statement.parameters == ["name"]
    assert len(statement.body) == 1

def test_if_statement():
    """Test parsing if statements"""
    code = '''If age greater than 18 then:
    Say "Adult"
Else:
    Say "Minor"'''
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert len(ast.statements) == 1
    statement = ast.statements[0]
    assert isinstance(statement, IfStatement)
    assert isinstance(statement.condition, BinaryOp)
    assert len(statement.then_block) == 1
    assert len(statement.else_block) == 1
