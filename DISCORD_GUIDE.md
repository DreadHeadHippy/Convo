# Discord Bot Development with Convo - Complete Integration Guide

## 🎯 Overview

The Convo programming language now includes **complete groundwork** for Discord bot development. This infrastructure allows developers to create Discord bots using Convo's natural language syntax instead of traditional programming languages.

## 🏗️ What We've Built

### Core Infrastructure

1. **Complete Discord Module** (`convo/modules/discord_bot.py`)
   - Full Discord bot wrapper around discord.py
   - Natural language message condition parsing
   - Event and command management system
   - Proper error handling and bot lifecycle management

2. **Seamless Convo Integration** (`convo/builtins.py`)
   - Discord functions integrated into Convo's built-in function system
   - All Discord capabilities accessible through natural language syntax
   - Type-safe function definitions with comprehensive error handling

3. **Ready-to-Use Examples** (`examples/`)
   - Basic Discord bot template (`discord_bot_basic.convo`)
   - Advanced Discord bot with games and moderation (`discord_bot_advanced.convo`)
   - Complete setup guide in Convo syntax (`discord_setup_guide.convo`)

4. **Comprehensive Testing** (`tests/test_discord_integration.py`)
   - Full test suite for Discord integration
   - Mock testing for Discord.py components
   - Validation of all Convo syntax parsing

### 2. Your First Discord Bot in Convo

```convo
# Simple Discord Bot
Call create_discord_bot with "YOUR_BOT_TOKEN", "!"

# Listen for hello messages
Define greet_user with message:
    Let username be get_user_name(message)
    Return "Hello " + username + "! Welcome to our server!"

Call listen_for_message with "contains \"hello\"", greet_user

# Add a ping command
Define ping_command with ctx:
    Return "Pong! Bot is working!"

Call add_discord_command with "ping", "Check if bot is responsive", ping_command

# Start the bot
Call start_discord_bot
```

### 3. Run Your Bot

```bash
python main.py your_bot_file.convo
```

## Core Discord Functions

### Bot Creation
- `create_discord_bot(token, prefix)` - Creates a bot with your token and command prefix

### Message Listeners
- `listen_for_message(condition, handler)` - Listen for messages matching a condition

### Commands
- `add_discord_command(name, description, handler)` - Add slash commands

### Bot Control
- `start_discord_bot()` - Start the bot (runs indefinitely)

### Message Utilities
- `get_user_name(message)` - Get the username from a message
- `get_message_content(message)` - Get the text content of a message
- `reply_with_text(text)` - Create a simple reply function

## Message Conditions

You can listen for messages based on various conditions:

- `"contains \"text\""` - Message contains the specified text
- `"starts with \"text\""` - Message starts with the text
- `"ends with \"text\""` - Message ends with the text  
- `"equals \"text\""` - Message exactly equals the text

## Advanced Examples

### Moderation Bot
```convo
Call create_discord_bot with "YOUR_TOKEN", ">"

# Auto-moderation
Define check_spam with message:
    Let content be lower(get_message_content(message))
    If contains(content, "spam") then:
        Let user be get_user_name(message)
        Return "⚠️ " + user + ", please keep chat friendly!"

Call listen_for_message with "contains \"spam\"", check_spam

Call start_discord_bot
```

### Interactive Game Bot
```convo
Call create_discord_bot with "YOUR_TOKEN", "!"

# Rock Paper Scissors
Define play_rps with ctx, choice:
    Let choices be ["rock", "paper", "scissors"]
    Let bot_choice be choices[random_int(0, 2)]
    
    Let result be "🎮 You: " + choice + " | Bot: " + bot_choice + "\n"
    
    If choice equals bot_choice then:
        Let result be result + "🤝 It's a tie!"
    Else:
        If choice equals "rock" and bot_choice equals "scissors" then:
            Let result be result + "🎉 You win!"
        Else:
            Let result be result + "🤖 Bot wins!"
    
    Return result

Call add_discord_command with "rps", "Play Rock Paper Scissors", play_rps

Call start_discord_bot
```

### Utility Bot
```convo
Call create_discord_bot with "YOUR_TOKEN", "/"

# Server statistics
Define server_stats with ctx:
    Return "📊 Server Stats:\n• Online Members: Active\n• Total Channels: Many\n• Boost Level: Check settings"

Call add_discord_command with "stats", "Get server statistics", server_stats

# Weather command (mock data)
Define weather with ctx, location:
    Let temp be random_int(15, 35)
    Return "🌤️ Weather in " + location + ": " + to_text(temp) + "°C"

Call add_discord_command with "weather", "Get weather for a location", weather

Call start_discord_bot
```

## Best Practices

### Security
1. **Never share your bot token publicly**
2. **Store tokens in environment variables or config files**
3. **Use specific permissions, avoid Administrator role**
4. **Test bots in private servers first**

### Code Organization
1. **Define handlers before registering them**
2. **Use descriptive function names**
3. **Add comments to explain complex logic**
4. **Group related functionality together**

### Error Handling
```convo
Define safe_command with ctx:
    Try:
        # Your command logic here
        Return "Command executed successfully!"
    Catch error:
        Return "Something went wrong: " + error
```

## Deployment

### Local Development
- Run directly with `python main.py bot.convo`
- Bot will run until stopped with Ctrl+C

### Production Deployment
- Use process managers like PM2 or systemd
- Set up logging and monitoring
- Use environment variables for configuration
- Consider using Docker containers

## Common Patterns

### Welcome Messages
```convo
Define welcome_new_member with message:
    If contains(get_message_content(message), "joined") then:
        Return "🎉 Welcome to our community! Please read the rules."

Call listen_for_message with "contains \"joined\"", welcome_new_member
```

### Auto-responses
```convo
Define auto_help with message:
    If contains(get_message_content(message), "help") then:
        Return "Need help? Try using /commands to see what I can do!"

Call listen_for_message with "contains \"help\"", auto_help
```

### Dynamic Commands
```convo
Define dynamic_info with ctx, topic:
    If topic equals "server" then:
        Return "This is our amazing Discord server!"
    Else:
        If topic equals "bot" then:
            Return "I'm a bot written in Convo language!"
        Else:
            Return "I don't know about: " + topic

Call add_discord_command with "info", "Get information about topics", dynamic_info
```

## Troubleshooting

### Common Issues

1. **Bot doesn't respond**
   - Check if bot token is correct
   - Verify bot has necessary permissions
   - Ensure Message Content Intent is enabled

2. **Commands not working**
   - Check command syntax in Convo code
   - Verify bot has appropriate permissions
   - Test with simple commands first

3. **Permission errors**
   - Review bot permissions in Discord server
   - Check if bot role is positioned correctly
   - Verify specific channel permissions

### Debug Tips
- Add `Say` statements to trace execution
- Test components individually
- Check Discord Developer Portal for bot status
- Use simple examples before complex functionality

## Resources

- **Discord Developer Documentation**: https://discord.com/developers/docs
- **discord.py Documentation**: https://discordpy.readthedocs.io/
- **Convo Language Examples**: See the `examples/` directory
- **Discord Permissions Calculator**: https://discordapi.com/permissions.html

## Support

For issues with:
- **Convo Language**: Check GitHub repository issues
- **Discord Bot Development**: Discord.py community and documentation
- **Discord API**: Discord Developer support channels

---

*Happy bot building with Convo! 🤖*
