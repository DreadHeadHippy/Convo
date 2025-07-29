# 🗣️ Convo Programming Language

**A natural programming language with conversational syntax**

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](tests/)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Convo is a programming language that reads like natural English, making programming more accessible and intuitive. Instead of cryptic symbols and syntax, write code that anyone can understand.

## ✨ Features

- 🗣️ **Natural Language Syntax** - Write code that reads like English
- 🎯 **Easy to Learn** - Perfect for beginners and education
- 🔧 **Full Programming Language** - Variables, functions, control flow
- 🐍 **Python-Based** - Built with Python for easy extension
- 🧪 **Well Tested** - Comprehensive test suite
- 🚀 **VS Code Support** - Syntax highlighting and debugging

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/yourusername/convo-language.git
cd convo-language
pip install -r requirements.txt
```

### Your First Convo Program

Create a file called `hello.convo`:

```convo
Say "Hello, World!"
Let name be "Alice"
Say "Welcome to Convo, " + name + "!"
```

Run it:

```bash
python main.py hello.convo
```

### Interactive Mode

```bash
python -m convo
```

## 📝 Language Syntax

### Variables
```convo
Let name be "Alice"
Let age be 25
Let is_student be true
```

### Arithmetic
```convo
Let result be 5 + 3 * 2
Let comparison be age greater than 18
```

### Functions
```convo
Define greet with name:
    Say "Hello, " + name + "!"
    Say "Nice to meet you!"

Call greet with "World"
```

### Control Flow
```convo
If age greater than 18 then:
    Say "You're an adult!"
Else:
    Say "You're a minor"

While count less than 5 do:
    Say "Count: " + count
    Let count be count + 1
```

## 🏗️ Project Structure

```
convo/
├── lexer.py          # Tokenizes Convo source code
├── parser.py         # Parses tokens into AST
├── interpreter.py    # Executes the parsed code
├── ast_nodes.py      # Abstract Syntax Tree definitions
└── __main__.py       # Entry point for the interpreter

examples/             # Example Convo programs
tests/               # Comprehensive test suite
```

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

## 🛠️ Development

### VS Code Tasks

- **Run Convo Program**: Execute any `.convo` file
- **Run Convo Interactive**: Start the REPL
- **Run Tests**: Execute the test suite

### Adding New Features

1. Add tokens to `lexer.py`
2. Update parser rules in `parser.py`
3. Add AST nodes in `ast_nodes.py`
4. Implement execution in `interpreter.py`
5. Write tests in `tests/`

## 🎯 Use Cases

- **Education** - Teaching programming concepts with natural language
- **Prototyping** - Quick scripting with readable syntax
- **Domain-Specific Languages** - Building readable automation scripts
- **Accessibility** - Programming for users who prefer natural language

## 🤝 Contributing

We welcome contributions! Please feel free to:

- 🐛 Report bugs
- 💡 Suggest new features
- 🔧 Submit pull requests
- 📖 Improve documentation

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🎉 Why Convo?

Most programming languages prioritize brevity and efficiency for experienced developers. Convo prioritizes **readability** and **accessibility**, making programming concepts clear to everyone.

**Traditional:**
```python
if user.age >= 18 and user.has_license:
    print("Can drive")
```

**Convo:**
```convo
If age greater than 18 and has_license equals true then:
    Say "Can drive"
```

---

Made with ❤️ for accessible programming
