"""
Tests for the Convo lexer
"""

import pytest
from convo.lexer import Lexer, TokenType

def test_simple_tokens():
    """Test basic token recognition"""
    lexer = Lexer('Say "Hello"')
    tokens = lexer.tokenize()
    
    assert len(tokens) == 3  # SAY, STRING, EOF
    assert tokens[0].type == TokenType.SAY
    assert tokens[1].type == TokenType.STRING
    assert tokens[1].value == "Hello"
    assert tokens[2].type == TokenType.EOF

def test_variable_assignment():
    """Test variable assignment tokenization"""
    lexer = Lexer('Let name be "Alice"')
    tokens = lexer.tokenize()
    
    token_types = [token.type for token in tokens[:-1]]  # Exclude EOF
    expected = [TokenType.LET, TokenType.IDENTIFIER, TokenType.BE, TokenType.STRING]
    assert token_types == expected

def test_numbers():
    """Test number tokenization"""
    lexer = Lexer('Let age be 25')
    tokens = lexer.tokenize()
    
    number_token = tokens[3]  # Fourth token should be the number
    assert number_token.type == TokenType.NUMBER
    assert number_token.value == 25

def test_operators():
    """Test operator tokenization"""
    lexer = Lexer('5 + 3 - 2 * 4 / 2')
    tokens = lexer.tokenize()
    
    operators = [token for token in tokens if token.type in [
        TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE
    ]]
    assert len(operators) == 4

def test_string_escapes():
    """Test string escape sequences"""
    lexer = Lexer(r'Say "Hello\nWorld"')
    tokens = lexer.tokenize()
    
    string_token = tokens[1]
    assert string_token.type == TokenType.STRING
    assert string_token.value == "Hello\nWorld"

def test_indentation():
    """Test indentation handling"""
    code = '''Define test:
    Say "Indented"
    Say "Still indented"
Say "Not indented"'''
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Should have INDENT and DEDENT tokens
    indent_tokens = [token for token in tokens if token.type == TokenType.INDENT]
    dedent_tokens = [token for token in tokens if token.type == TokenType.DEDENT]
    
    assert len(indent_tokens) == 1
    assert len(dedent_tokens) == 1
