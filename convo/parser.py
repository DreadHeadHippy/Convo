"""
Parser for the Convo programming language
Converts tokens into an Abstract Syntax Tree (AST)
"""

from typing import List, Optional, Union
from .lexer import Token, TokenType, Lexer
from .ast_nodes import *

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def error(self, message: str):
        if self.current_token:
            token_info = f"Type: {self.current_token.type}, Value: {self.current_token.value}"
            raise SyntaxError(f"Line {self.current_token.line}, Column {self.current_token.column}: {message} | Token: {token_info}")
        else:
            raise SyntaxError(f"Unexpected end of input: {message}")
    
    def advance(self):
        """Move to the next token"""
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
    
    def skip_whitespace_in_collections(self):
        """Skip newlines and indentation tokens when parsing collections"""
        while (self.current_token and 
               self.current_token.type in (TokenType.NEWLINE, TokenType.INDENT, TokenType.DEDENT) and
               self.pos < len(self.tokens) - 1):
            self.advance()
    
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
        # Skip leading INDENT tokens
        while self.match(TokenType.INDENT):
            self.advance()
        while self.current_token and not self.match(TokenType.EOF):
            # Skip trailing DEDENT tokens before EOF
            while self.match(TokenType.DEDENT):
                self.advance()
            if self.match(TokenType.EOF):
                break
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
            while self.match(TokenType.INDENT):
                self.advance()
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
        elif self.match(TokenType.FOR):
            return self.parse_for_statement()
        elif self.match(TokenType.TRY):
            return self.parse_try_statement()
        elif self.match(TokenType.THROW):
            return self.parse_throw_statement()
        elif self.match(TokenType.RETURN):
            return self.parse_return_statement()
        elif self.match(TokenType.BREAK):
            return self.parse_break_statement()
        elif self.match(TokenType.CONTINUE):
            return self.parse_continue_statement()
        elif self.match(TokenType.IMPORT):
            return self.parse_import_statement()
        elif self.match(TokenType.FROM):
            return self.parse_import_statement()  # Will handle both import types
        elif self.match(TokenType.NEWLINE):
            self.advance()
            return None
        elif self.match(TokenType.IDENTIFIER):
            # Could be a method call or other expression statement
            # Look ahead to see if this is a method call
            next_token = self.peek()
            if next_token and next_token.type == TokenType.DOT:
                # This might be a method call, try to parse it as an expression statement
                expr = self.parse_expression()
                if isinstance(expr, MethodCall):
                    # Create a wrapper function call for the method call
                    return CallStatement(FunctionCall("_method_call", [expr]))
                else:
                    self.error("Expression statements are not yet supported")
            else:
                token_val = self.current_token.value if self.current_token and hasattr(self.current_token, 'value') else None
                self.error(f"Unexpected token: {token_val}")
        else:
            token_val = self.current_token.value if self.current_token and hasattr(self.current_token, 'value') else None
            self.error(f"Unexpected token: {token_val}")
    
    def parse_say_statement(self) -> SayStatement:
        """Parse: Say <expression>"""
        self.consume(TokenType.SAY)
        expression = self.parse_expression()
        return SayStatement(expression)
    
    def parse_let_statement(self) -> LetStatement:
        """Parse: Let <identifier> be <expression> or Let this.<property> be <expression>"""
        self.consume(TokenType.LET)
        
        # Handle object property assignment (this.property)
        if self.match(TokenType.IDENTIFIER) and self.current_token and hasattr(self.current_token, 'value') and self.current_token.value == "this":
            self.advance()
            self.consume(TokenType.DOT)
            property_token = self.consume(TokenType.IDENTIFIER)
            if not property_token or not hasattr(property_token, 'value'):
                self.error("Expected property name after 'this.'")
            property_name = property_token.value
            self.consume(TokenType.BE)
            value = self.parse_expression()
            return ObjectPropertyAssignment("this", property_name, value)
        
        # Regular variable assignment
        name_token = self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.BE)
        value = self.parse_expression()
        if not name_token or not hasattr(name_token, 'value'):
            self.error("Expected variable name after 'Let'")
        name_val = name_token.value
        return LetStatement(name_val, value)
    
    def parse_function_definition(self) -> FunctionDefinition:
        """Parse: Define <name> with <param1>, <param2>: <body>"""
        self.consume(TokenType.DEFINE)
        name_token = self.consume(TokenType.IDENTIFIER)
        
        parameters = []
        if self.match(TokenType.WITH):
            self.advance()
            # Parse parameter list
            if self.match(TokenType.IDENTIFIER):
                if self.current_token and hasattr(self.current_token, 'value'):
                    if self.current_token and hasattr(self.current_token, 'value'):
                        parameters.append(self.current_token.value)
                self.advance()
                
                while self.match(TokenType.COMMA):
                    self.advance()
                    param_token = self.consume(TokenType.IDENTIFIER)
                    parameters.append(param_token.value if param_token and hasattr(param_token, 'value') else None)
        
        self.consume(TokenType.COLON)
        self.skip_newlines()
        
        # Parse function body (indented block)
        if self.match(TokenType.INDENT):
            body = self.parse_block()
        else:
            self.error("Expected indented block after function definition")
        
        # Check if this is a class definition (first character is uppercase)
        if not name_token or not hasattr(name_token, 'value'):
            self.error("Expected function or class name after 'Define'")
        if name_token.value[0].isupper():
            return ClassDefinition(name_token.value, parameters, body)
        else:
            return FunctionDefinition(name_token.value, parameters, body)
    
    def parse_call_statement(self) -> CallStatement:
        """Parse: Call <function_name> with <arg1>, <arg2> or Call <object>.<method> with <args>"""
        self.consume(TokenType.CALL)
        
        # Parse object.method or function_name
        name_token = self.consume(TokenType.IDENTIFIER)
        if not name_token or not hasattr(name_token, 'value'):
            self.error("Expected function or object name after 'Call'")
        name = name_token.value
        
        # Check for method call (object.method)
        if self.match(TokenType.DOT):
            self.advance()
            method_token = self.consume(TokenType.IDENTIFIER)
            if not method_token or not hasattr(method_token, 'value'):
                self.error("Expected method name after '.' in call statement")
            method_name = method_token.value
            
            arguments = []
            if self.match(TokenType.WITH):
                self.advance()
                # Parse argument list
                arguments.append(self.parse_expression())
                
                while self.match(TokenType.COMMA):
                    self.advance()
                    arguments.append(self.parse_expression())
            
            method_call = MethodCall(name, method_name, arguments)
            # Wrap MethodCall in a FunctionCall for CallStatement
            function_call = FunctionCall(f"{name}.{method_name}", arguments)
            return CallStatement(function_call)
        else:
            # Regular function call
            arguments = []
            if self.match(TokenType.WITH):
                self.advance()
                # Parse argument list
                arguments.append(self.parse_expression())
                
                while self.match(TokenType.COMMA):
                    self.advance()
                    arguments.append(self.parse_expression())
            
            function_call = FunctionCall(name, arguments)
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
    
    def parse_for_statement(self) -> Statement:
        """Parse enhanced for-loop statements with different iteration patterns"""
        self.consume(TokenType.FOR)
        
        # Check for different patterns:
        # 1. For each item in collection do:
        # 2. For item at index in collection do:
        # 3. For key, value in collection do: (unpacking)
        
        if self.match(TokenType.EACH):
            # Standard for-each loop: For each item in collection do:
            self.advance()  # consume 'each'
            variable = self.consume(TokenType.IDENTIFIER).value
            self.consume(TokenType.IN)
            collection = self.parse_expression()
            self.consume(TokenType.DO)
            self.consume(TokenType.COLON)
            self.skip_newlines()
            
            # Parse body
            if self.match(TokenType.INDENT):
                body = self.parse_block()
            else:
                self.error("Expected indented block after 'do:'")
            
            return ForStatement(variable, collection, body)
            
        else:
            # Check for patterns that start with an identifier
            first_var = self.consume(TokenType.IDENTIFIER).value
            
            if self.match(TokenType.AT):
                # Indexed iteration: For item at index in collection do:
                self.advance()  # consume 'at'
                index_var = self.consume(TokenType.IDENTIFIER).value
                self.consume(TokenType.IN)
                collection = self.parse_expression()
                self.consume(TokenType.DO)
                self.consume(TokenType.COLON)
                self.skip_newlines()
                
                # Parse body
                if self.match(TokenType.INDENT):
                    body = self.parse_block()
                else:
                    self.error("Expected indented block after 'do:'")
                
                return ForIndexStatement(first_var, index_var, collection, body)
                
            elif self.match(TokenType.COMMA):
                # Unpacking iteration: For key, value in collection do:
                variables = [first_var]
                while self.match(TokenType.COMMA):
                    self.advance()  # consume comma
                    variables.append(self.consume(TokenType.IDENTIFIER).value)
                
                self.consume(TokenType.IN)
                collection = self.parse_expression()
                self.consume(TokenType.DO)
                self.consume(TokenType.COLON)
                self.skip_newlines()
                
                # Parse body
                if self.match(TokenType.INDENT):
                    body = self.parse_block()
                else:
                    self.error("Expected indented block after 'do:'")
                
                return ForUnpackStatement(variables, collection, body)
                
            elif self.match(TokenType.IN):
                # Simple iteration: For item in collection do:
                self.advance()  # consume 'in'
                collection = self.parse_expression()
                self.consume(TokenType.DO)
                self.consume(TokenType.COLON)
                self.skip_newlines()
                
                # Parse body
                if self.match(TokenType.INDENT):
                    body = self.parse_block()
                else:
                    self.error("Expected indented block after 'do:'")
                
                return ForStatement(first_var, collection, body)
                
            else:
                self.error("Expected 'at', ',', or 'in' after variable in for statement")
    
    def parse_try_statement(self) -> TryStatement:
        """Parse: Try: <body> Catch <variable>: <catch_body>"""
        self.consume(TokenType.TRY)
        self.consume(TokenType.COLON)
        self.skip_newlines()
        
        # Parse try block
        if self.match(TokenType.INDENT):
            try_block = self.parse_block()
        else:
            self.error("Expected indented block after 'try:'")
        
        # Parse catch block
        self.consume(TokenType.CATCH)
        error_var = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.COLON)
        self.skip_newlines()
        
        if self.match(TokenType.INDENT):
            catch_block = self.parse_block()
        else:
            self.error("Expected indented block after 'catch:'")
        
        return TryStatement(try_block, catch_block, error_var)
    
    def parse_throw_statement(self) -> ThrowStatement:
        """Parse: Throw <expression>"""
        self.consume(TokenType.THROW)
        expression = self.parse_expression()
        return ThrowStatement(expression)
    
    def parse_return_statement(self) -> ReturnStatement:
        """Parse: Return [expression]"""
        self.consume(TokenType.RETURN)
        expression = None
        if not self.match(TokenType.NEWLINE, TokenType.DEDENT, TokenType.EOF):
            expression = self.parse_expression()
        return ReturnStatement(expression)
    
    def parse_break_statement(self) -> BreakStatement:
        """Parse: Break"""
        self.consume(TokenType.BREAK)
        return BreakStatement()
    
    def parse_continue_statement(self) -> ContinueStatement:
        """Parse: Continue"""
        self.consume(TokenType.CONTINUE)
        return ContinueStatement()
    
    def parse_import_statement(self) -> Statement:
        """Parse: Import <module_name> [as <alias>] | From <module> import <items>"""
        
        # Handle "from module import" statements
        if self.match(TokenType.FROM):
            return self.parse_from_import_statement()
        
        # Handle regular "import module" statements
        self.consume(TokenType.IMPORT)
        module_name = self.consume(TokenType.IDENTIFIER).value
        
        # Check for optional "as alias"
        alias = None
        if self.match(TokenType.AS):
            self.advance()
            alias = self.consume(TokenType.IDENTIFIER).value
        
        return ImportStatement(module_name, alias)
    
    def parse_from_import_statement(self) -> FromImportStatement:
        """Parse: From <module> import <item1>, <item2> [as <alias1>, <alias2>]"""
        self.consume(TokenType.FROM)
        module_name = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.IMPORT)
        
        # Parse imported items
        imports = []
        aliases = []
        
        # First import item
        imports.append(self.consume(TokenType.IDENTIFIER).value)
        
        # Check for alias
        if self.match(TokenType.AS):
            self.advance()
            aliases.append(self.consume(TokenType.IDENTIFIER).value)
        else:
            aliases.append(None)
        
        # Additional import items
        while self.match(TokenType.COMMA):
            self.advance()
            imports.append(self.consume(TokenType.IDENTIFIER).value)
            
            # Check for alias
            if self.match(TokenType.AS):
                self.advance()
                aliases.append(self.consume(TokenType.IDENTIFIER).value)
            else:
                aliases.append(None)
        
        return FromImportStatement(module_name, imports, aliases)
    
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
            operator = self.current_token.value if self.current_token and hasattr(self.current_token, 'value') else None
            if operator is None:
                self.error("Expected operator in expression")
            self.advance()
            right = self.parse_and_expression()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_and_expression(self) -> Expression:
        """Parse AND expressions"""
        expr = self.parse_equality_expression()
        
        while self.match(TokenType.AND):
            operator = self.current_token.value if self.current_token and hasattr(self.current_token, 'value') else None
            if operator is None:
                self.error("Expected operator in expression")
            self.advance()
            right = self.parse_equality_expression()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_equality_expression(self) -> Expression:
        """Parse equality expressions (equals, not equals)"""
        expr = self.parse_comparison_expression()
        
        while self.match(TokenType.EQUALS, TokenType.NOT_EQUALS):
            operator = self.current_token.value if self.current_token and hasattr(self.current_token, 'value') else None
            if operator is None:
                self.error("Expected operator in expression")
            self.advance()
            right = self.parse_comparison_expression()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_comparison_expression(self) -> Expression:
        """Parse comparison expressions (greater, less)"""
        expr = self.parse_additive_expression()
        
        while self.match(TokenType.GREATER, TokenType.LESS):
            operator = self.current_token.value if self.current_token and hasattr(self.current_token, 'value') else None
            if operator is None:
                self.error("Expected operator in expression")
            self.advance()
            # Handle "than" keyword after greater/less
            if self.match(TokenType.IDENTIFIER) and self.current_token and hasattr(self.current_token, 'value') and self.current_token.value == "than":
                self.advance()
            right = self.parse_additive_expression()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_additive_expression(self) -> Expression:
        """Parse addition and subtraction"""
        expr = self.parse_multiplicative_expression()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token.value if self.current_token and hasattr(self.current_token, 'value') else None
            if operator is None:
                self.error("Expected operator in expression")
            self.advance()
            right = self.parse_multiplicative_expression()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_multiplicative_expression(self) -> Expression:
        """Parse multiplication, division, and modulo"""
        expr = self.parse_unary_expression()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self.current_token.value if self.current_token and hasattr(self.current_token, 'value') else None
            if operator is None:
                self.error("Expected operator in expression")
            self.advance()
            right = self.parse_unary_expression()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_unary_expression(self) -> Expression:
        """Parse unary expressions (not, -, +)"""
        if self.match(TokenType.NOT, TokenType.MINUS, TokenType.PLUS):
            operator = self.current_token.value if self.current_token and hasattr(self.current_token, 'value') else None
            if operator is None:
                self.error("Expected operator in expression")
            self.advance()
            operand = self.parse_unary_expression()
            return UnaryOp(operator, operand)
        
        return self.parse_primary_expression()
    
    def parse_primary_expression(self) -> Expression:
        """Parse primary expressions (literals, identifiers, function calls, parentheses, lists, dicts, etc.)"""
        # Handle string literals
        if self.match(TokenType.STRING):
            value = self.current_token.value if self.current_token and hasattr(self.current_token, 'value') else ""
            self.advance()
            # Remove quotes from string literal
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            return StringLiteral(value)
        
        # Handle number literals (integer and float)
        if self.match(TokenType.NUMBER):
            value = self.current_token.value if self.current_token and hasattr(self.current_token, 'value') else "0"
            self.advance()
            if '.' in str(value):
                return NumberLiteral(float(value))
            else:
                return NumberLiteral(int(value))
        
        # Handle list literals [1, 2, 3]
        if self.match(TokenType.LBRACKET):
            return self.parse_list_literal()
        
        # Handle dictionary literals {"key": "value"}
        if self.match(TokenType.LBRACE):
            return self.parse_dictionary_literal()
        
        # Handle object instantiation (new ClassName with args)
        if self.match(TokenType.NEW):
            return self.parse_object_instantiation()
        
        # Handle identifiers, property access, method calls
        if self.match(TokenType.IDENTIFIER):
            # Check for special literals first
            if self.current_token and hasattr(self.current_token, 'value'):
                if self.current_token.value == "true":
                    self.advance()
                    return BooleanLiteral(True)
                elif self.current_token.value == "false":
                    self.advance()
                    return BooleanLiteral(False)
                elif self.current_token.value in ["null", "none"]:
                    self.advance()
                    return NullLiteral()
            
            expr = self.parse_identifier_expression()
            
            # Handle chained property access and method calls
            while self.match(TokenType.DOT):
                self.advance()
                property_name = self.consume(TokenType.IDENTIFIER).value
                
                # Check if it's a method call
                if self.match(TokenType.LPAREN):
                    self.advance()  # consume '('
                    arguments = []
                    
                    if not self.match(TokenType.RPAREN):
                        arguments.append(self.parse_expression())
                        while self.match(TokenType.COMMA):
                            self.advance()
                            arguments.append(self.parse_expression())
                    
                    self.consume(TokenType.RPAREN)
                    if isinstance(expr, Identifier):
                        expr = MethodCall(expr.name, property_name, arguments)
                    else:
                        expr = MethodCall(str(expr), property_name, arguments)
                else:
                    # Check if this is a built-in collection method that should be treated as a method call
                    builtin_methods = ['length', 'keys', 'values', 'upper', 'lower']
                    if property_name in builtin_methods:
                        # Treat as method call with no arguments
                        if isinstance(expr, Identifier):
                            expr = MethodCall(expr.name, property_name, [])
                        else:
                            expr = MethodCall(str(expr), property_name, [])
                    else:
                        # Property access
                        expr = PropertyAccess(expr, property_name)
            
            # Handle array/dictionary indexing
            while self.match(TokenType.LBRACKET):
                self.advance()
                index = self.parse_expression()
                self.consume(TokenType.RBRACKET)
                expr = IndexAccess(expr, index)
            
            return expr
        
        # Handle parenthesized expressions
        if self.match(TokenType.LPAREN):
            self.advance()  # consume '('
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr
        
        token_val = self.current_token.value if self.current_token and hasattr(self.current_token, 'value') else None
        self.error(f"Unexpected token in expression: {token_val}")
    
    def parse_list_literal(self) -> Union[ListLiteral, ListComprehension]:
        """Parse [element1, element2, ...] or [expr for var in iterable if condition]"""
        self.consume(TokenType.LBRACKET)
        
        # Skip any whitespace after opening bracket
        self.skip_whitespace_in_collections()
        
        if self.match(TokenType.RBRACKET):
            # Empty list
            self.advance()
            return ListLiteral([])
        
        # Parse the first expression
        first_expr = self.parse_expression()
        
        # Skip whitespace after first expression
        self.skip_whitespace_in_collections()
        
        # Check if this is a list comprehension (has "for" keyword)
        if self.match(TokenType.FOR):
            return self.parse_list_comprehension_from_expr(first_expr)
        
        # Regular list literal
        elements = [first_expr]
        
        while self.match(TokenType.COMMA):
            self.advance()
            
            # Skip whitespace after comma
            self.skip_whitespace_in_collections()
            
            if self.match(TokenType.RBRACKET):  # Allow trailing comma
                break
                
            elements.append(self.parse_expression())
            
            # Skip whitespace after each element
            self.skip_whitespace_in_collections()
        
        # Skip any whitespace before closing bracket
        self.skip_whitespace_in_collections()
        self.consume(TokenType.RBRACKET)
        return ListLiteral(elements)
    
    def parse_list_comprehension_from_expr(self, transform_expr: Expression) -> ListComprehension:
        """Parse list comprehension from the transform expression: for var in iterable if condition"""
        # Consume the "for" keyword
        self.consume(TokenType.FOR)
        
        # Expect "each" keyword
        if self.match(TokenType.EACH):
            self.advance()
        
        # Get the loop variable
        if not self.match(TokenType.IDENTIFIER):
            line = self.current_token.line if self.current_token else 0
            column = self.current_token.column if self.current_token else 0
            raise SyntaxError(f"Line {line}, Column {column}: Expected variable name in list comprehension")
        
        variable = self.current_token.value if self.current_token else ""
        self.advance()
        
        # Expect "in" keyword
        if not self.match(TokenType.IN):
            line = self.current_token.line if self.current_token else 0
            column = self.current_token.column if self.current_token else 0
            raise SyntaxError(f"Line {line}, Column {column}: Expected 'in' in list comprehension")
        self.advance()
        
        # Parse the iterable expression
        iterable = self.parse_expression()
        
        # Check for optional "if" condition
        condition = None
        if self.match(TokenType.IF):
            self.advance()
            condition = self.parse_expression()
        
        # Consume closing bracket
        self.skip_whitespace_in_collections()
        self.consume(TokenType.RBRACKET)
        
        return ListComprehension(transform_expr, variable, iterable, condition)
    
    def parse_dictionary_literal(self) -> DictionaryLiteral:
        """Parse {"key": value, "key2": value2} with support for multi-line format"""
        self.consume(TokenType.LBRACE)
        pairs = []
        
        # Skip any whitespace after opening brace
        self.skip_whitespace_in_collections()
        
        if not self.match(TokenType.RBRACE):
            # Parse first key-value pair
            key = self.parse_expression()
            self.consume(TokenType.COLON)
            value = self.parse_expression()
            pairs.append((key, value))
            
            while self.match(TokenType.COMMA):
                self.advance()
                
                # Skip whitespace after comma
                self.skip_whitespace_in_collections()
                
                if self.match(TokenType.RBRACE):  # Allow trailing comma
                    break
                    
                key = self.parse_expression()
                self.consume(TokenType.COLON)
                value = self.parse_expression()
                pairs.append((key, value))
        
        # Skip any whitespace before closing brace
        self.skip_whitespace_in_collections()
        self.consume(TokenType.RBRACE)
        return DictionaryLiteral(pairs)
    
    def parse_object_instantiation(self) -> ObjectInstantiation:
        """Parse: new ClassName with arg1, arg2"""
        self.consume(TokenType.NEW)
        class_name = self.consume(TokenType.IDENTIFIER).value
        
        arguments = []
        if self.match(TokenType.WITH):
            self.advance()
            arguments.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                self.advance()
                arguments.append(self.parse_expression())
        
        return ObjectInstantiation(class_name, arguments)
    
    def parse_identifier_expression(self) -> Expression:
        """Parse identifier that might be a function call"""
        name = self.current_token.value if self.current_token and hasattr(self.current_token, 'value') else None
        if name is None:
            self.error("Expected name in expression")
        self.advance()
        
        # Check for function call with parentheses
        if self.match(TokenType.LPAREN):
            self.advance()  # consume '('
            arguments = []
            
            if not self.match(TokenType.RPAREN):
                arguments.append(self.parse_expression())
                while self.match(TokenType.COMMA):
                    self.advance()
                    arguments.append(self.parse_expression())
            
            self.consume(TokenType.RPAREN)
            return FunctionCall(name, arguments)
        
        return Identifier(name)

def parse_convo(text: str) -> Program:
    """Convenience function to parse Convo source code"""
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()
