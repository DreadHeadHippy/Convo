"""
Interpreter for the Convo programming language
Executes the Abstract Syntax Tree (AST)
"""

from typing import Any, Dict, List, Optional
from .ast_nodes import *

class ConvoFunction:
    def __init__(self, name: str, parameters: List[str], body: List[Statement], closure: Dict[str, Any]):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.closure = closure.copy()  # Capture the closure environment

class ConvoRuntimeError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class Environment:
    def __init__(self, parent: Optional['Environment'] = None):
        self.parent = parent
        self.variables: Dict[str, Any] = {}
    
    def define(self, name: str, value: Any):
        """Define a variable in this environment"""
        self.variables[name] = value
    
    def get(self, name: str) -> Any:
        """Get a variable value, searching up the scope chain"""
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise ConvoRuntimeError(f"Undefined variable: {name}")
    
    def set(self, name: str, value: Any):
        """Set a variable value, searching up the scope chain"""
        if name in self.variables:
            self.variables[name] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            raise ConvoRuntimeError(f"Undefined variable: {name}")

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.current_env = self.global_env
        self.output = []  # Store output for testing
        
        # Define built-in functions
        self._define_builtins()
    
    def _define_builtins(self):
        """Define built-in functions and variables"""
        # Built-in constants
        self.global_env.define("true", True)
        self.global_env.define("false", False)
        self.global_env.define("null", None)
    
    def interpret(self, program: Program) -> List[str]:
        """Interpret a Convo program and return output"""
        self.output = []
        try:
            for statement in program.statements:
                self.execute_statement(statement)
        except ConvoRuntimeError as e:
            self.output.append(f"Runtime Error: {e.message}")
        return self.output
    
    def execute_statement(self, statement: Statement) -> Any:
        """Execute a statement"""
        if isinstance(statement, SayStatement):
            return self.execute_say_statement(statement)
        elif isinstance(statement, LetStatement):
            return self.execute_let_statement(statement)
        elif isinstance(statement, FunctionDefinition):
            return self.execute_function_definition(statement)
        elif isinstance(statement, CallStatement):
            return self.execute_call_statement(statement)
        elif isinstance(statement, IfStatement):
            return self.execute_if_statement(statement)
        elif isinstance(statement, WhileStatement):
            return self.execute_while_statement(statement)
        elif isinstance(statement, Block):
            return self.execute_block(statement)
        else:
            raise ConvoRuntimeError(f"Unknown statement type: {type(statement)}")
    
    def execute_say_statement(self, statement: SayStatement) -> None:
        """Execute a Say statement"""
        value = self.evaluate_expression(statement.expression)
        output = self.stringify(value)
        print(output)
        self.output.append(output)
    
    def execute_let_statement(self, statement: LetStatement) -> None:
        """Execute a Let statement (variable assignment)"""
        value = self.evaluate_expression(statement.value)
        self.current_env.define(statement.name, value)
    
    def execute_function_definition(self, statement: FunctionDefinition) -> None:
        """Execute a function definition"""
        function = ConvoFunction(
            statement.name,
            statement.parameters,
            statement.body,
            self.current_env.variables
        )
        self.current_env.define(statement.name, function)
    
    def execute_call_statement(self, statement: CallStatement) -> None:
        """Execute a function call statement"""
        self.evaluate_function_call(statement.function_call)
    
    def execute_if_statement(self, statement: IfStatement) -> None:
        """Execute an If statement"""
        condition_value = self.evaluate_expression(statement.condition)
        
        if self.is_truthy(condition_value):
            for stmt in statement.then_block:
                self.execute_statement(stmt)
        elif statement.else_block:
            for stmt in statement.else_block:
                self.execute_statement(stmt)
    
    def execute_while_statement(self, statement: WhileStatement) -> None:
        """Execute a While statement"""
        while True:
            condition_value = self.evaluate_expression(statement.condition)
            if not self.is_truthy(condition_value):
                break
            
            for stmt in statement.body:
                self.execute_statement(stmt)
    
    def execute_block(self, statement: Block) -> None:
        """Execute a block of statements with a new scope"""
        previous_env = self.current_env
        self.current_env = Environment(previous_env)
        
        try:
            for stmt in statement.statements:
                self.execute_statement(stmt)
        finally:
            self.current_env = previous_env
    
    def evaluate_expression(self, expression: Expression) -> Any:
        """Evaluate an expression and return its value"""
        if isinstance(expression, Literal):
            return expression.value
        elif isinstance(expression, Identifier):
            return self.current_env.get(expression.name)
        elif isinstance(expression, BinaryOp):
            return self.evaluate_binary_op(expression)
        elif isinstance(expression, UnaryOp):
            return self.evaluate_unary_op(expression)
        elif isinstance(expression, FunctionCall):
            return self.evaluate_function_call(expression)
        else:
            raise ConvoRuntimeError(f"Unknown expression type: {type(expression)}")
    
    def evaluate_binary_op(self, expression: BinaryOp) -> Any:
        """Evaluate a binary operation"""
        left = self.evaluate_expression(expression.left)
        right = self.evaluate_expression(expression.right)
        operator = expression.operator
        
        # Arithmetic operations
        if operator == '+':
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)  # String concatenation
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            if right == 0:
                raise ConvoRuntimeError("Division by zero")
            return left / right
        
        # Comparison operations
        elif operator in ['equals', 'is']:
            return left == right
        elif operator in ['not equals', 'is not']:
            return left != right
        elif operator in ['greater', 'greater than']:
            return left > right
        elif operator in ['less', 'less than']:
            return left < right
        
        # Logical operations
        elif operator == 'and':
            return self.is_truthy(left) and self.is_truthy(right)
        elif operator == 'or':
            return self.is_truthy(left) or self.is_truthy(right)
        
        else:
            raise ConvoRuntimeError(f"Unknown binary operator: {operator}")
    
    def evaluate_unary_op(self, expression: UnaryOp) -> Any:
        """Evaluate a unary operation"""
        operand = self.evaluate_expression(expression.operand)
        operator = expression.operator
        
        if operator == 'not':
            return not self.is_truthy(operand)
        elif operator == '-':
            return -operand
        elif operator == '+':
            return +operand
        else:
            raise ConvoRuntimeError(f"Unknown unary operator: {operator}")
    
    def evaluate_function_call(self, expression: FunctionCall) -> Any:
        """Evaluate a function call"""
        function = self.current_env.get(expression.name)
        
        if not isinstance(function, ConvoFunction):
            raise ConvoRuntimeError(f"'{expression.name}' is not a function")
        
        # Evaluate arguments
        arguments = [self.evaluate_expression(arg) for arg in expression.arguments]
        
        # Check parameter count
        if len(arguments) != len(function.parameters):
            raise ConvoRuntimeError(
                f"Function '{function.name}' expects {len(function.parameters)} arguments, "
                f"got {len(arguments)}"
            )
        
        # Create new environment for function execution
        previous_env = self.current_env
        function_env = Environment(self.global_env)
        
        # Copy closure variables
        for name, value in function.closure.items():
            function_env.define(name, value)
        
        # Bind parameters to arguments
        for param, arg in zip(function.parameters, arguments):
            function_env.define(param, arg)
        
        self.current_env = function_env
        
        try:
            # Execute function body
            for statement in function.body:
                self.execute_statement(statement)
        finally:
            self.current_env = previous_env
        
        return None  # Functions don't return values in basic Convo
    
    def is_truthy(self, value: Any) -> bool:
        """Determine if a value is truthy in Convo"""
        if value is None or value is False:
            return False
        if value == 0 or value == "":
            return False
        return True
    
    def stringify(self, value: Any) -> str:
        """Convert a value to its string representation"""
        if value is None:
            return "null"
        elif value is True:
            return "true"
        elif value is False:
            return "false"
        elif isinstance(value, str):
            return value
        else:
            return str(value)
