"""
Token definitions for the Convo programming language
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional

class TokenType(Enum):
    # Literals
    STRING = auto()
    NUMBER = auto()
    IDENTIFIER = auto()
    
    # Keywords
    SAY = auto()          # Say "Hello"
    LET = auto()          # Let x be 5
    BE = auto()           # Let x be 5
    DEFINE = auto()       # Define function with args
    WITH = auto()         # Define function with args
    CALL = auto()         # Call function with args
    IF = auto()           # If condition then
    THEN = auto()         # If condition then
    ELSE = auto()         # Else
    WHILE = auto()        # While condition do
    DO = auto()           # While condition do
    FOR = auto()          # For each item in list
    EACH = auto()         # For each item in list  
    IN = auto()           # in keyword
    BREAK = auto()        # Break from loop
    CONTINUE = auto()     # Continue loop
    RETURN = auto()       # Return from function
    TRY = auto()          # Try block
    CATCH = auto()        # Catch errors
    THROW = auto()        # Throw error
    IMPORT = auto()       # Import module
    FROM = auto()         # From module import
    CREATE = auto()       # Create object/list
    LIST = auto()         # List data type
    DICTIONARY = auto()   # Dictionary data type
    CLASS = auto()        # Class definition
    NEW = auto()          # Create new instance
    
    # Operators
    PLUS = auto()         # +
    MINUS = auto()        # -
    MULTIPLY = auto()     # *
    DIVIDE = auto()       # /
    EQUALS = auto()       # equals, is
    NOT_EQUALS = auto()   # not equals, is not
    GREATER = auto()      # greater than
    LESS = auto()         # less than
    AND = auto()          # and
    OR = auto()           # or
    NOT = auto()          # not
    
    # Punctuation
    COLON = auto()        # :
    COMMA = auto()        # ,
    LPAREN = auto()       # (
    RPAREN = auto()       # )
    LBRACKET = auto()     # [
    RBRACKET = auto()     # ]
    LBRACE = auto()       # {
    RBRACE = auto()       # }
    DOT = auto()          # .
    NEWLINE = auto()      # \n
    INDENT = auto()       # indentation
    DEDENT = auto()       # dedentation
    
    # Special
    EOF = auto()
    UNKNOWN = auto()

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.indent_stack = [0]  # Track indentation levels
        
    def error(self, message: str):
        raise SyntaxError(f"Line {self.line}, Column {self.column}: {message}")
    
    def peek(self, offset: int = 0) -> Optional[str]:
        pos = self.pos + offset
        if pos < len(self.text):
            return self.text[pos]
        return None
    
    def advance(self) -> Optional[str]:
        if self.pos < len(self.text):
            char = self.text[self.pos]
            self.pos += 1
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return char
        return None
    
    def skip_whitespace(self):
        char = self.peek()
        while char and char in ' \t':
            self.advance()
            char = self.peek()
    
    def read_string(self) -> str:
        quote_char = self.advance()  # Skip opening quote
        value = ""
        
        while self.peek() and self.peek() != quote_char:
            char = self.advance()
            if char == '\\':
                # Handle escape sequences
                next_char = self.advance()
                if next_char == 'n':
                    value += '\n'
                elif next_char == 't':
                    value += '\t'
                elif next_char == '\\':
                    value += '\\'
                elif next_char and next_char == quote_char:
                    value += quote_char
                elif next_char:
                    value += next_char
            elif char:
                value += char
        
        if not self.peek():
            self.error("Unterminated string")
        
        self.advance()  # Skip closing quote
        return value
    
    def read_number(self) -> float:
        value = ""
        has_dot = False
        
        char = self.peek()
        while char and (char.isdigit() or char == '.'):
            if char == '.':
                if has_dot:
                    break
                has_dot = True
            next_char = self.advance()
            if next_char:
                value += next_char
            char = self.peek()
        
        return float(value) if has_dot else int(value)
    
    def read_identifier(self) -> str:
        value = ""
        char = self.peek()
        while char and (char.isalnum() or char == '_'):
            next_char = self.advance()
            if next_char:
                value += next_char
            char = self.peek()
        return value
    
    def handle_indentation(self):
        # Count leading spaces/tabs
        indent_level = 0
        char = self.peek()
        while char and char in ' \t':
            if char == ' ':
                indent_level += 1
            else:  # tab
                indent_level += 4  # Treat tab as 4 spaces
            self.advance()
            char = self.peek()
        
        current_indent = self.indent_stack[-1]
        
        if indent_level > current_indent:
            self.indent_stack.append(indent_level)
            self.tokens.append(Token(TokenType.INDENT, None, self.line, self.column))
        elif indent_level < current_indent:
            while self.indent_stack and self.indent_stack[-1] > indent_level:
                self.indent_stack.pop()
                self.tokens.append(Token(TokenType.DEDENT, None, self.line, self.column))
            
            if not self.indent_stack or self.indent_stack[-1] != indent_level:
                self.error("Invalid indentation")
    
    def tokenize(self) -> list[Token]:
        keywords = {
            'say': TokenType.SAY,
            'let': TokenType.LET,
            'be': TokenType.BE,
            'define': TokenType.DEFINE,
            'with': TokenType.WITH,
            'call': TokenType.CALL,
            'if': TokenType.IF,
            'then': TokenType.THEN,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'do': TokenType.DO,
            'for': TokenType.FOR,
            'each': TokenType.EACH,
            'in': TokenType.IN,
            'break': TokenType.BREAK,
            'continue': TokenType.CONTINUE,
            'return': TokenType.RETURN,
            'try': TokenType.TRY,
            'catch': TokenType.CATCH,
            'throw': TokenType.THROW,
            'import': TokenType.IMPORT,
            'from': TokenType.FROM,
            'create': TokenType.CREATE,
            'list': TokenType.LIST,
            'dictionary': TokenType.DICTIONARY,
            'class': TokenType.CLASS,
            'new': TokenType.NEW,
            'and': TokenType.AND,
            'or': TokenType.OR,
            'not': TokenType.NOT,
            'equals': TokenType.EQUALS,
            'is': TokenType.EQUALS,
            'greater': TokenType.GREATER,
            'than': TokenType.IDENTIFIER,  # "than" will be treated as regular identifier and handled in parser
            'less': TokenType.LESS,
        }
        
        at_line_start = True
        
        while self.pos < len(self.text):
            if at_line_start:
                self.handle_indentation()
                at_line_start = False
                if self.peek() == '\n':
                    continue
            
            char = self.peek()
            
            if char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, char, self.line, self.column))
                self.advance()
                at_line_start = True
                continue
            
            if char and char in ' \t':
                self.skip_whitespace()
                continue
            
            if char and char in '"\'':
                value = self.read_string()
                self.tokens.append(Token(TokenType.STRING, value, self.line, self.column))
                continue
            
            if char == '#':
                # Skip comments until end of line
                while char and char != '\n':
                    self.advance()
                    char = self.peek()
                continue
            
            if char and char.isdigit():
                value = self.read_number()
                self.tokens.append(Token(TokenType.NUMBER, value, self.line, self.column))
                continue
            
            if char and (char.isalpha() or char == '_'):
                value = self.read_identifier().lower()
                token_type = keywords.get(value, TokenType.IDENTIFIER)
                self.tokens.append(Token(token_type, value, self.line, self.column))
                continue
            
            # Single character tokens
            single_char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                ':': TokenType.COLON,
                ',': TokenType.COMMA,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '.': TokenType.DOT,
            }
            
            if char in single_char_tokens:
                self.tokens.append(Token(single_char_tokens[char], char, self.line, self.column))
                self.advance()
                continue
            
            # Unknown character
            self.tokens.append(Token(TokenType.UNKNOWN, char, self.line, self.column))
            self.advance()
        
        # Add final dedents
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT, None, self.line, self.column))
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
