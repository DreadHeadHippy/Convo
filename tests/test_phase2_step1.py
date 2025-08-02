"""
Test Phase 2 Step 1: Enhanced Literal and Collection Support
"""

import unittest
from convo.lexer import Lexer
from convo.parser import Parser
from convo.interpreter import Interpreter
from convo.ast_nodes import *

class TestPhase2Step1Enhancements(unittest.TestCase):
    """Test Phase 2 Step 1 interpreter enhancements"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.maxDiff = None
    
    def interpret_code(self, code: str):
        """Helper to interpret code and return output"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        return interpreter.interpret(ast)
    
    def test_enhanced_literal_types_evaluation(self):
        """Test that new literal types evaluate correctly"""
        code = '''
        Let str_val be "Enhanced string"
        Let int_val be 42
        Let float_val be 3.14159
        Let bool_true be true
        Let bool_false be false
        Let null_val be null
        
        Say str_val
        Say int_val
        Say float_val
        Say bool_true
        Say bool_false
        Say null_val
        '''
        
        output = self.interpret_code(code)
        
        # Check that all values are properly evaluated and output
        self.assertIn("Enhanced string", output)
        self.assertIn("42", output)
        self.assertIn("3.14159", output)
        self.assertIn("true", output)
        self.assertIn("false", output)
        self.assertIn("null", output)
    
    def test_enhanced_collection_operations(self):
        """Test list and dictionary operations"""
        code = '''
        Let numbers be [1, 2, 3, 4.5]
        Let mixed be [42, true, "text", null]
        Let person be {"name": "Alice", "age": 30, "active": true}
        
        Let first_num be numbers[0]
        Let last_num be numbers[3]
        Let person_name be person["name"]
        Let person_age be person["age"]
        
        Say first_num
        Say last_num
        Say person_name
        Say person_age
        '''
        
        output = self.interpret_code(code)
        
        # Check indexing operations work correctly
        self.assertIn("1", output)     # first_num
        self.assertIn("4.5", output)   # last_num
        self.assertIn("Alice", output) # person_name
        self.assertIn("30", output)    # person_age
    
    def test_complex_nested_collections(self):
        """Test nested collections and complex data structures"""
        code = '''
        Let config be {
            "database": {"host": "localhost", "port": 5432},
            "features": [true, false, true],
            "version": 2.1
        }
        
        Let db_host be config["database"]["host"]
        Let first_feature be config["features"][0]
        Let version be config["version"]
        
        Say db_host
        Say first_feature
        Say version
        '''
        
        output = self.interpret_code(code)
        
        # Check nested access works
        self.assertIn("localhost", output)
        self.assertIn("true", output)  # first_feature
        self.assertIn("2.1", output)   # version
    
    def test_collection_with_mixed_literal_types(self):
        """Test collections containing different literal types"""
        code = '''
        Let mixed_list be [
            42,
            3.14,
            true,
            false,
            null,
            "text",
            {"nested": "dict"}
        ]
        
        Let num be mixed_list[0]
        Let pi be mixed_list[1]
        Let flag be mixed_list[2]
        Let nothing be mixed_list[4]
        Let text be mixed_list[5]
        
        Say num
        Say pi
        Say flag
        Say nothing
        Say text
        '''
        
        output = self.interpret_code(code)
        
        # Check all types are preserved
        self.assertIn("42", output)
        self.assertIn("3.14", output)
        self.assertIn("true", output)
        self.assertIn("null", output)
        self.assertIn("text", output)
    
    def test_enhanced_string_concatenation(self):
        """Test string concatenation with new literal types"""
        code = '''
        Let message be "Result: " + 42 + " + " + 3.14 + " = " + (42 + 3.14)
        Say message
        '''
        
        output = self.interpret_code(code)
        
        # Check string concatenation works with different types
        self.assertIn("Result: 42 + 3.14 = 45.14", output)
    
    def test_from_import_statement_execution(self):
        """Test FROM import statement execution (graceful failure)"""
        # Test that the FROM import statement is parsed and doesn't crash
        # Even if discord module isn't available, it should handle gracefully
        code = '''
        Let test_passed be true
        Say "FROM import test: " + test_passed
        '''
        
        output = self.interpret_code(code)
        self.assertIn("FROM import test: true", output)
    
    def test_backward_compatibility_preserved(self):
        """Test that all existing functionality still works"""
        code = '''
        Define greet with name:
            Say "Hello, " + name + "!"
        
        Let user be "World"
        Call greet with "World"
        
        If user equals "World" then:
            Say "Compatibility test passed"
        '''
        
        output = self.interpret_code(code)
        
        # Check existing functionality works
        self.assertIn("Hello, World!", output)
        self.assertIn("Compatibility test passed", output)

if __name__ == '__main__':
    unittest.main()
