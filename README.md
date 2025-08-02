# 🗣️ Convo Programming Language

**A natural programming language with conversational syntax**

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/DreadHeadHippy/Convo/ci-tests-new.yml?branch=main&label=tests)](https://github.com/DreadHeadHippy/Convo/actions/workflows/ci-tests-new.yml)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/DreadHeadHippy/Convo)](https://github.com/DreadHeadHippy/Convo/releases)
[![GitHub stars](https://img.shields.io/github/stars/DreadHeadHippy/Convo)](https://github.com/DreadHeadHippy/Convo/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/DreadHeadHippy/Convo)](https://github.com/DreadHeadHippy/Convo/network/members)
[![GitHub issues](https://img.shields.io/github/issues/DreadHeadHippy/Convo)](https://github.com/DreadHeadHippy/Convo/issues)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)

Convo is a **programming language** that reads like natural English, making programming accessible to everyone. Create real applications, Discord bots, games, and more with intuitive, conversational syntax.

## 🎉 Why Convo?

**Accessibility First:** Programming shouldn't require memorizing cryptic symbols. Convo lets you write code that anyone can read and understand.

**Traditional Python:**
```python
def calculate_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    else:
        return "F"
```

**Convo:**
```convo
Define calculate_grade with score:
    If score greater equal 90 then:
        Return "A"
    Else if score greater equal 80 then:
        Return "B"
    Else:
        Return "F"
```

## ✨ Production Features

### 🏗️ **Complete Language Implementation**
- **Lexical Analysis** - Professional tokenization
- **Parsing** - Full AST generation with error recovery
- **Interpretation** - Robust execution engine
- **Type System** - Dynamic typing with runtime safety

### 🎯 **Real-World Applications**
- **Discord Bots** - 43 built-in functions for bot development
- **Games & Interactive Programs** - Full control flow and state management
- **Data Processing** - Lists, dictionaries, and comprehensions
- **Educational Tools** - Perfect for teaching programming concepts

### 🚀 **Advanced Programming Features**
- **Functions & Closures** - First-class function support
- **Object-Oriented Programming** - Classes and inheritance
- **Control Flow** - If/else, loops (for, while), try/catch
- **Collections** - Lists, dictionaries with built-in methods
- **List Comprehensions** - Functional programming constructs
- **Module System** - Import/export functionality
- **Error Handling** - Comprehensive exception management

### 🔧 **Developer Experience**
- **100% Test Coverage** - 104 passing tests ensuring reliability
- **VS Code Integration** - Syntax highlighting and debugging
- **Interactive REPL** - Live code testing and exploration
- **Comprehensive Documentation** - Examples and guides
- **Production Examples** - Real applications you can run today

## 🚀 Quick Start

### Installation

#### Option 1: Install from GitHub (Recommended)
```bash
# Install Convo directly from GitHub
pip install git+https://github.com/DreadHeadHippy/Convo.git

# Or install with Discord bot support
pip install "git+https://github.com/DreadHeadHippy/Convo.git#egg=convo-lang[discord]"
```

#### Option 2: Install from Source
```bash
git clone https://github.com/DreadHeadHippy/Convo.git
cd Convo
pip install -e .

# Or with Discord support
pip install -e ".[discord]"
```

#### Verify Installation
```bash
# Test the installation
convo --version

# Test Discord module (if installed with discord extras)
python -c "from convo.modules.discord_bot import DiscordModule; print('Discord ready!')"
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

Now that you know the syntax, explore these working example programs:

### 🎯 **Learning Examples**
- **📚 Hello World** (`hello_world.convo`) - Your first Convo program
- **📊 Variables** (`variables.convo`) - Data types and variable assignment
- **🔧 Functions** (`functions.convo`) - Function definitions and calls
- **🔄 Control Flow** (`control_flow.convo`) - If statements, loops, and logic

### 🏗️ **Advanced Features**
- **🎭 Classes & Objects** (`classes_and_objects.convo`) - Object-oriented programming
- **📝 Lists Demo** (`lists_demo.convo`) - List operations and methods
- **📋 Dictionaries Demo** (`dictionaries_demo.convo`) - Dictionary manipulation
- **⚠️ Error Handling** (`error_handling.convo`) - Try/catch and exception management

### 🎮 **Real-World Applications**
- **🎯 Game Demo** (`game_demo.convo`) - Complete RPG-style combat game
- **🏦 Banking Demo** (`banking_demo.convo`) - Financial calculations and eligibility checks  
- **📊 Grade Calculator** (`grade_calculator.convo`) - Student grade management system
- **🌤️ Weather App** (`weather_app.convo`) - Weather advisory system
- **🔧 Enhanced Demo** (`enhanced_demo.convo`) - Comprehensive language feature showcase

### 🤖 **Discord Bot Examples**
- **📋 Discord Setup Guide** (`discord_setup_guide.convo`) - Complete bot setup tutorial
- **🤖 Discord Bot Basic** (`discord_bot_basic.convo`) - Simple bot with commands
- **🤖 Discord Bot Advanced** (`discord_bot_advanced.convo`) - Complex bot with games and moderation
- **🔥 Discord Bot Modern** (`discord_bot_modern.convo`) - Modern slash commands example
- **📖 Discord Slash Commands Guide** (`discord_slash_commands_guide.convo`) - Complete slash commands tutorial
- **🎮 Discord Bot UI Complete** (`discord_bot_ui_complete.convo`) - Interactive buttons, modals, menus
- **📚 Discord UI Complete Guide** (`discord_ui_complete_guide.convo`) - Comprehensive UI components tutorial
- **🛡️ Discord Moderation Bot** (`discord_moderation_bot.convo`) - Full-featured moderation system

Try any example:
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

### Imports and Modules
```convo
# Import modules to extend functionality
Import discord

# Now Discord functions are available
Call create_discord_bot with "YOUR_BOT_TOKEN", "!"
Call start_discord_bot
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

### Error Handling
```convo
Try:
    Let result be risky_operation()
    Say "Success: " + result
Catch error:
    Say "Error occurred: " + error
```

## 🏗️ Project Structure

```
convo/
├── lexer.py          # Tokenizes Convo source code
├── parser.py         # Parses tokens into AST
├── interpreter.py    # Executes the parsed code
├── ast_nodes.py      # Abstract Syntax Tree definitions
├── builtins.py       # Built-in functions and constants
└── __main__.py       # Entry point for the interpreter

examples/             # Example Convo programs
tests/               # Comprehensive test suite (104 tests)
main.py              # Command-line interface
```

## 🧪 Testing & Development

### Running Tests
```bash
python -m pytest tests/ -v
```

### VS Code Integration
- **Run Convo Program**: Execute any `.convo` file
- **Run Convo Interactive**: Start the REPL
- **Run Tests**: Execute the test suite

### Adding New Features
1. Add tokens to `lexer.py`
2. Update parser rules in `parser.py`
3. Add AST nodes in `ast_nodes.py`
4. Implement execution in `interpreter.py`
5. Write tests in `tests/`
6. Add new libraries or modules using the import system

## 🤖 Discord Bot Development

**Convo is a real programming language** - when you write Discord bots in Convo, you're writing in **pure Convo syntax**, not Python! The Convo interpreter handles all the Python complexity internally.

### Why This Matters
- **You write**: Natural Convo language (`Call create_discord_bot with "TOKEN"`)
- **You DON'T write**: Complex Python (`@bot.command`, `async def`, `await ctx.send()`)
- **Convo handles**: All Discord API complexity, async/await, error handling

### Complete Discord Bot Example
```convo
# Import Discord functionality
Import discord

# Create a Discord bot
Call create_discord_bot with "YOUR_BOT_TOKEN", "!"

# Modern slash commands (global - work in all servers)
Define ping_command with interaction:
    Let user be get_interaction_user(interaction)
    Return "🏓 Pong! Hello " + user + "!"

Call create_global_slash_command with "ping", "Check if bot is alive", ping_command

Define info_command with interaction:
    Let guild be get_interaction_guild(interaction)
    Return "🤖 I'm a bot written in Convo running in " + guild + "!"

Call create_global_slash_command with "info", "Get bot info", info_command

# Server-specific slash command (replace with your guild ID)
Define admin_command with interaction:
    Let user be get_interaction_user(interaction)
    Return "🔧 Admin tools accessed by " + user

Call create_guild_slash_command with "admin", "Admin tools", admin_command, 123456789

# Sync commands with Discord
Call sync_global_commands

# Legacy message listener for backward compatibility
Define handle_hello with message:
    Let username be get_user_name(message)
    Return "Hello " + username + "! Try using /ping instead!"

Call listen_for_message with "contains \"hello\"", handle_hello

# Start the bot
Call start_discord_bot
```

### Available Discord Functions (43 total)
**Basic Functions:**
- `create_discord_bot(token, prefix)` - Create bot instance
- `listen_for_message(condition, handler)` - Listen for specific messages
- `add_discord_command(name, description, handler)` - Add traditional prefix commands
- `start_discord_bot()` - Start the bot
- `get_user_name(message)` - Get username from message
- `get_message_content(message)` - Get message text

**Modern Slash Commands:**
- `create_global_slash_command(name, description, handler)` - Global slash commands (all servers)
- `create_guild_slash_command(name, description, handler, guild_id)` - Server-specific commands
- `create_slash_command(name, description, handler)` - Create global slash command (legacy)
- `sync_global_commands()` - Sync global commands with Discord
- `sync_guild_commands(guild_id)` - Sync server-specific commands
- `sync_discord_commands(guild_id?)` - Sync commands (global or guild)

**Interaction Helpers:**
- `get_interaction_user(interaction)` - Get user from slash command
- `get_interaction_guild(interaction)` - Get server from slash command
- `get_interaction_channel(interaction)` - Get channel from slash command

**🎯 Interactive UI Components:**
- `create_button(label, style, custom_id, emoji, disabled)` - Interactive buttons
- `create_select_menu(placeholder, options, custom_id, min_vals, max_vals)` - Dropdown menus
- `create_modal_input(label, placeholder, required, min_len, max_len, style)` - Form inputs
- `create_modal(title, custom_id, inputs)` - Modal dialogs (forms)
- `create_view(timeout)` - Component container with timeout
- `send_message_with_components(channel, content, embed, view)` - Send messages with UI
- `create_embed_with_components(title, desc, color, buttons, menu)` - Rich embeds with UI
- `show_modal(interaction, modal)` - Display modal dialog

**🖱️ Context Menus & Advanced:**
- `create_context_menu_user(name)` - Right-click user commands
- `create_context_menu_message(name)` - Right-click message commands
- `create_autocomplete_choices(choices)` - Static autocomplete options
- `create_dynamic_autocomplete(function)` - Dynamic autocomplete options

**Advanced Functions:**
- `send_embed()` - Rich embedded messages
- `add_reaction()` - React to messages  
- `send_file()` - File uploads/downloads
- `join_voice_channel()` - Voice chat integration
- `play_audio()` - Music/audio playback

**Error Handling & Utilities:**
- `handle_discord_error()` - Error management
- `validate_discord_config()` - Configuration validation
- `get_discord_help()` - Built-in help system
- `debug_discord_environment()` - Debugging tools

### Bot Types You Can Build
- **🛡️ Moderation Bots** - Auto-moderation, warnings, bans, raid protection with interactive appeals
- **🎮 Game Bots** - Interactive games with buttons, trivia with select menus, RPG systems with modals
- **🔧 Utility Bots** - Server management with UI forms, polls with buttons, reminders with interactive setup
- **🎵 Music Bots** - Audio playback controls via buttons, playlist management with dropdowns
- **📊 Analytics Bots** - Interactive dashboards with buttons, user surveys with modal forms
- **💼 Business Bots** - Support ticket systems with modal forms, application processes with step-by-step UI
- **🎓 Educational Bots** - Interactive quizzes with buttons, learning paths with select menus, progress tracking

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

## 💖 Support

If you enjoy Convo or want to support its development, you can buy me a coffee:

<a href="https://ko-fi.com/dreadheadhippy" target="_blank"><img src="https://cdn.ko-fi.com/cdn/kofi5.png?v=3" height="36" alt="Support on Ko-fi" /></a>

---

Made with ❤️ for accessible programming
