"""
Interpreter for the Convo programming language
Executes the Abstract Syntax Tree (AST)
"""

from typing import Any, Dict, List, Optional, Union
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
        elif isinstance(statement, ForIndexStatement):
            return self.execute_for_index_statement(statement)
        elif isinstance(statement, ForUnpackStatement):
            return self.execute_for_unpack_statement(statement)
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
        elif isinstance(statement, ImportStatement):
            return self.execute_import_statement(statement)
        elif isinstance(statement, FromImportStatement):
            return self.execute_from_import_statement(statement)
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
        
        # Check if variable exists in parent scopes
        # If it does, update it; otherwise, define it in current scope
        try:
            # Try to find the variable in parent scopes
            if self.current_env.parent:
                self.current_env.parent.get(statement.name)
                # Variable exists in parent scope, so set it there
                self.current_env.set(statement.name, value)
            else:
                # No parent scope, define in current scope
                self.current_env.define(statement.name, value)
        except ConvoRuntimeError:
            # Variable doesn't exist in parent scopes, define in current scope
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
        elif statement.function_call.name == "_method_call" and len(statement.function_call.arguments) == 1:
            # Special handling for method calls wrapped in expressions
            method_call = statement.function_call.arguments[0]
            if isinstance(method_call, MethodCall):
                self.evaluate_method_call(method_call)
            else:
                self.evaluate_expression(method_call)
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
    
    def execute_for_index_statement(self, statement: ForIndexStatement) -> None:
        """Execute a For-Index statement (For item at index in collection)"""
        iterable = self.evaluate_expression(statement.iterable)
        
        if not isinstance(iterable, list):
            raise ConvoRuntimeError(f"Cannot iterate over {type(iterable)}")
        
        # Create new scope for loop variables
        previous_env = self.current_env
        self.current_env = Environment(previous_env)
        
        try:
            for index, item in enumerate(iterable):
                self.current_env.define(statement.item_var, item)
                self.current_env.define(statement.index_var, index)
                
                try:
                    for stmt in statement.body:
                        self.execute_statement(stmt)
                except BreakException:
                    break
                except ContinueException:
                    continue
        finally:
            self.current_env = previous_env
    
    def execute_for_unpack_statement(self, statement: ForUnpackStatement) -> None:
        """Execute a For-Unpack statement (For key, value in collection)"""
        iterable = self.evaluate_expression(statement.iterable)
        
        # Handle different iterable types
        if isinstance(iterable, dict):
            # Iterate over dictionary items
            iterator = iterable.items()
        elif isinstance(iterable, list):
            # Iterate over list, expecting each item to be unpacked
            iterator = iterable
        else:
            raise ConvoRuntimeError(f"Cannot unpack iterate over {type(iterable)}")
        
        # Create new scope for loop variables
        previous_env = self.current_env
        self.current_env = Environment(previous_env)
        
        try:
            for item in iterator:
                # Unpack the item based on expected number of variables
                if isinstance(item, (list, tuple)) and len(item) == len(statement.variables):
                    # Item is a sequence with matching length
                    for var, value in zip(statement.variables, item):
                        self.current_env.define(var, value)
                elif isinstance(item, tuple) and len(item) == 2 and len(statement.variables) == 2:
                    # Handle dictionary items (key, value) pairs
                    self.current_env.define(statement.variables[0], item[0])
                    self.current_env.define(statement.variables[1], item[1])
                else:
                    raise ConvoRuntimeError(f"Cannot unpack {item} into {len(statement.variables)} variables")
                
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
    
    def execute_import_statement(self, statement: ImportStatement) -> None:
        """Execute an Import statement"""
        module_name = statement.module_name.lower()
        
        # Check if module is available and load it
        if module_name == "discord":
            try:
                from .modules.discord_bot import DISCORD_FUNCTIONS
                # Register Discord functions in the current environment
                for name, func in DISCORD_FUNCTIONS.items():
                    self.current_env.define(name, func)
            except ImportError:
                raise ConvoRuntimeError(f"Discord module not available. Install discord.py: pip install discord.py")
        else:
            # For now, only Discord module is supported
            # In the future, we can add a module registry system
            raise ConvoRuntimeError(f"Unknown module: {module_name}")
    
    def execute_from_import_statement(self, statement: FromImportStatement) -> None:
        """Execute a From...Import statement"""
        module_name = statement.module_name.lower()
        
        # Check if module is available and load it
        if module_name == "discord":
            try:
                from .modules.discord_bot import DISCORD_FUNCTIONS
                # Import only the specified functions with optional aliases
                for i, import_name in enumerate(statement.imports):
                    if import_name in DISCORD_FUNCTIONS:
                        # Get the alias if provided, otherwise use the original name
                        alias = statement.aliases[i] if i < len(statement.aliases) and statement.aliases[i] else import_name
                        self.current_env.define(alias, DISCORD_FUNCTIONS[import_name])
                    else:
                        raise ConvoRuntimeError(f"'{import_name}' is not available in discord module")
            except ImportError:
                raise ConvoRuntimeError(f"Discord module not available. Install discord.py: pip install discord.py")
        else:
            # For now, only Discord module is supported
            # In the future, we can add a module registry system
            raise ConvoRuntimeError(f"Unknown module: {module_name}")
    
    def execute_object_property_assignment(self, statement: ObjectPropertyAssignment) -> None:
        """Execute object property assignment (this.property = value)"""
        # Handle both old string format and new Expression format
        if hasattr(statement, 'object_expr'):
            # New format: object_expr is an Expression
            if isinstance(statement.object_expr, Identifier) and statement.object_expr.name == "this":
                object_name = "this"
            else:
                object_name = str(statement.object_expr)
        else:
            # Old format: object_name is a string
            object_name = statement.object_name
            
        if object_name == "this":
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
            raise ConvoRuntimeError(f"Unsupported object property assignment: {object_name}")
    
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
        elif isinstance(expression, StringLiteral):
            return self.evaluate_string_literal(expression)
        elif isinstance(expression, NumberLiteral):
            return self.evaluate_number_literal(expression)
        elif isinstance(expression, BooleanLiteral):
            return self.evaluate_boolean_literal(expression)
        elif isinstance(expression, NullLiteral):
            return self.evaluate_null_literal(expression)
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
        elif isinstance(expression, ListComprehension):
            return self.evaluate_list_comprehension(expression)
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
    
    def evaluate_string_literal(self, expression: StringLiteral) -> str:
        """Evaluate a string literal"""
        return expression.value
    
    def evaluate_number_literal(self, expression: NumberLiteral) -> Union[int, float]:
        """Evaluate a number literal"""
        return expression.value
    
    def evaluate_boolean_literal(self, expression: BooleanLiteral) -> bool:
        """Evaluate a boolean literal"""
        return expression.value
    
    def evaluate_null_literal(self, expression: NullLiteral) -> None:
        """Evaluate a null literal"""
        return None
    
    def evaluate_list_literal(self, expression: ListLiteral) -> List[Any]:
        """Evaluate a list literal"""
        return [self.evaluate_expression(element) for element in expression.elements]
    
    def evaluate_list_comprehension(self, expression: ListComprehension) -> List[Any]:
        """Evaluate a list comprehension: [expr for var in iterable if condition]"""
        # Evaluate the iterable
        iterable = self.evaluate_expression(expression.iterable)
        
        # Ensure iterable is actually iterable
        if not hasattr(iterable, '__iter__'):
            raise ConvoRuntimeError(f"Object of type {type(iterable).__name__} is not iterable")
        
        result = []
        
        # Create a new environment for the loop variable
        loop_env = Environment(parent=self.current_env)
        old_env = self.current_env
        self.current_env = loop_env
        
        try:
            for item in iterable:
                # Bind the loop variable
                loop_env.define(expression.variable, item)
                
                # Check the condition if present
                if expression.condition:
                    condition_result = self.evaluate_expression(expression.condition)
                    if not self.is_truthy(condition_result):
                        continue
                
                # Evaluate the transform expression
                transformed_item = self.evaluate_expression(expression.transform_expr)
                result.append(transformed_item)
        finally:
            # Restore the original environment
            self.current_env = old_env
        
        return result
    
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
        # Handle both old and new IndexAccess formats
        if hasattr(expression, 'object_expr'):
            # New format
            obj = self.evaluate_expression(expression.object_expr)
        else:
            # Old format
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
        # Handle both old and new PropertyAccess formats
        if hasattr(expression, 'object_expr'):
            # New format
            obj = self.evaluate_expression(expression.object_expr)
        else:
            # Old format
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
    
    def evaluate_binary_op(self, expression: BinaryOp) -> Any:
        """Evaluate a binary operation with enhanced type handling"""
        # For logical operations, use short-circuit evaluation
        if expression.operator == 'and':
            left = self.evaluate_expression(expression.left)
            if not self.is_truthy(left):
                return False  # Short-circuit: if left is falsy, return False
            right = self.evaluate_expression(expression.right)
            return self.is_truthy(right)
        
        elif expression.operator == 'or':
            left = self.evaluate_expression(expression.left)
            if self.is_truthy(left):
                return True  # Short-circuit: if left is truthy, return True
            right = self.evaluate_expression(expression.right)
            return self.is_truthy(right)
        
        # For other operations, evaluate both sides
        left = self.evaluate_expression(expression.left)
        right = self.evaluate_expression(expression.right)
        operator = expression.operator
        
        # Enhanced arithmetic operations
        if operator == '+':
            return self.evaluate_addition(left, right)
        elif operator == '-':
            return self.evaluate_subtraction(left, right)
        elif operator == '*':
            return self.evaluate_multiplication(left, right)
        elif operator == '/':
            return self.evaluate_division(left, right)
        elif operator == '%':
            return self.evaluate_modulo(left, right)
        elif operator == '**':
            return self.evaluate_power(left, right)
        
        # Enhanced comparison operations
        elif operator in ['equals', 'is']:
            return self.evaluate_equality(left, right)
        elif operator in ['not equals', 'is not']:
            return not self.evaluate_equality(left, right)
        elif operator in ['greater', 'greater than']:
            return self.evaluate_comparison(left, right, '>')
        elif operator in ['less', 'less than']:
            return self.evaluate_comparison(left, right, '<')
        elif operator in ['greater equal', 'greater than or equal']:
            return self.evaluate_comparison(left, right, '>=')
        elif operator in ['less equal', 'less than or equal']:
            return self.evaluate_comparison(left, right, '<=')
        
        else:
            raise ConvoRuntimeError(f"Unknown binary operator: {operator}")
    
    def evaluate_addition(self, left: Any, right: Any) -> Any:
        """Enhanced addition with smart type handling"""
        # String concatenation
        if isinstance(left, str) or isinstance(right, str):
            return self.stringify(left) + self.stringify(right)
        
        # List concatenation
        if isinstance(left, list) and isinstance(right, list):
            return left + right
        
        # Numeric addition
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left + right
        
        # Try to convert to numbers if possible
        try:
            left_num = float(left) if not isinstance(left, (int, float)) else left
            right_num = float(right) if not isinstance(right, (int, float)) else right
            result = left_num + right_num
            # Return int if both operands were integers
            if isinstance(left, int) and isinstance(right, int):
                return int(result)
            return result
        except (ValueError, TypeError):
            # Fall back to string concatenation
            return self.stringify(left) + self.stringify(right)
    
    def evaluate_subtraction(self, left: Any, right: Any) -> Any:
        """Enhanced subtraction with type checking"""
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            try:
                left = float(left)
                right = float(right)
            except (ValueError, TypeError):
                raise ConvoRuntimeError(f"Cannot subtract {type(right).__name__} from {type(left).__name__}")
        
        result = left - right
        # Return int if both operands were integers
        if isinstance(left, int) and isinstance(right, int):
            return int(result)
        return result
    
    def evaluate_multiplication(self, left: Any, right: Any) -> Any:
        """Enhanced multiplication with type checking"""
        # String repetition
        if isinstance(left, str) and isinstance(right, int):
            return left * right
        if isinstance(left, int) and isinstance(right, str):
            return left * right
        
        # List repetition
        if isinstance(left, list) and isinstance(right, int):
            return left * right
        if isinstance(left, int) and isinstance(right, list):
            return left * right
        
        # Numeric multiplication
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            try:
                left = float(left)
                right = float(right)
            except (ValueError, TypeError):
                raise ConvoRuntimeError(f"Cannot multiply {type(left).__name__} and {type(right).__name__}")
        
        result = left * right
        # Return int if both operands were integers
        if isinstance(left, int) and isinstance(right, int):
            return int(result)
        return result
    
    def evaluate_division(self, left: Any, right: Any) -> Any:
        """Enhanced division with type checking"""
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            try:
                left = float(left)
                right = float(right)
            except (ValueError, TypeError):
                raise ConvoRuntimeError(f"Cannot divide {type(left).__name__} by {type(right).__name__}")
        
        if right == 0:
            raise ConvoRuntimeError("Division by zero")
        
        return left / right
    
    def evaluate_modulo(self, left: Any, right: Any) -> Any:
        """Enhanced modulo operation"""
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            try:
                left = float(left)
                right = float(right)
            except (ValueError, TypeError):
                raise ConvoRuntimeError(f"Cannot compute {type(left).__name__} modulo {type(right).__name__}")
        
        if right == 0:
            raise ConvoRuntimeError("Modulo by zero")
        
        return left % right
    
    def evaluate_power(self, left: Any, right: Any) -> Any:
        """Enhanced power operation"""
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            try:
                left = float(left)
                right = float(right)
            except (ValueError, TypeError):
                raise ConvoRuntimeError(f"Cannot raise {type(left).__name__} to power of {type(right).__name__}")
        
        return left ** right
    
    def evaluate_equality(self, left: Any, right: Any) -> bool:
        """Enhanced equality comparison"""
        # Handle None comparisons
        if left is None or right is None:
            return left is right
        
        # Direct equality for same types
        if type(left) == type(right):
            return left == right
        
        # Numeric equality (int and float)
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left == right
        
        # String comparison
        if isinstance(left, str) or isinstance(right, str):
            return str(left) == str(right)
        
        # Default equality
        return left == right
    
    def evaluate_comparison(self, left: Any, right: Any, op: str) -> bool:
        """Enhanced comparison operations"""
        # Numeric comparisons
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            if op == '>':
                return left > right
            elif op == '<':
                return left < right
            elif op == '>=':
                return left >= right
            elif op == '<=':
                return left <= right
        
        # String comparisons
        if isinstance(left, str) and isinstance(right, str):
            if op == '>':
                return left > right
            elif op == '<':
                return left < right
            elif op == '>=':
                return left >= right
            elif op == '<=':
                return left <= right
        
        # Try to convert to numbers for comparison
        try:
            left_num = float(left) if not isinstance(left, (int, float)) else left
            right_num = float(right) if not isinstance(right, (int, float)) else right
            if op == '>':
                return left_num > right_num
            elif op == '<':
                return left_num < right_num
            elif op == '>=':
                return left_num >= right_num
            elif op == '<=':
                return left_num <= right_num
        except (ValueError, TypeError):
            pass
        
        # Fall back to string comparison
        left_str = self.stringify(left)
        right_str = self.stringify(right)
        if op == '>':
            return left_str > right_str
        elif op == '<':
            return left_str < right_str
        elif op == '>=':
            return left_str >= right_str
        elif op == '<=':
            return left_str <= right_str
        
        return False
    
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
        """Determine if a value is truthy with enhanced literal support"""
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        if isinstance(value, list):
            return len(value) > 0
        if isinstance(value, dict):
            return len(value) > 0
        # For any other type, check if it's falsy in Python
        return bool(value)
    
    def stringify(self, value: Any) -> str:
        """Convert any value to a string representation with enhanced literal support"""
        if value is None:
            return "null"
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, str):
            return value
        if isinstance(value, float):
            # Output whole-number floats as integers
            if value.is_integer():
                return str(int(value))
            else:
                return str(value)
        if isinstance(value, list):
            # Format list nicely with enhanced stringify
            items = [self.stringify(item) for item in value]
            return "[" + ", ".join(items) + "]"
        if isinstance(value, dict):
            # Format dict nicely with enhanced stringify
            pairs = [f'"{k}": {self.stringify(v)}' for k, v in value.items()]
            return "{" + ", ".join(pairs) + "}"
        return str(value)
    
    def evaluate_method_call(self, expression: MethodCall) -> Any:
        """Evaluate a method call"""
        # Handle both old and new MethodCall formats
        if hasattr(expression, 'object_expr'):
            # New format: object_expr is an Expression
            if isinstance(expression.object_expr, Identifier):
                obj = self.current_env.get(expression.object_expr.name)
            else:
                obj = self.evaluate_expression(expression.object_expr)
        else:
            # Old format: object_name is a string
            obj = self.current_env.get(expression.object_name)
        
        # Handle built-in collection methods
        if isinstance(obj, list):
            return self.handle_list_method(obj, expression.method_name, expression.arguments)
        elif isinstance(obj, dict):
            return self.handle_dict_method(obj, expression.method_name, expression.arguments)
        elif isinstance(obj, str):
            return self.handle_string_method(obj, expression.method_name, expression.arguments)
        elif isinstance(obj, ConvoObject):
            # Original object method handling
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
            raise ConvoRuntimeError(f"Cannot call method '{expression.method_name}' on {type(obj)}")
    
    def handle_list_method(self, lst: list, method_name: str, arguments: List[Expression]) -> Any:
        """Handle built-in list methods"""
        args = [self.evaluate_expression(arg) for arg in arguments]
        
        if method_name == "length":
            if len(args) != 0:
                raise ConvoRuntimeError("List.length takes no arguments")
            return len(lst)
        
        elif method_name == "add":
            if len(args) != 1:
                raise ConvoRuntimeError("List.add takes exactly 1 argument")
            lst.append(args[0])
            return None
        
        elif method_name == "remove":
            if len(args) != 1:
                raise ConvoRuntimeError("List.remove takes exactly 1 argument")
            try:
                lst.remove(args[0])
                return None
            except ValueError:
                raise ConvoRuntimeError(f"List.remove: item {args[0]} not found")
        
        elif method_name == "insert":
            if len(args) != 2:
                raise ConvoRuntimeError("List.insert takes exactly 2 arguments (index, item)")
            index, item = args
            if not isinstance(index, int):
                raise ConvoRuntimeError("List.insert: index must be a number")
            try:
                lst.insert(index, item)
                return None
            except IndexError:
                raise ConvoRuntimeError(f"List.insert: index {index} out of range")
        
        elif method_name == "contains":
            if len(args) != 1:
                raise ConvoRuntimeError("List.contains takes exactly 1 argument")
            return args[0] in lst
        
        elif method_name == "clear":
            if len(args) != 0:
                raise ConvoRuntimeError("List.clear takes no arguments")
            lst.clear()
            return None
        
        elif method_name == "reverse":
            if len(args) != 0:
                raise ConvoRuntimeError("List.reverse takes no arguments")
            lst.reverse()
            return None
        
        elif method_name == "sort":
            if len(args) != 0:
                raise ConvoRuntimeError("List.sort takes no arguments")
            try:
                lst.sort()
                return None
            except TypeError:
                raise ConvoRuntimeError("List.sort: items must be comparable")
        
        else:
            raise ConvoRuntimeError(f"List has no method '{method_name}'")
    
    def handle_dict_method(self, dct: dict, method_name: str, arguments: List[Expression]) -> Any:
        """Handle built-in dictionary methods"""
        args = [self.evaluate_expression(arg) for arg in arguments]
        
        if method_name == "length":
            if len(args) != 0:
                raise ConvoRuntimeError("Dictionary.length takes no arguments")
            return len(dct)
        
        elif method_name == "keys":
            if len(args) != 0:
                raise ConvoRuntimeError("Dictionary.keys takes no arguments")
            return list(dct.keys())
        
        elif method_name == "values":
            if len(args) != 0:
                raise ConvoRuntimeError("Dictionary.values takes no arguments")
            return list(dct.values())
        
        elif method_name == "contains":
            if len(args) != 1:
                raise ConvoRuntimeError("Dictionary.contains takes exactly 1 argument")
            return args[0] in dct
        
        elif method_name == "remove":
            if len(args) != 1:
                raise ConvoRuntimeError("Dictionary.remove takes exactly 1 argument")
            key = args[0]
            if key in dct:
                del dct[key]
                return None
            else:
                raise ConvoRuntimeError(f"Dictionary.remove: key {key} not found")
        
        elif method_name == "clear":
            if len(args) != 0:
                raise ConvoRuntimeError("Dictionary.clear takes no arguments")
            dct.clear()
            return None
        
        else:
            raise ConvoRuntimeError(f"Dictionary has no method '{method_name}'")
    
    def handle_string_method(self, s: str, method_name: str, arguments: List[Expression]) -> Any:
        """Handle built-in string methods"""
        args = [self.evaluate_expression(arg) for arg in arguments]
        
        if method_name == "length":
            if len(args) != 0:
                raise ConvoRuntimeError("String.length takes no arguments")
            return len(s)
        
        elif method_name == "upper":
            if len(args) != 0:
                raise ConvoRuntimeError("String.upper takes no arguments")
            return s.upper()
        
        elif method_name == "lower":
            if len(args) != 0:
                raise ConvoRuntimeError("String.lower takes no arguments")
            return s.lower()
        
        elif method_name == "contains":
            if len(args) != 1:
                raise ConvoRuntimeError("String.contains takes exactly 1 argument")
            substring = args[0]
            if not isinstance(substring, str):
                raise ConvoRuntimeError("String.contains: argument must be a string")
            return substring in s
        
        else:
            raise ConvoRuntimeError(f"String has no method '{method_name}'")
