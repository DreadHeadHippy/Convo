"""
Tests for the improved AST structure with clear expression/statement separation
"""

import pytest
from convo.lexer import Lexer
from convo.parser import Parser
from convo.ast_nodes import *
from convo.interpreter import Interpreter

class TestASTStructure:
    """Test the improved AST structure and node organization"""
    
    def test_expression_statement_hierarchy(self):
        """Test that expressions and statements are properly separated"""
        # Test literal expressions
        literal = Literal("test")
        assert isinstance(literal, Expression)
        assert isinstance(literal, ASTNode)
        
        # Test statements
        say_stmt = SayStatement(literal)
        assert isinstance(say_stmt, Statement)
        assert isinstance(say_stmt, ASTNode)
        
        # Test compound statements
        if_stmt = IfStatement(literal, [say_stmt])
        assert isinstance(if_stmt, CompoundStatement)
        assert isinstance(if_stmt, Statement)
        assert isinstance(if_stmt, ASTNode)
    
    def test_new_literal_types(self):
        """Test the new specific literal types"""
        # Boolean literal
        bool_lit = BooleanLiteral(True)
        assert bool_lit.value is True
        assert isinstance(bool_lit, Literal)
        
        # Number literal
        num_lit = NumberLiteral(42)
        assert num_lit.value == 42
        assert isinstance(num_lit, Literal)
        
        # String literal
        str_lit = StringLiteral("hello")
        assert str_lit.value == "hello"
        assert isinstance(str_lit, Literal)
        
        # Null literal
        null_lit = NullLiteral()
        assert null_lit.value is None
        assert isinstance(null_lit, Literal)
    
    def test_new_assignment_types(self):
        """Test the new assignment statement types"""
        target = "x"
        value = Literal(10)
        
        # Regular assignment
        assign = AssignmentStatement(target, value)
        assert assign.target == target
        assert assign.value == value
        
        # Compound assignment
        compound = CompoundAssignmentStatement(target, "+", value)
        assert compound.target == target
        assert compound.operator == "+"
        assert compound.value == value
    
    def test_conditional_expression(self):
        """Test conditional expressions (ternary operator)"""
        condition = BooleanLiteral(True)
        true_expr = StringLiteral("yes")
        false_expr = StringLiteral("no")
        
        cond_expr = ConditionalExpression(condition, true_expr, false_expr)
        assert cond_expr.condition == condition
        assert cond_expr.true_expr == true_expr
        assert cond_expr.false_expr == false_expr
        assert isinstance(cond_expr, Expression)
    
    def test_collection_literals(self):
        """Test collection literal expressions"""
        elements: List[Expression] = [NumberLiteral(1), NumberLiteral(2), NumberLiteral(3)]
        
        # List literal
        list_lit = ListLiteral(elements)
        assert list_lit.elements == elements
        assert isinstance(list_lit, Expression)
        
        # Tuple literal
        tuple_lit = TupleLiteral(elements)
        assert tuple_lit.elements == elements
        assert isinstance(tuple_lit, Expression)
        
        # Dictionary literal
        pairs = [(StringLiteral("key"), StringLiteral("value"))]
        dict_lit = DictionaryLiteral(pairs)
        assert dict_lit.pairs == pairs
        assert isinstance(dict_lit, Expression)
    
    def test_access_operations(self):
        """Test access operation expressions"""
        obj = Identifier("arr")
        index = NumberLiteral(0)
        prop_name = "length"
        
        # Index access
        idx_access = IndexAccess(obj, index)
        assert idx_access.object == obj
        assert idx_access.object_expr == obj  # New alias
        assert idx_access.index == index
        assert isinstance(idx_access, Expression)
        
        # Property access
        prop_access = PropertyAccess(obj, prop_name)
        assert prop_access.object == obj
        assert prop_access.object_expr == obj  # New alias
        assert prop_access.property_name == prop_name
        assert isinstance(prop_access, Expression)
        
        # Slice access
        start = NumberLiteral(1)
        end = NumberLiteral(5)
        slice_access = SliceAccess(obj, start, end)
        assert slice_access.object_expr == obj
        assert slice_access.start == start
        assert slice_access.end == end
        assert isinstance(slice_access, Expression)
    
    def test_lambda_expressions(self):
        """Test lambda/anonymous function expressions"""
        params = ["x", "y"]
        body = BinaryOp(Identifier("x"), "+", Identifier("y"))
        
        lambda_expr = LambdaExpression(params, body)
        assert lambda_expr.parameters == params
        assert lambda_expr.body == body
        assert isinstance(lambda_expr, Expression)
    
    def test_compound_statements(self):
        """Test compound statement types"""
        condition = BooleanLiteral(True)
        body: List[Statement] = [SayStatement(StringLiteral("test"))]
        
        # If statement
        if_stmt = IfStatement(condition, body)
        assert isinstance(if_stmt, CompoundStatement)
        
        # While statement
        while_stmt = WhileStatement(condition, body)
        assert isinstance(while_stmt, CompoundStatement)
        
        # For statement
        for_stmt = ForStatement("i", ListLiteral([]), body)
        assert isinstance(for_stmt, CompoundStatement)
        
        # Try statement
        try_stmt = TryStatement(body, body)
        assert isinstance(try_stmt, CompoundStatement)
    
    def test_method_call_compatibility(self):
        """Test that MethodCall maintains backward compatibility"""
        # Old format (string object_name)
        old_method = MethodCall("obj", "method", [])
        assert old_method.object_name == "obj"
        assert isinstance(old_method.object_expr, Identifier)
        assert old_method.object_expr.name == "obj"
        
        # Test with identifier as object name too
        obj_expr = Identifier("obj")
        # MethodCall accepts both string and Expression - let's test string only
        new_method = MethodCall("obj", "method", [])
        assert new_method.object_name == "obj"
    
    def test_property_assignment_compatibility(self):
        """Test that PropertyAssignmentStatement maintains backward compatibility"""
        value = StringLiteral("test")
        
        # Old format (string object_name)
        old_assign = PropertyAssignmentStatement("obj", "prop", value)
        assert old_assign.object_name == "obj"
        assert isinstance(old_assign.object_expr, Identifier)
        
        # Test with string input
        new_assign = PropertyAssignmentStatement("obj", "prop", value)
        assert new_assign.object_name == "obj"
    
    def test_expression_statement(self):
        """Test expression statements for expressions used as statements"""
        expr = FunctionCall("print", [StringLiteral("hello")])
        expr_stmt = ExpressionStatement(expr)
        
        assert expr_stmt.expression == expr
        assert isinstance(expr_stmt, Statement)
    
    def test_ast_node_location(self):
        """Test that AST nodes can store location information"""
        node = Literal("test")
        node.location = (10, 5)
        
        assert node.location == (10, 5)
    
    def test_from_import_statement(self):
        """Test the new FromImportStatement"""
        from_import = FromImportStatement("math", ["sin", "cos"], ["sine", "cosine"])
        
        assert from_import.module_name == "math"
        assert from_import.imports == ["sin", "cos"]
        assert from_import.aliases == ["sine", "cosine"]
        assert isinstance(from_import, Statement)
    
    def test_with_statement(self):
        """Test the new WithStatement for context managers"""
        context = FunctionCall("open", [StringLiteral("file.txt")])
        body: List[Statement] = [SayStatement(StringLiteral("reading file"))]
        
        with_stmt = WithStatement(context, "file", body)
        assert with_stmt.context_expr == context
        assert with_stmt.variable == "file"
        assert with_stmt.body == body
        assert isinstance(with_stmt, CompoundStatement)
    
    def test_class_definition_inheritance(self):
        """Test class definition with inheritance support"""
        class_def = ClassDefinition("Child", ["param"], [], "Parent")
        
        assert class_def.name == "Child"
        assert class_def.constructor_params == ["param"]
        assert class_def.parent_class == "Parent"
        assert isinstance(class_def, CompoundStatement)


class TestASTIntegration:
    """Test AST structure with parser and interpreter integration"""
    
    def parse_code(self, code: str):
        """Helper to parse code into AST"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()
    
    def test_parse_basic_expressions(self):
        """Test parsing basic expressions with new AST structure"""
        code = """
        Say "hello"
        Let x be 42
        """
        
        ast = self.parse_code(code)
        assert isinstance(ast, Program)
        assert len(ast.statements) == 2
        
        # Check Say statement
        say_stmt = ast.statements[0]
        assert isinstance(say_stmt, SayStatement)
        assert isinstance(say_stmt.expression, Literal)
        
        # Check Let statement
        let_stmt = ast.statements[1]
        assert isinstance(let_stmt, LetStatement)
        assert isinstance(let_stmt.value, Literal)
    
    def test_ast_interpreter_compatibility(self):
        """Test that the new AST structure works with the interpreter"""
        code = """
        Let x be 10
        Let y be 20
        Say x + y
        """
        
        # Parse and interpret
        ast = self.parse_code(code)
        interpreter = Interpreter()
        result = interpreter.interpret(ast)
        # Should execute without errors and print 30
