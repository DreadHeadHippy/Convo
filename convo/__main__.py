"""
Main entry point for the Convo programming language interpreter
"""

import sys
import argparse
from pathlib import Path
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter, ConvoRuntimeError

def run_file(file_path: str):
    """Run a Convo program from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            source_code = file.read()
        
        # Tokenize
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        # Parse
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Interpret
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except SyntaxError as e:
        print(f"Syntax Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ConvoRuntimeError as e:
        print(f"Runtime Error: {e.message}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Internal Error: {e}", file=sys.stderr)
        sys.exit(1)

def run_interactive():
    """Run the Convo REPL (Read-Eval-Print Loop)"""
    print("Convo Interactive Shell")
    print("Type 'exit' or 'quit' to leave, 'help' for help.")
    print()
    
    interpreter = Interpreter()
    
    while True:
        try:
            line = input("convo> ").strip()
            
            if line.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            elif line.lower() == 'help':
                print_help()
                continue
            elif not line:
                continue
            
            # Tokenize
            lexer = Lexer(line)
            tokens = lexer.tokenize()
            
            # Parse
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Interpret
            interpreter.interpret(ast)
            
        except KeyboardInterrupt:
            print("\nUse 'exit' or 'quit' to leave.")
        except EOFError:
            print("\nGoodbye!")
            break
        except SyntaxError as e:
            print(f"Syntax Error: {e}")
        except ConvoRuntimeError as e:
            print(f"Runtime Error: {e.message}")
        except Exception as e:
            print(f"Error: {e}")

def print_help():
    """Print help information"""
    print("""
Convo Language Help
==================

Basic Syntax:
  Say "Hello, World!"                    # Print text
  Let name be "Alice"                    # Define variable
  Let age be 25                          # Define number
  Say "Hello, " + name                   # String concatenation

Functions:
  Define greet with name:                # Define function
      Say "Hello, " + name + "!"
  
  Call greet with "World"                # Call function

Control Flow:
  If age greater than 18 then:           # If statement
      Say "Adult"
  Else:
      Say "Minor"
  
  While age less than 30 do:             # While loop
      Let age be age + 1
      Say age

Examples:
  Let x be 10
  Let y be 20
  If x less than y then:
      Say "x is smaller"
  
  Define add with a, b:
      Say a + b
  
  Call add with 5, 3
""")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Convo Programming Language Interpreter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m convo                        # Start interactive shell
  python -m convo script.convo           # Run a Convo file
  python -m convo --help                 # Show this help
        """
    )
    
    parser.add_argument(
        'file',
        nargs='?',
        help='Convo source file to execute'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Convo 1.0.0'
    )
    
    args = parser.parse_args()
    
    if args.file:
        run_file(args.file)
    else:
        run_interactive()

if __name__ == '__main__':
    main()
