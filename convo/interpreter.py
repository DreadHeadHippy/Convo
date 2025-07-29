"""
Interpreter for the Convo programming language
Executes the Abstract Syntax Tree (AST)
"""

from typing import Any, Dict, List, Optional
from .ast_nodes import *
from .builtins import BUILTIN_FUNCTIONS

class ConvoFunction:
    def __init__(self, name: str, parameters: List[str], body: List[Statement], closure: Dict[str, Any]):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.closure = closure.copy()  # Capture the closure environment

class ConvoClass:
    def __init__(self, name: str, constructor_params: List[str], methods: Dict[str, ConvoFunction], attributes: Dict[str, Any] = None):
        self.name = name
        self.constructor_params = constructor_params
        self.methods = methods
        self.attributes = attributes or {}

class ConvoObject:
    def __init__(self, class_def: ConvoClass, instance_vars: Dict[str, Any] = None):
        self.class_def = class_def
        self.instance_vars = instance_vars or {}

class ConvoRuntimeError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class ReturnException(Exception):
    def __init__(self, value: Any = None):
        self.value = value

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

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
        
        # Built-in functions
        for name, func in BUILTIN_FUNCTIONS.items():
            self.global_env.define(name, func)
    
    def interpret(self, program: Program) -> List[str]:
        """Interpret a Convo program and return output"""
        self.output = []
        try:
            for statement in program.statements:
                self.execute_statement(statement)
        except ConvoRuntimeError as e:
            self.output.append(f"Runtime Error: {e.message}")
        except ReturnException:
            pass  # Allow returns at top level
        return self.output
    
    def execute_statement(self, statement: Statement) -> Any:
        """Execute a statement"""
        if isinstance(statement, SayStatement):
            return self.execute_say_statement(statement)
        elif isinstance(statement, LetStatement):
            return self.execute_let_statement(statement)
        elif isinstance(statement, FunctionDefinition):
            return self.execute_function_definition(statement)
        elif isinstance(statement, ClassDefinition):
            return self.execute_class_definition(statement)
        elif isinstance(statement, CallStatement):
            return self.execute_call_statement(statement)
        elif isinstance(statement, IfStatement):
            return self.execute_if_statement(statement)
        elif isinstance(statement, WhileStatement):
            return self.execute_while_statement(statement)
        elif isinstance(statement, ForStatement):
            return self.execute_for_statement(statement)
        elif isinstance(statement, TryStatement):
            return self.execute_try_statement(statement)
        elif isinstance(statement, ThrowStatement):
            return self.execute_throw_statement(statement)
        elif isinstance(statement, ReturnStatement):
            return self.execute_return_statement(statement)
        elif isinstance(statement, BreakStatement):
            raise BreakException()
        elif isinstance(statement, ContinueStatement):
            raise ContinueException()
        elif isinstance(statement, ObjectPropertyAssignment):
            return self.execute_object_property_assignment(statement)
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
    
    def execute_class_definition(self, statement: ClassDefinition) -> None:
        """Execute a class definition"""
        methods = {}
        attributes = {}
        
        # Process class body to separate methods and attributes
        for stmt in statement.body:
            if isinstance(stmt, FunctionDefinition):
                function = ConvoFunction(
                    stmt.name,
                    stmt.parameters,
                    stmt.body,
                    self.current_env.variables
                )
                methods[stmt.name] = function
            elif isinstance(stmt, LetStatement):
                # Class attribute
                value = self.evaluate_expression(stmt.value)
                attributes[stmt.name] = value
        
        class_def = ConvoClass(statement.name, statement.constructor_params, methods, attributes)
        self.current_env.define(statement.name, class_def)
    
    def execute_call_statement(self, statement: CallStatement) -> None:
        """Execute a function call statement"""
        if isinstance(statement.function_call, MethodCall):
            self.evaluate_method_call(statement.function_call)
        else:
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
            
            try:
                for stmt in statement.body:
                    self.execute_statement(stmt)
            except BreakException:
                break
            except ContinueException:
                continue
    
    def execute_for_statement(self, statement: ForStatement) -> None:
        """Execute a For statement"""
        iterable = self.evaluate_expression(statement.iterable)
        
        if not isinstance(iterable, list):
            raise ConvoRuntimeError(f"Cannot iterate over {type(iterable)}")
        
        # Create new scope for loop variable
        previous_env = self.current_env
        self.current_env = Environment(previous_env)
        
        try:
            for item in iterable:
                self.current_env.define(statement.variable, item)
                
                try:
                    for stmt in statement.body:
                        self.execute_statement(stmt)
                except BreakException:
                    break
                except ContinueException:
                    continue
        finally:
            self.current_env = previous_env
    
    def execute_try_statement(self, statement: TryStatement) -> None:
        """Execute a Try statement"""
        try:
            for stmt in statement.try_block:
                self.execute_statement(stmt)
        except Exception as e:
            # Create new scope for error variable
            previous_env = self.current_env
            self.current_env = Environment(previous_env)
            
            try:
                # Bind error to the catch variable
                error_message = str(e) if not isinstance(e, ConvoRuntimeError) else e.message
                self.current_env.define(statement.error_variable, error_message)
                
                for stmt in statement.catch_block:
                    self.execute_statement(stmt)
            finally:
                self.current_env = previous_env
    
    def execute_throw_statement(self, statement: ThrowStatement) -> None:
        """Execute a Throw statement"""
        value = self.evaluate_expression(statement.expression)
        raise ConvoRuntimeError(str(value))
    
    def execute_return_statement(self, statement: ReturnStatement) -> None:
        """Execute a Return statement"""
        value = None
        if statement.value:
            value = self.evaluate_expression(statement.value)
        raise ReturnException(value)
    
    def execute_object_property_assignment(self, statement: ObjectPropertyAssignment) -> None:
        """Execute object property assignment (this.property = value)"""
        if statement.object_name == "this":
            # Find the current object context
            try:
                obj = self.current_env.get("this")
                if isinstance(obj, ConvoObject):
                    value = self.evaluate_expression(statement.value)
                    obj.instance_vars[statement.property_name] = value
                else:
                    raise ConvoRuntimeError("'this' is not an object")
            except ConvoRuntimeError:
                raise ConvoRuntimeError("Cannot use 'this' outside of object context")
        else:
            raise ConvoRuntimeError(f"Unsupported object property assignment: {statement.object_name}")
    
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
            return self.evaluate_literal(expression)
        elif isinstance(expression, Identifier):
            return self.current_env.get(expression.name)
        elif isinstance(expression, BinaryOp):
            return self.evaluate_binary_op(expression)
        elif isinstance(expression, UnaryOp):
            return self.evaluate_unary_op(expression)
        elif isinstance(expression, FunctionCall):
            return self.evaluate_function_call(expression)
        elif isinstance(expression, MethodCall):
            return self.evaluate_method_call(expression)
        elif isinstance(expression, ListLiteral):
            return self.evaluate_list_literal(expression)
        elif isinstance(expression, DictionaryLiteral):
            return self.evaluate_dictionary_literal(expression)
        elif isinstance(expression, IndexAccess):
            return self.evaluate_index_access(expression)
        elif isinstance(expression, PropertyAccess):
            return self.evaluate_property_access(expression)
        elif isinstance(expression, ObjectInstantiation):
            return self.evaluate_object_instantiation(expression)
        else:
            raise ConvoRuntimeError(f"Unknown expression type: {type(expression)}")
    
    def evaluate_literal(self, expression: Literal) -> Any:
        """Evaluate a literal expression"""
        value = expression.value
        
        # Handle special literal values
        if value == "null":
            return None
        elif value == "true":
            return True
        elif value == "false":
            return False
        else:
            return value
    
    def evaluate_list_literal(self, expression: ListLiteral) -> List[Any]:
        """Evaluate a list literal"""
        return [self.evaluate_expression(element) for element in expression.elements]
    
    def evaluate_dictionary_literal(self, expression: DictionaryLiteral) -> Dict[str, Any]:
        """Evaluate a dictionary literal"""
        result = {}
        for key_expr, value_expr in expression.pairs:
            key = self.evaluate_expression(key_expr)
            value = self.evaluate_expression(value_expr)
            result[str(key)] = value
        return result
    
    def evaluate_index_access(self, expression: IndexAccess) -> Any:
        """Evaluate index access (obj[index])"""
        obj = self.evaluate_expression(expression.object)
        index = self.evaluate_expression(expression.index)
        
        if isinstance(obj, list):
            if not isinstance(index, int):
                raise ConvoRuntimeError(f"List index must be an integer, got {type(index)}")
            if index < 0 or index >= len(obj):
                raise ConvoRuntimeError(f"List index {index} out of range")
            return obj[index]
        elif isinstance(obj, dict):
            key = str(index)
            if key not in obj:
                raise ConvoRuntimeError(f"Dictionary key '{key}' not found")
            return obj[key]
        else:
            raise ConvoRuntimeError(f"Cannot index {type(obj)}")
    
    def evaluate_property_access(self, expression: PropertyAccess) -> Any:
        """Evaluate property access (obj.property)"""
        obj = self.evaluate_expression(expression.object)
        
        if isinstance(obj, ConvoObject):
            # Check instance variables first
            if expression.property_name in obj.instance_vars:
                return obj.instance_vars[expression.property_name]
            # Check class attributes
            elif expression.property_name in obj.class_def.attributes:
                return obj.class_def.attributes[expression.property_name]
            # Check methods
            elif expression.property_name in obj.class_def.methods:
                return obj.class_def.methods[expression.property_name]
            else:
                raise ConvoRuntimeError(f"Object has no property '{expression.property_name}'")
        else:
            raise ConvoRuntimeError(f"Cannot access property of {type(obj)}")
    
    def evaluate_object_instantiation(self, expression: ObjectInstantiation) -> ConvoObject:
        """Evaluate object instantiation (new ClassName with args)"""
        class_def = self.current_env.get(expression.class_name)
        
        if not isinstance(class_def, ConvoClass):
            raise ConvoRuntimeError(f"'{expression.class_name}' is not a class")
        
        # Evaluate constructor arguments
        arguments = [self.evaluate_expression(arg) for arg in expression.arguments]
        
        # Check parameter count
        if len(arguments) != len(class_def.constructor_params):
            raise ConvoRuntimeError(
                f"Class '{class_def.name}' constructor expects {len(class_def.constructor_params)} arguments, "
                f"got {len(arguments)}"
            )
        
        # Create new object instance
        obj = ConvoObject(class_def)
        
        # Create constructor environment
        previous_env = self.current_env
        constructor_env = Environment(self.global_env)
        
        # Bind 'this' to the new object
        constructor_env.define("this", obj)
        
        # Bind constructor parameters
        for param, arg in zip(class_def.constructor_params, arguments):
            constructor_env.define(param, arg)
        
        self.current_env = constructor_env
        
        try:
            # Execute constructor body (class body acts as constructor)
            for stmt in class_def.methods.get('__init__', ConvoFunction('__init__', [], [], {})).body:
                self.execute_statement(stmt)
            
            # If no explicit constructor, execute the class body as constructor
            for name, method in class_def.methods.items():
                if name != '__init__':
                    # Bind methods to the object
                    obj.instance_vars[name] = method
        finally:
            self.current_env = previous_env
        
        return obj
    
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
        
        # Check if it's a built-in function
        if callable(function) and not isinstance(function, ConvoFunction):
            # Built-in function
            arguments = [self.evaluate_expression(arg) for arg in expression.arguments]
            try:
                return function(*arguments)
            except Exception as e:
                raise ConvoRuntimeError(f"Error calling built-in function '{expression.name}': {str(e)}")
        
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
        except ReturnException as ret:
            return ret.value
        finally:
            self.current_env = previous_env
        
        return None  # Functions return null by default
    
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
        elif isinstance(value, list):
            # Convert list to string representation
            elements = [self.stringify(item) for item in value]
            return "[" + ", ".join(elements) + "]"
        elif isinstance(value, dict):
            # Convert dict to string representation
            pairs = [f'"{k}": {self.stringify(v)}' for k, v in value.items()]
            return "{" + ", ".join(pairs) + "}"
        else:
            return str(value)
    
    def evaluate_method_call(self, expression: MethodCall) -> Any:
        """Evaluate a method call"""
        obj = self.current_env.get(expression.object_name)
        
        if isinstance(obj, ConvoObject):
            # Get the method from the object's class
            if expression.method_name not in obj.class_def.methods:
                raise ConvoRuntimeError(f"Object has no method '{expression.method_name}'")
            
            method = obj.class_def.methods[expression.method_name]
            
            # Evaluate arguments
            arguments = [self.evaluate_expression(arg) for arg in expression.arguments]
            
            # Check parameter count
            if len(arguments) != len(method.parameters):
                raise ConvoRuntimeError(
                    f"Method '{method.name}' expects {len(method.parameters)} arguments, "
                    f"got {len(arguments)}"
                )
            
            # Create new environment for method execution
            previous_env = self.current_env
            method_env = Environment(self.global_env)
            
            # Bind 'this' to the object
            method_env.define("this", obj)
            
            # Copy closure variables
            for name, value in method.closure.items():
                method_env.define(name, value)
            
            # Bind parameters to arguments
            for param, arg in zip(method.parameters, arguments):
                method_env.define(param, arg)
            
            self.current_env = method_env
            
            try:
                # Execute method body
                for statement in method.body:
                    self.execute_statement(statement)
            except ReturnException as ret:
                return ret.value
            finally:
                self.current_env = previous_env
            
            return None  # Methods return null by default
        else:
            raise ConvoRuntimeError(f"Cannot call method on {type(obj)}")
