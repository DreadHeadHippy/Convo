#!/usr/bin/env python3
"""
Test Phase 2 Step 2: Enhanced Control Flow and Expressions

Tests enhanced binary operations, advanced conditional expressions, 
improved evaluation order, and enhanced loop control.
"""

import pytest
from convo.lexer import Lexer
from convo.parser import Parser
from convo.interpreter import Interpreter
from convo.ast_nodes import *


class TestEnhancedBinaryOperations:
    """Test enhanced binary operations with better type handling"""
    
    def test_enhanced_addition(self):
        """Test enhanced addition with different types"""
        # String concatenation
        program = 'Let result be "Hello" + " " + "World"'
        lexer = Lexer(program)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.interpret(ast)
        assert interpreter.global_env.get("result") == "Hello World"
        
        # Number + string concatenation
        program = 'Let result be 42 + " is the answer"'
        lexer = Lexer(program)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.interpret(ast)
        assert interpreter.global_env.get("result") == "42 is the answer"
    
    def test_enhanced_multiplication(self):
        """Test enhanced multiplication with different types"""
        # String repetition
        program = 'Let result be "Hi" * 3'
        lexer = Lexer(program)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.interpret(ast)
        assert interpreter.global_env.get("result") == "HiHiHi"
    
    def test_enhanced_equality(self):
        """Test enhanced equality comparisons"""
        # String vs number equality
        program = 'Let result be 42 equals "42"'
        lexer = Lexer(program)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.interpret(ast)
        assert interpreter.global_env.get("result") == True
        
        # Null comparisons
        program = 'Let result be null equals null'
        lexer = Lexer(program)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.interpret(ast)
        assert interpreter.global_env.get("result") == True
    
    def test_enhanced_comparisons(self):
        """Test enhanced comparison operations"""
        # String comparisons
        program = 'Let result be "apple" less than "banana"'
        lexer = Lexer(program)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.interpret(ast)
        assert interpreter.global_env.get("result") == True
        
        # Mixed type comparisons (convert to numbers)
        program = 'Let result be "10" greater than 5'
        lexer = Lexer(program)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.interpret(ast)
        assert interpreter.global_env.get("result") == True
    
    def test_short_circuit_evaluation(self):
        """Test short-circuit evaluation for logical operations"""
        # Test 'and' short-circuit
        program = '''
Let x be false
Let y be true
Let result be x and y
'''
        lexer = Lexer(program)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.interpret(ast)
        assert interpreter.global_env.get("result") == False
        
        # Test 'or' short-circuit
        program = '''
Let x be true
Let y be false
Let result be x or y
'''
        lexer = Lexer(program)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.interpret(ast)
        assert interpreter.global_env.get("result") == True


class TestEnhancedTruthiness:
    """Test enhanced truthiness evaluation"""
    
    def test_truthiness_values(self):
        """Test truthiness of different values"""
        test_cases = [
            ("null", False),
            ("true", True),
            ("false", False),
            ("0", False),
            ("1", True),
            ('""', False),
            ('"hello"', True),
        ]
        
        for value, expected in test_cases:
            program = f'''
If {value} then:
    Let result be true
Else:
    Let result be false
'''
            lexer = Lexer(program)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            interpreter = Interpreter()
            interpreter.interpret(ast)
            assert interpreter.global_env.get("result") == expected, f"Failed for value {value}"


class TestEnhancedStringification:
    """Test enhanced string conversion"""
    
    def test_stringify_literals(self):
        """Test stringification of different literal types"""
        program = '''
Let null_str be null + ""
Let bool_true_str be true + ""
Let bool_false_str be false + ""
Let number_str be 42 + ""
'''
        lexer = Lexer(program)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
        assert interpreter.global_env.get("null_str") == "null"
        assert interpreter.global_env.get("bool_true_str") == "true"
        assert interpreter.global_env.get("bool_false_str") == "false"
        assert interpreter.global_env.get("number_str") == "42"


class TestErrorHandling:
    """Test enhanced error handling for binary operations"""
    
    def test_division_by_zero(self):
        """Test division by zero error"""
        program = 'Let result be 10 / 0'
        lexer = Lexer(program)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        output = interpreter.interpret(ast)
        assert any("Division by zero" in line for line in output), f"Expected 'Division by zero' error in output: {output}"
    
    def test_invalid_subtraction(self):
        """Test invalid subtraction operations"""
        program = 'Let result be "hello" - "world"'
        lexer = Lexer(program)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        output = interpreter.interpret(ast)
        assert any("Cannot subtract" in line for line in output), f"Expected 'Cannot subtract' error in output: {output}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
