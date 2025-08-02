"""
Tests for the import system in the Convo programming language
"""

import pytest
from convo.lexer import Lexer
from convo.parser import Parser
from convo.interpreter import Interpreter
from convo.ast_nodes import *

def test_import_statement_parsing():
    """Test that import statements are parsed correctly"""
    code = "Import discord"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    
    assert len(program.statements) == 1
    assert isinstance(program.statements[0], ImportStatement)
    assert program.statements[0].module_name == "discord"

def test_import_statement_execution():
    """Test that import statements execute without error"""
    code = "Import discord"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    interpreter = Interpreter()
    
    # Should not raise an exception
    interpreter.interpret(program)

def test_discord_functions_available_after_import():
    """Test that Discord functions are available after import"""
    code = """
Import discord
Call create_discord_bot with "test_token", "!"
"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    interpreter = Interpreter()
    
    # Should not raise an exception for undefined function
    output = interpreter.interpret(program)

def test_unknown_module_import():
    """Test that importing unknown modules raises an error"""
    code = "Import unknown_module"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    interpreter = Interpreter()
    
    output = interpreter.interpret(program)
    assert any("Unknown module: unknown_module" in line for line in output)

def test_import_with_alias():
    """Test import with alias (future feature)"""
    # This test is for future implementation
    # For now, just ensure the AST supports it
    import_stmt = ImportStatement("discord", "d")
    assert import_stmt.module_name == "discord"
    assert import_stmt.alias == "d"
