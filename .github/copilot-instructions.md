<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Convo Programming Language Development

This project is developing a new programming language called "Convo" with natural language-like syntax.

## Project Structure

- `convo/` - Core language implementation
  - `lexer.py` - Tokenizes Convo source code into tokens
  - `parser.py` - Parses tokens into Abstract Syntax Tree (AST)
  - `interpreter.py` - Executes the AST
  - `ast_nodes.py` - Defines AST node classes
  - `__main__.py` - Entry point for running Convo programs

- `examples/` - Example Convo programs
- `tests/` - Test suite for the language implementation

## Convo Language Syntax

Convo uses natural language-like syntax:

```convo
Say "Hello, World!"                    # Print statement
Let name be "Alice"                    # Variable assignment
Define greet with name:                # Function definition
    Say "Hello, " + name + "!"
Call greet with "World"                # Function call
If age greater than 18 then:           # Conditional
    Say "Adult"
```

## Development Guidelines

1. Keep the natural language syntax intuitive and readable
2. Maintain consistent error handling and reporting
3. Ensure proper indentation handling for block structures
4. Write comprehensive tests for new features
5. Document language features in the README

## Code Style

- Use Python type hints where possible
- Follow PEP 8 conventions
- Write descriptive docstrings for classes and methods
- Use meaningful variable and function names
