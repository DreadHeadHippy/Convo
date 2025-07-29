"""
Convo Programming Language

A natural language-like programming language with conversational syntax.
"""

__version__ = "1.0.0"
__author__ = "Convo Language Team"

from .lexer import Lexer, Token, TokenType
from .parser import Parser, parse_convo
from .interpreter import Interpreter, ConvoRuntimeError
from .ast_nodes import *

__all__ = [
    'Lexer', 'Token', 'TokenType',
    'Parser', 'parse_convo',
    'Interpreter', 'ConvoRuntimeError',
    'ASTNode', 'Expression', 'Statement',
    'Literal', 'Identifier', 'BinaryOp', 'UnaryOp', 'FunctionCall',
    'SayStatement', 'LetStatement', 'FunctionDefinition', 'CallStatement',
    'IfStatement', 'WhileStatement', 'Block', 'Program'
]
