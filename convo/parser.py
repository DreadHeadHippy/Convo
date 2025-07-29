"""
Parser for the Convo programming language
Converts tokens into an Abstract Syntax Tree (AST)
"""

from typing import List, Optional
from .lexer import Token, TokenType, Lexer
from .ast_nodes import *

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def error(self, message: str):
        if self.current_token:
            raise SyntaxError(f"Line {self.current_token.line}, Column {self.current_token.column}: {message}")
        else:
            raise SyntaxError(f"Unexpected end of input: {message}")
    
    def advance(self):
        """Move to the next token"""
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def peek(self, offset: int = 1) -> Optional[Token]:
        """Look ahead at the next token without advancing"""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def match(self, *token_types: TokenType) -> bool:
        """Check if current token matches any of the given types"""
        if self.current_token and self.current_token.type in token_types:
            return True
        return False
    
    def consume(self, token_type: TokenType, message: str = None) -> Token:
        """Consume a token of the expected type or raise an error"""
        if self.current_token and self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        
        if message is None:
            message = f"Expected {token_type.name}"
        self.error(message)
    
    def skip_newlines(self):
        """Skip any newline tokens"""
        while self.match(TokenType.NEWLINE):
            self.advance()
    
    def parse(self) -> Program:
        """Parse the tokens into a Program AST node"""
        statements = []
        self.skip_newlines()
        
        while self.current_token and not self.match(TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return Program(statements)
    
    def parse_statement(self) -> Optional[Statement]:
        """Parse a single statement"""
        if self.match(TokenType.SAY):
            return self.parse_say_statement()
        elif self.match(TokenType.LET):
            return self.parse_let_statement()
        elif self.match(TokenType.DEFINE):
            return self.parse_function_definition()
        elif self.match(TokenType.CALL):
            return self.parse_call_statement()
        elif self.match(TokenType.IF):
            return self.parse_if_statement()
        elif self.match(TokenType.WHILE):
            return self.parse_while_statement()
        elif self.match(TokenType.NEWLINE):
            self.advance()
            return None
        else:
            self.error(f"Unexpected token: {self.current_token.value}")
    
    def parse_say_statement(self) -> SayStatement:
        """Parse: Say <expression>"""
        self.consume(TokenType.SAY)
        expression = self.parse_expression()
        return SayStatement(expression)
    
    def parse_let_statement(self) -> LetStatement:
        """Parse: Let <identifier> be <expression>"""
        self.consume(TokenType.LET)
        name_token = self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.BE)
        value = self.parse_expression()
        return LetStatement(name_token.value, value)
    
    def parse_function_definition(self) -> FunctionDefinition:
        """Parse: Define <name> with <param1>, <param2>: <body>"""
        self.consume(TokenType.DEFINE)
        name_token = self.consume(TokenType.IDENTIFIER)
        
        parameters = []
        if self.match(TokenType.WITH):
            self.advance()
            # Parse parameter list
            if self.match(TokenType.IDENTIFIER):
                parameters.append(self.current_token.value)
                self.advance()
                
                while self.match(TokenType.COMMA):
                    self.advance()
                    param_token = self.consume(TokenType.IDENTIFIER)
                    parameters.append(param_token.value)
        
        self.consume(TokenType.COLON)
        self.skip_newlines()
        
        # Parse function body (indented block)
        if self.match(TokenType.INDENT):
            body = self.parse_block()
        else:
            self.error("Expected indented block after function definition")
        
        return FunctionDefinition(name_token.value, parameters, body)
    
    def parse_call_statement(self) -> CallStatement:
        """Parse: Call <function_name> with <arg1>, <arg2>"""
        self.consume(TokenType.CALL)
        name_token = self.consume(TokenType.IDENTIFIER)
        
        arguments = []
        if self.match(TokenType.WITH):
            self.advance()
            # Parse argument list
            arguments.append(self.parse_expression())
            
            while self.match(TokenType.COMMA):
                self.advance()
                arguments.append(self.parse_expression())
        
        function_call = FunctionCall(name_token.value, arguments)
        return CallStatement(function_call)
    
    def parse_if_statement(self) -> IfStatement:
        """Parse: If <condition> then: <body> [else: <else_body>]"""
        self.consume(TokenType.IF)
        condition = self.parse_expression()
        self.consume(TokenType.THEN)
        self.consume(TokenType.COLON)
        self.skip_newlines()
        
        # Parse then block
        if self.match(TokenType.INDENT):
            then_block = self.parse_block()
        else:
            self.error("Expected indented block after 'then:'")
        
        # Parse optional else block
        else_block = []
        if self.match(TokenType.ELSE):
            self.advance()
            self.consume(TokenType.COLON)
            self.skip_newlines()
            
            if self.match(TokenType.INDENT):
                else_block = self.parse_block()
            else:
                self.error("Expected indented block after 'else:'")
        
        return IfStatement(condition, then_block, else_block)
    
    def parse_while_statement(self) -> WhileStatement:
        """Parse: While <condition> do: <body>"""
        self.consume(TokenType.WHILE)
        condition = self.parse_expression()
        self.consume(TokenType.DO)
        self.consume(TokenType.COLON)
        self.skip_newlines()
        
        # Parse body
        if self.match(TokenType.INDENT):
            body = self.parse_block()
        else:
            self.error("Expected indented block after 'do:'")
        
        return WhileStatement(condition, body)
    
    def parse_block(self) -> List[Statement]:
        """Parse an indented block of statements"""
        self.consume(TokenType.INDENT)
        statements = []
        
        while self.current_token and not self.match(TokenType.DEDENT, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        if self.match(TokenType.DEDENT):
            self.advance()
        
        return statements
    
    def parse_expression(self) -> Expression:
        """Parse an expression with operator precedence"""
        return self.parse_or_expression()
    
    def parse_or_expression(self) -> Expression:
        """Parse OR expressions (lowest precedence)"""
        expr = self.parse_and_expression()
        
        while self.match(TokenType.OR):
            operator = self.current_token.value
            self.advance()
            right = self.parse_and_expression()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_and_expression(self) -> Expression:
        """Parse AND expressions"""
        expr = self.parse_equality_expression()
        
        while self.match(TokenType.AND):
            operator = self.current_token.value
            self.advance()
            right = self.parse_equality_expression()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_equality_expression(self) -> Expression:
        """Parse equality expressions (equals, not equals)"""
        expr = self.parse_comparison_expression()
        
        while self.match(TokenType.EQUALS, TokenType.NOT_EQUALS):
            operator = self.current_token.value
            self.advance()
            right = self.parse_comparison_expression()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_comparison_expression(self) -> Expression:
        """Parse comparison expressions (greater, less)"""
        expr = self.parse_additive_expression()
        
        while self.match(TokenType.GREATER, TokenType.LESS):
            operator = self.current_token.value
            self.advance()
            # Handle "than" keyword after greater/less
            if self.match(TokenType.IDENTIFIER) and self.current_token.value == "than":
                self.advance()
            right = self.parse_additive_expression()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_additive_expression(self) -> Expression:
        """Parse addition and subtraction"""
        expr = self.parse_multiplicative_expression()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token.value
            self.advance()
            right = self.parse_multiplicative_expression()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_multiplicative_expression(self) -> Expression:
        """Parse multiplication and division"""
        expr = self.parse_unary_expression()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.current_token.value
            self.advance()
            right = self.parse_unary_expression()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_unary_expression(self) -> Expression:
        """Parse unary expressions (not, -, +)"""
        if self.match(TokenType.NOT, TokenType.MINUS, TokenType.PLUS):
            operator = self.current_token.value
            self.advance()
            operand = self.parse_unary_expression()
            return UnaryOp(operator, operand)
        
        return self.parse_primary_expression()
    
    def parse_primary_expression(self) -> Expression:
        """Parse primary expressions (literals, identifiers, function calls, parentheses)"""
        if self.match(TokenType.STRING, TokenType.NUMBER):
            value = self.current_token.value
            self.advance()
            return Literal(value)
        
        if self.match(TokenType.IDENTIFIER):
            name = self.current_token.value
            self.advance()
            return Identifier(name)
        
        if self.match(TokenType.LPAREN):
            self.advance()  # consume '('
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr
        
        self.error(f"Unexpected token in expression: {self.current_token.value}")

def parse_convo(text: str) -> Program:
    """Convenience function to parse Convo source code"""
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()
