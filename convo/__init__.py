"""
Convo Programming Language

A natural language-like programming language with conversational syntax.
"""

__version__ = "0.0.1"
__author__ = "DreadHeadHippy"

# Support both relative and absolute imports for better compatibility
try:
    from .lexer import Lexer, Token, TokenType
    from .parser import Parser, parse_convo
    from .interpreter import Interpreter, ConvoRuntimeError
    from .ast_nodes import *
except ImportError:
    # Fallback to absolute imports if relative imports fail
    from convo.lexer import Lexer, Token, TokenType
    from convo.parser import Parser, parse_convo
    from convo.interpreter import Interpreter, ConvoRuntimeError
    from convo.ast_nodes import *

__all__ = [
    'Lexer', 'Token', 'TokenType',
    'Parser', 'parse_convo',
    'Interpreter', 'ConvoRuntimeError',
    'ASTNode', 'Expression', 'Statement',
    'Literal', 'Identifier', 'BinaryOp', 'UnaryOp', 'FunctionCall',
    'SayStatement', 'LetStatement', 'FunctionDefinition', 'CallStatement',
    'IfStatement', 'WhileStatement', 'Block', 'Program'
]
