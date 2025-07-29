"""
Tests for the Convo interpreter
"""

from convo.lexer import Lexer
from convo.parser import Parser
from convo.interpreter import Interpreter

def test_say_statement():
    """Test Say statement execution"""
    code = 'Say "Hello, World!"'
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    interpreter = Interpreter()
    output = interpreter.interpret(ast)
    
    assert len(output) == 1
    assert output[0] == "Hello, World!"

def test_variable_assignment():
    """Test variable assignment and usage"""
    code = '''Let name be "Alice"
Say "Hello, " + name'''
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    interpreter = Interpreter()
    output = interpreter.interpret(ast)
    
    assert len(output) == 1
    assert output[0] == "Hello, Alice"

def test_arithmetic():
    """Test arithmetic operations"""
    code = '''Let result be 5 + 3 * 2
Say result'''
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    interpreter = Interpreter()
    output = interpreter.interpret(ast)
    
    assert len(output) == 1
    assert output[0] == "11"  # 5 + (3 * 2) = 11

def test_function_definition_and_call():
    """Test function definition and calling"""
    code = '''Define greet with name:
    Say "Hello, " + name + "!"

Call greet with "World"'''
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    interpreter = Interpreter()
    output = interpreter.interpret(ast)
    
    assert len(output) == 1
    assert output[0] == "Hello, World!"

def test_if_statement():
    """Test if statement execution"""
    code = '''Let age be 25
If age greater than 18 then:
    Say "Adult"
Else:
    Say "Minor"'''
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    interpreter = Interpreter()
    output = interpreter.interpret(ast)
    
    assert len(output) == 1
    assert output[0] == "Adult"

def test_while_loop():
    """Test while loop execution"""
    code = '''Let count be 1
While count less than 4 do:
    Say count
    Let count be count + 1'''
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    interpreter = Interpreter()
    output = interpreter.interpret(ast)
    
    assert len(output) == 3
    assert output == ["1", "2", "3"]
