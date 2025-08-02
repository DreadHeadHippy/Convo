#!/usr/bin/env python3
"""
Package Structure Validation Tool for Convo Programming Language

This script validates that the Convo package is properly structured and can be
imported correctly. It's useful for:
- Verifying package integrity after changes
- Debugging import issues
- Ensuring distribution readiness
- CI/CD pipeline validation

Usage:
    python test_package_structure.py
"""

import sys
import importlib
import subprocess
from pathlib import Path

def test_package_imports():
    """Test that all package components import correctly"""
    print("🔍 Testing package imports...")
    
    try:
        # Test main package import
        import convo
        print(f"✅ Main package imported - version: {convo.__version__}")
        
        # Test core components
        from convo import Lexer, Parser, Interpreter
        print("✅ Core components imported")
        
        # Test AST nodes
        from convo import ASTNode, Expression, Statement
        print("✅ AST components imported")
        
        # Test specific classes
        from convo.lexer import TokenType
        from convo.ast_nodes import BinaryOp, Literal
        print("✅ Specific classes imported")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_module_execution():
    """Test that the module can be executed"""
    print("\n🔍 Testing module execution...")
    
    try:
        # Test version command
        result = subprocess.run([sys.executable, "-m", "convo", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Module execution works - {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Module execution failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Module execution error: {e}")
        return False

def test_package_metadata():
    """Test package metadata consistency"""
    print("\n🔍 Testing package metadata...")
    
    try:
        import convo
        
        # Check version consistency
        if convo.__version__ == "0.0.1":
            print("✅ Version is correct")
        else:
            print(f"❌ Version mismatch: {convo.__version__}")
            return False
            
        # Check author
        if convo.__author__ == "DreadHeadHippy":
            print("✅ Author is correct")
        else:
            print(f"❌ Author mismatch: {convo.__author__}")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Metadata error: {e}")
        return False

def test_package_structure():
    """Test package file structure"""
    print("\n🔍 Testing package structure...")
    
    project_root = Path(__file__).parent
    
    required_files = [
        "convo/__init__.py",
        "convo/__main__.py", 
        "convo/lexer.py",
        "convo/parser.py",
        "convo/interpreter.py",
        "convo/ast_nodes.py",
        "convo/builtins.py",
        "convo/modules/__init__.py",
        "setup.py",
        "pyproject.toml",
        "MANIFEST.in"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (project_root / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def test_example_execution():
    """Test that a simple example works"""
    print("\n🔍 Testing simple program execution...")
    
    try:
        from convo import Lexer, Parser, Interpreter
        
        # Simple test program
        source = 'Say "Hello from package test!"'
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
        print("✅ Simple program execution works")
        return True
    except Exception as e:
        print(f"❌ Program execution error: {e}")
        return False

def main():
    """Run all package structure tests"""
    print("🚀 Running Convo Package Structure Tests\n")
    
    tests = [
        test_package_structure,
        test_package_imports,
        test_package_metadata,
        test_module_execution,
        test_example_execution
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    print(f"\n📊 Test Results:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print("🎉 All package structure tests passed!")
        return True
    else:
        print("⚠️  Some tests failed - package structure needs attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
