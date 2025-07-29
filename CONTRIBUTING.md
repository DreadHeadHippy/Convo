# Contributing to Convo Programming Language

Thank you for your interest in contributing to Convo! This document provides guidelines for contributing to the project.

## 🎯 Ways to Contribute

- **Report bugs** - Help us find and fix issues
- **Suggest features** - Propose new language features or improvements
- **Submit code** - Fix bugs, implement features, or improve documentation
- **Write examples** - Create educational Convo programs
- **Improve documentation** - Help make Convo more accessible

## 🚀 Getting Started

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Convo.git
   cd Convo
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pytest
   ```
4. Run tests to ensure everything works:
   ```bash
   python -m pytest tests/ -v
   ```

### Project Structure

- `convo/` - Core language implementation
  - `lexer.py` - Tokenizes Convo source code
  - `parser.py` - Parses tokens into AST
  - `interpreter.py` - Executes the AST
  - `ast_nodes.py` - AST node definitions
  - `builtins.py` - Built-in functions
- `examples/` - Example Convo programs
- `tests/` - Test suite
- `main.py` - CLI entry point

## 📋 Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use type hints where possible
- Write descriptive docstrings
- Keep functions focused and small
- Use meaningful variable names

### Language Design Principles

1. **Natural Language First** - Syntax should read like English
2. **Beginner Friendly** - Easy to learn and understand
3. **Consistent** - Similar concepts use similar syntax
4. **Extensible** - Easy to add new features
5. **Error Friendly** - Clear, helpful error messages

### Testing

- Write tests for all new features
- Ensure existing tests pass
- Test both positive and negative cases
- Include integration tests with example programs

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_parser.py -v

# Test example programs
python -m convo examples/hello_world.convo
```

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce** the problem
3. **Expected behavior** vs actual behavior
4. **Convo code** that demonstrates the issue
5. **Error messages** or unexpected output
6. **Environment details** (OS, Python version)

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md).

## 💡 Suggesting Features

For feature requests:

1. **Check existing issues** to avoid duplicates
2. **Describe the problem** the feature would solve
3. **Propose specific syntax** if applicable
4. **Provide use cases** and examples
5. **Consider backwards compatibility**

Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md).

## 🔧 Language Features

When proposing new language features:

1. **Follow natural language principles**
2. **Provide concrete examples** of usage
3. **Consider implementation complexity**
4. **Think about error handling**
5. **Ensure consistency** with existing syntax

Use the [language feature template](.github/ISSUE_TEMPLATE/language_feature.md).

## 📝 Pull Request Process

1. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the guidelines above

3. **Write or update tests** for your changes

4. **Update documentation** if needed

5. **Run the test suite**:
   ```bash
   python -m pytest tests/ -v
   ```

6. **Commit your changes** with clear messages:
   ```bash
   git commit -m "Add feature: natural language loops"
   ```

7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request** using the template

### Pull Request Guidelines

- **Clear title** describing the change
- **Detailed description** of what was changed and why
- **Link related issues** using keywords (fixes #123)
- **Include examples** if changing language behavior
- **Update documentation** as needed

## 🏷️ Commit Message Format

Use clear, descriptive commit messages:

```
Add feature: while loops with natural syntax

- Implement WHILE token in lexer
- Add WhileStatement AST node
- Update parser to handle while loops
- Add interpreter support for while loops
- Include tests and examples
```

## 📚 Documentation

When updating documentation:

- Keep it beginner-friendly
- Include code examples
- Update README if adding major features
- Ensure examples work correctly
- Check for typos and clarity

## 🎉 Recognition

Contributors will be:

- Listed in the project contributors
- Credited in release notes for significant contributions
- Mentioned in documentation for major features

## 📞 Getting Help

If you need help:

- Check existing [issues](https://github.com/DreadHeadHippy/Convo/issues)
- Create a new issue with your question
- Review the [README](README.md) and examples

## 📄 License

By contributing to Convo, you agree that your contributions will be licensed under the Apache 2.0 License.

Thank you for helping make Convo better! 🚀
