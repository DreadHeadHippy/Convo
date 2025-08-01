# 🗣️ Convo Programming Language

**A natural programming language with conversational syntax**

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/DreadHeadHippy/Convo/ci-tests-new.yml?branch=main&label=tests)](https://github.com/DreadHeadHippy/Convo/actions/workflows/ci-tests-new.yml)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/DreadHeadHippy/Convo)](https://github.com/DreadHeadHippy/Convo/releases)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/DreadHeadHippy/Convo)](https://github.com/DreadHeadHippy/Convo/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/DreadHeadHippy/Convo)](https://github.com/DreadHeadHippy/Convo/network)
[![GitHub issues](https://img.shields.io/github/issues/DreadHeadHippy/Convo)](https://github.com/DreadHeadHippy/Convo/issues)
[![Status](https://img.shields.io/badge/status-production%20ready-success)](examples/)

Convo is a **fully functional programming language** that reads like natural English, making programming more accessible and intuitive. Instead of cryptic symbols and syntax, write code that anyone can understand.

## ✨ Features

- 🗣️ **Natural Language Syntax** - Write code that reads like English
- 🎯 **Easy to Learn** - Perfect for beginners and education
- 🔧 **Full Programming Language** - Variables, functions, control flow, loops
- 🏗️ **Complete Architecture** - Lexer, parser, interpreter, and AST
- 🎮 **Real Applications** - Build games, calculators, and interactive programs
- 🤖 **Discord Bot Support** - Create Discord bots with natural language
    - 🐍 **Python-Based** - Built with Python for easy extension
    - 🧪 **Well Tested** - Comprehensive test suite (35 tests passing)
    - 🚀 **VS Code Support** - Syntax highlighting and debugging
- 💬 **Interactive REPL** - Test code interactively
- 🔄 **Advanced Features** - Nested functions, scoping, error handling

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/DreadHeadHippy/Convo.git
cd Convo
pip install -r requirements.txt
```

### Your First Convo Program

Create a file called `hello.convo`:

```convo
Say "Hello, World!"
Let name be "Alice"
Say "Welcome to Convo, " + name + "!"

Define greet with person:
    Say "Nice to meet you, " + person + "!"

Call greet with name
```

Run it:

```bash
python main.py hello.convo
```

### Interactive Mode

```bash
python -m convo
```

## 🎮 Example Programs

Convo comes with several working example programs:

- **🎯 Game Demo** (`game_demo.convo`) - A complete RPG-style combat game
- **🏦 Banking Demo** (`banking_demo.convo`) - Financial calculations and eligibility checks  
- **📊 Grade Calculator** (`grade_calculator.convo`) - Student grade management system
- **🌤️ Weather App** (`weather_app.convo`) - Weather advisory system
- **🔧 Enhanced Demo** (`enhanced_demo.convo`) - Comprehensive language feature showcase
- **🤖 Discord Bot Basic** (`discord_bot_basic.convo`) - Simple Discord bot with commands
- **🤖 Discord Bot Advanced** (`discord_bot_advanced.convo`) - Complex Discord bot with games and moderation
- **📋 Discord Setup Guide** (`discord_setup_guide.convo`) - Complete Discord bot setup tutorial

Try them:
```bash
python main.py examples/game_demo.convo
python main.py examples/enhanced_demo.convo
python main.py examples/discord_setup_guide.convo
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

### Advanced Features
```convo
Define calculate_grade with score:
    If score greater than 90 then:
        Say "Grade: A"
    Else:
        If score greater than 80 then:
            Say "Grade: B"
        Else:
            Say "Grade: C"

# Nested functions and complex logic
Define weather_system with temp, is_raining:
    If temp greater than 25 and not is_raining then:
        Say "Perfect weather!"
    Else:
        Say "Stay inside!"
```

### Discord Bot Development
```convo
# Create a Discord bot
Call create_discord_bot with "YOUR_BOT_TOKEN", "!"

# Listen for messages
Define handle_hello with message:
    Let username be get_user_name(message)
    Return "Hello " + username + "!"

Call listen_for_message with "contains \"hello\"", handle_hello

# Add commands
Define bot_info with ctx:
    Return "I'm a bot written in Convo!"

Call add_discord_command with "info", "Get bot info", bot_info

# Start the bot
Call start_discord_bot  
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

## 🤖 Discord Bot Development

**Convo is a real programming language** - when you write Discord bots in Convo, you're writing in **pure Convo syntax**, not Python! The Convo interpreter handles all the Python complexity internally.

### Why This Matters
- **You write**: Natural Convo language (`Call create_discord_bot with "TOKEN"`)
- **You DON'T write**: Complex Python (`@bot.command`, `async def`, `await ctx.send()`)
- **Convo handles**: All Discord API complexity, async/await, error handling

### Setup
To get started with Convo:
1. Clone the repository: `git clone https://github.com/DreadHeadHippy/Convo.git`
2. Change into the project directory: `cd Convo`
3. Install dependencies: `pip install -r requirements.txt`
4. Run your first Convo program as shown below.
## 🔒 Security Best Practices

Convo development should follow standard security procedures:

- **Never commit secrets or sensitive information to source control.** Use environment variables or a `.env` file for configuration.
- **Validate all user input** to prevent code injection and abuse.
- **Keep dependencies up to date** and check for vulnerabilities (e.g., with `pip-audit`).
- **Monitor and log application activity** for suspicious behavior.
- **Report vulnerabilities** via the [SECURITY.md](SECURITY.md) file.

### Quick Start
```convo
# Create and configure a Discord bot

# Convo Programming Language

![Test Status](https://github.com/DreadHeadHippy/Convo/actions/workflows/ci-tests-new.yml/badge.svg)

**Current Version:** V0.0.1

---

Call create_discord_bot with "YOUR_BOT_TOKEN", "!"

# Add message listeners
Define greet_user with message:
    Let username be get_user_name(message)
    Return "Hello " + username + "! Welcome to the server!"

Call listen_for_message with "contains \"hello\"", greet_user

# Add custom commands
Define tell_joke with ctx:
    Return "Why did the programmer quit? Because they didn't get arrays! 😄"

Call add_discord_command with "joke", "Get a programming joke", tell_joke

# Start the bot
Call start_discord_bot
```

### Available Discord Functions
- `create_discord_bot(token, prefix)` - Create bot instance
- `listen_for_message(condition, handler)` - Listen for specific messages
- `add_discord_command(name, description, handler)` - Add slash commands
- `start_discord_bot()` - Start the bot
- `get_user_name(message)` - Get username from message
- `get_message_content(message)` - Get message text

### Examples Included
- **Basic Bot** - Simple greetings and commands
- **Advanced Bot** - Games, moderation, polls, and utilities
- **Setup Guide** - Complete tutorial for Discord bot creation

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
- **Discord Bots** - Create interactive Discord bots with conversational syntax
- **Prototyping** - Quick scripting with readable syntax
- **Domain-Specific Languages** - Building readable automation scripts
- **Accessibility** - Programming for users who prefer natural language
- **Game Development** - Simple game logic and interactive experiences

## 🤝 Contributing

We welcome contributions! Please feel free to:

- 🐛 Report bugs
- 💡 Suggest new features
- 🔧 Submit pull requests
- 📖 Improve documentation

## 📜 License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.

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


## 💖 Support

If you enjoy Convo or want to support its development, you can buy me a coffee:

<a href="https://ko-fi.com/dreadheadhippy" target="_blank"><img src="https://cdn.ko-fi.com/cdn/kofi5.png?v=3" height="36" alt="Support on Ko-fi" /></a>

---

Made with ❤️ for accessible programming
