"""
Test Phase 1 Step 3 parser improvements
"""

import unittest
from convo.lexer import Lexer
from convo.parser import Parser
from convo.ast_nodes import *

class TestPhase1Step3Improvements(unittest.TestCase):
    """Test the Phase 1 Step 3 parser improvements"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.maxDiff = None
    
    def parse_code(self, code: str):
        """Helper to parse code and return AST"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()
    
    def test_enhanced_from_import_parsing(self):
        """Test FROM import syntax with aliases"""
        code = "From discord import client, message as msg"
        
        ast = self.parse_code(code)
        self.assertEqual(len(ast.statements), 1)
        
        import_stmt = ast.statements[0]
        self.assertIsInstance(import_stmt, FromImportStatement)
        self.assertEqual(import_stmt.module_name, "discord")
        self.assertEqual(import_stmt.imports, ["client", "message"])
        self.assertEqual(import_stmt.aliases, [None, "msg"])
    
    def test_enhanced_literal_parsing(self):
        """Test improved literal type parsing"""
        code = '''
        Let str_lit be "Enhanced string"
        Let num_int be 42
        Let num_float be 3.14
        Let bool_true be true
        Let bool_false be false
        Let null_val be null
        '''
        
        ast = self.parse_code(code)
        
        # Check string literal
        string_assignment = ast.statements[0]
        self.assertIsInstance(string_assignment, LetStatement)
        self.assertIsInstance(string_assignment.value, StringLiteral)
        self.assertEqual(string_assignment.value.value, "Enhanced string")
        
        # Check integer literal
        int_assignment = ast.statements[1]
        self.assertIsInstance(int_assignment, LetStatement)
        self.assertIsInstance(int_assignment.value, NumberLiteral)
        self.assertEqual(int_assignment.value.value, 42)
        
        # Check float literal
        float_assignment = ast.statements[2]
        self.assertIsInstance(float_assignment, LetStatement)
        self.assertIsInstance(float_assignment.value, NumberLiteral)
        self.assertEqual(float_assignment.value.value, 3.14)
        
        # Check boolean literals
        bool_true_assignment = ast.statements[3]
        self.assertIsInstance(bool_true_assignment, LetStatement)
        self.assertIsInstance(bool_true_assignment.value, BooleanLiteral)
        self.assertEqual(bool_true_assignment.value.value, True)
        
        bool_false_assignment = ast.statements[4]
        self.assertIsInstance(bool_false_assignment, LetStatement)
        self.assertIsInstance(bool_false_assignment.value, BooleanLiteral)
        self.assertEqual(bool_false_assignment.value.value, False)
        
        # Check null literal
        null_assignment = ast.statements[5]
        self.assertIsInstance(null_assignment, LetStatement)
        self.assertIsInstance(null_assignment.value, NullLiteral)
        self.assertIsNone(null_assignment.value.value)
    
    def test_enhanced_collection_literals(self):
        """Test list and dictionary literal parsing"""
        code = '''
        Let my_list be [1, 2.5, true, "text"]
        Let my_dict be {"key1": "value1", "key2": 42, "key3": true}
        '''
        
        ast = self.parse_code(code)
        
        # Check list literal
        list_assignment = ast.statements[0]
        self.assertIsInstance(list_assignment.value, ListLiteral)
        list_elements = list_assignment.value.elements
        
        self.assertEqual(len(list_elements), 4)
        self.assertIsInstance(list_elements[0], NumberLiteral)
        self.assertEqual(list_elements[0].value, 1)
        self.assertIsInstance(list_elements[1], NumberLiteral)
        self.assertEqual(list_elements[1].value, 2.5)
        self.assertIsInstance(list_elements[2], BooleanLiteral)
        self.assertEqual(list_elements[2].value, True)
        self.assertIsInstance(list_elements[3], StringLiteral)
        self.assertEqual(list_elements[3].value, "text")
        
        # Check dictionary literal
        dict_assignment = ast.statements[1]
        self.assertIsInstance(dict_assignment.value, DictionaryLiteral)
        dict_pairs = dict_assignment.value.pairs
        
        self.assertEqual(len(dict_pairs), 3)
        # First pair: "key1": "value1"
        key1, value1 = dict_pairs[0]
        self.assertIsInstance(key1, StringLiteral)
        self.assertEqual(key1.value, "key1")
        self.assertIsInstance(value1, StringLiteral)
        self.assertEqual(value1.value, "value1")
        
        # Second pair: "key2": 42
        key2, value2 = dict_pairs[1]
        self.assertIsInstance(key2, StringLiteral)
        self.assertEqual(key2.value, "key2")
        self.assertIsInstance(value2, NumberLiteral)
        self.assertEqual(value2.value, 42)
        
        # Third pair: "key3": true
        key3, value3 = dict_pairs[2]
        self.assertIsInstance(key3, StringLiteral)
        self.assertEqual(key3.value, "key3")
        self.assertIsInstance(value3, BooleanLiteral)
        self.assertEqual(value3.value, True)
    
    def test_enhanced_expression_parsing(self):
        """Test improved expression parsing"""
        code = '''
        Let complex_expr be (42 + 3.14) * 2
        Let dict_access be my_dict["key"]
        '''
        
        ast = self.parse_code(code)
        
        # Check complex expression with parentheses
        complex_assignment = ast.statements[0]
        self.assertIsInstance(complex_assignment, LetStatement)
        self.assertIsInstance(complex_assignment.value, BinaryOp)
        
        # Left operand should be (42 + 3.14)
        left_operand = complex_assignment.value.left
        self.assertIsInstance(left_operand, BinaryOp)
        self.assertEqual(left_operand.operator, "+")
        self.assertIsInstance(left_operand.left, NumberLiteral)
        self.assertEqual(left_operand.left.value, 42)
        self.assertIsInstance(left_operand.right, NumberLiteral)
        self.assertEqual(left_operand.right.value, 3.14)
        
        # Operator should be *
        self.assertEqual(complex_assignment.value.operator, "*")
        
        # Right operand should be 2
        right_operand = complex_assignment.value.right
        self.assertIsInstance(right_operand, NumberLiteral)
        self.assertEqual(right_operand.value, 2)
        
        # Check dictionary access
        dict_access_assignment = ast.statements[1]
        self.assertIsInstance(dict_access_assignment, LetStatement)
        self.assertIsInstance(dict_access_assignment.value, IndexAccess)
        self.assertIsInstance(dict_access_assignment.value.object, Identifier)
        self.assertEqual(dict_access_assignment.value.object.name, "my_dict")
        self.assertIsInstance(dict_access_assignment.value.index, StringLiteral)
        self.assertEqual(dict_access_assignment.value.index.value, "key")

if __name__ == '__main__':
    unittest.main()
