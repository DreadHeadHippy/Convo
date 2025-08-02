"""
Discord Bot Module for Convo Programming Language

This module provides Discord bot functionality with natural language syntax.
Allows users to create Discord bots using Convo's intuitive syntax.

Example Convo Discord Bot:
```convo
Import discord

Create bot with token "your_bot_token"

Listen for message events:
    If message contains "hello" then:
        Reply with "Hello there!"

Listen for command "ping":
    Reply with "Pong!"

Start bot
```
"""

import asyncio
import re
import sys
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass

# Check if discord.py is available
try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    discord = None
    commands = None
    DISCORD_AVAILABLE = False

@dataclass
class ConvoDiscordEvent:
    """Represents a Discord event handler in Convo"""
    event_type: str
    condition: Optional[str]
    action: Callable
    parameters: Dict[str, Any]

@dataclass
class ConvoDiscordCommand:
    """Represents a Discord command in Convo"""
    name: str
    description: str
    action: Callable
    parameters: List[str]

class ConvoDiscordBot:
    """Discord bot implementation for Convo language"""
    
    def __init__(self, token: str, prefix: str = "!"):
        if not DISCORD_AVAILABLE:
            raise RuntimeError("discord.py library not installed. Run: pip install discord.py")
        
        self.token = token
        self.prefix = prefix
        
        # Create intents more safely - avoid hanging
        try:
            # Type check to satisfy linter
            if discord is None or commands is None:
                raise RuntimeError("Discord library not available")
                
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
            intents.presences = True
            
            self.bot = commands.Bot(command_prefix=prefix, intents=intents)
        except Exception as e:
            # Fallback to minimal intents if all fail
            print(f"Warning: Using minimal intents due to error: {e}")
            if discord is None or commands is None:
                raise RuntimeError("Discord library not available")
            intents = discord.Intents.default()
            intents.message_content = True
            self.bot = commands.Bot(command_prefix=prefix, intents=intents)
        
        self.events: List[ConvoDiscordEvent] = []
        self.commands: List[ConvoDiscordCommand] = []
        self.is_running = False
        
        # Setup default events
        self._setup_default_events()
    
    def _setup_default_events(self):
        """Setup default Discord events"""
        
        @self.bot.event
        async def on_ready():
            print(f"Bot {self.bot.user} is ready!")
            self.is_running = True
        
        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return
            
            # Process custom message events
            for event in self.events:
                if event.event_type == "message":
                    await self._handle_message_event(event, message)
            
            # Process commands
            await self.bot.process_commands(message)
    
    async def _handle_message_event(self, event: ConvoDiscordEvent, message):
        """Handle custom message events"""
        try:
            # Check conditions
            if event.condition:
                if not self._check_message_condition(event.condition, message):
                    return
            
            # Execute action
            if callable(event.action):
                result = event.action(message)
                if result:
                    await message.channel.send(str(result))
        except Exception as e:
            print(f"Error in message event: {e}")
    
    def _check_message_condition(self, condition: str, message) -> bool:
        """Check if message meets condition"""
        condition = condition.lower().strip()
        message_content = message.content.lower()
        
        if "contains" in condition:
            # Extract what it should contain
            match = re.search(r'contains\s+"([^"]*)"', condition)
            if match:
                return match.group(1) in message_content
        
        elif "starts with" in condition:
            match = re.search(r'starts with\s+"([^"]*)"', condition)
            if match:
                return message_content.startswith(match.group(1))
        
        elif "ends with" in condition:
            match = re.search(r'ends with\s+"([^"]*)"', condition)
            if match:
                return message_content.endswith(match.group(1))
        
        elif "equals" in condition:
            match = re.search(r'equals\s+"([^"]*)"', condition)
            if match:
                return message_content == match.group(1)
        
        return False
    
    def add_message_listener(self, condition: str, action: Callable):
        """Add a message event listener"""
        event = ConvoDiscordEvent(
            event_type="message",
            condition=condition,
            action=action,
            parameters={}
        )
        self.events.append(event)
    
    def add_command(self, name: str, description: str, action: Callable):
        """Add a Discord command"""
        command_obj = ConvoDiscordCommand(
            name=name,
            description=description,
            action=action,
            parameters=[]
        )
        self.commands.append(command_obj)
        
        # Register with discord.py
        @self.bot.command(name=name, help=description)
        async def discord_command(ctx, *args):
            try:
                result = action(ctx, *args)
                if result:
                    await ctx.send(str(result))
            except Exception as e:
                await ctx.send(f"Error: {e}")
    
    def add_slash_command(self, name: str, description: str, action: Callable, guild_id: Optional[int] = None):
        """Add a slash command (global or guild-specific)"""
        command_obj = ConvoDiscordCommand(
            name=name,
            description=description,
            action=action,
            parameters=[]
        )
        self.commands.append(command_obj)
        
        # Register slash command with discord.py
        if guild_id:
            # Guild-specific command
            if discord is None:
                raise RuntimeError("Discord library not available")
            @self.bot.tree.command(name=name, description=description, guild=discord.Object(id=guild_id))
            async def slash_command(interaction):  # Remove type hint to avoid linter issues
                try:
                    result = action(interaction)
                    if result:
                        await interaction.response.send_message(str(result))
                    else:
                        await interaction.response.send_message("Command executed successfully!")
                except Exception as e:
                    await interaction.response.send_message(f"Error: {e}")
        else:
            # Global command
            @self.bot.tree.command(name=name, description=description)
            async def slash_command(interaction):  # Remove type hint to avoid linter issues
                try:
                    result = action(interaction)
                    if result:
                        await interaction.response.send_message(str(result))
                    else:
                        await interaction.response.send_message("Command executed successfully!")
                except Exception as e:
                    await interaction.response.send_message(f"Error: {e}")
    
    async def sync_commands(self, guild_id: Optional[int] = None):
        """Sync slash commands with Discord"""
        try:
            if guild_id:
                # Sync to specific guild
                if discord is None:
                    raise RuntimeError("Discord library not available")
                guild = discord.Object(id=guild_id)
                synced = await self.bot.tree.sync(guild=guild)
                print(f"Synced {len(synced)} commands to guild {guild_id}")
            else:
                # Sync globally
                synced = await self.bot.tree.sync()
                print(f"Synced {len(synced)} global commands")
        except Exception as e:
            print(f"Failed to sync commands: {e}")
    
    def start(self):
        """Start the Discord bot"""
        if not self.token:
            raise RuntimeError("Bot token is required")
        
        print(f"Starting Discord bot with prefix '{self.prefix}'...")
        try:
            self.bot.run(self.token)
        except KeyboardInterrupt:
            print("Bot stopped by user")
        except Exception as e:
            print(f"Bot error: {e}")

class DiscordModule:
    """Discord module for Convo language integration"""
    
    def __init__(self):
        self.current_bot: Optional[ConvoDiscordBot] = None
        self.message_handlers: List[Callable] = []
        self.command_handlers: Dict[str, Callable] = {}
    
    def create_bot(self, token: str, prefix: str = "!") -> ConvoDiscordBot:
        """Create a new Discord bot instance"""
        self.current_bot = ConvoDiscordBot(token, prefix)
        return self.current_bot
    
    def listen_for_messages(self, condition: str, action: Callable):
        """Add message listener to current bot"""
        if not self.current_bot:
            raise RuntimeError("No bot created. Use 'Create bot' first.")
        
        self.current_bot.add_message_listener(condition, action)
    
    def add_command(self, name: str, description: str, action: Callable):
        """Add command to current bot"""
        if not self.current_bot:
            raise RuntimeError("No bot created. Use 'Create bot' first.")
        
        self.current_bot.add_command(name, description, action)
    
    def add_slash_command(self, name: str, description: str, action: Callable, guild_id: Optional[int] = None):
        """Add slash command to current bot (global or guild-specific)"""
        if not self.current_bot:
            raise RuntimeError("No bot created. Use 'Create bot' first.")
        
        self.current_bot.add_slash_command(name, description, action, guild_id)
    
    def sync_commands(self, guild_id: Optional[int] = None):
        """Sync slash commands with Discord"""
        if not self.current_bot:
            raise RuntimeError("No bot created. Use 'Create bot' first.")
        
        # Run the sync in the bot's event loop
        asyncio.create_task(self.current_bot.sync_commands(guild_id))
    
    def start_bot(self):
        """Start the current bot"""
        if not self.current_bot:
            raise RuntimeError("No bot created. Use 'Create bot' first.")
        
        self.current_bot.start()
    
    def reply_with(self, text: str):
        """Create a reply function for bot responses"""
        return lambda *args: text
    
    def get_user_mention(self, message):
        """Get the mention for the message author"""
        if hasattr(message, 'author'):
            return f"<@{message.author.id}>"
        return "User"
    
    def get_channel_name(self, message):
        """Get the channel name"""
        if hasattr(message, 'channel') and hasattr(message.channel, 'name'):
            return message.channel.name
        return "unknown"
    
    def get_server_name(self, message):
        """Get the server name"""
        if hasattr(message, 'guild') and hasattr(message.guild, 'name'):
            return message.guild.name
        return "Direct Message"

# Global Discord module instance
discord_module = DiscordModule()

# Built-in functions for Discord integration
def create_discord_bot(token: str, prefix: str = "!"):
    """Create a Discord bot with the given token and prefix"""
    if not token or token.strip() == "":
        raise ValueError("Bot token cannot be empty")
    
    if token == "YOUR_BOT_TOKEN_HERE":
        raise ValueError("Please replace 'YOUR_BOT_TOKEN_HERE' with your actual Discord bot token")
    
    try:
        print(f"Creating Discord bot with prefix '{prefix}'...")
        bot = discord_module.create_bot(token, prefix)
        print("Discord bot created successfully!")
        return bot
    except Exception as e:
        print(f"Failed to create Discord bot: {e}")
        raise RuntimeError(f"Discord bot creation failed: {e}")

def listen_for_message(condition: str, action: Callable):
    """Listen for messages matching condition"""
    discord_module.listen_for_messages(condition, action)

def add_discord_command(name: str, description: str, action: Callable):
    """Add a Discord command"""
    discord_module.add_command(name, description, action)

def create_global_slash_command(name: str, description: str, action: Callable):
    """Create a global slash command (available in all servers)"""
    discord_module.add_slash_command(name, description, action, None)

def create_guild_slash_command(name: str, description: str, action: Callable, guild_id: int):
    """Create a guild-specific slash command (only available in specified server)"""
    discord_module.add_slash_command(name, description, action, guild_id)

def create_slash_command(name: str, description: str, action: Callable):
    """Create a slash command (legacy function - creates global command)"""
    discord_module.add_slash_command(name, description, action, None)

def sync_discord_commands(guild_id: Optional[int] = None):
    """Sync slash commands with Discord"""
    discord_module.sync_commands(guild_id)

def sync_global_commands():
    """Sync global slash commands with Discord"""
    discord_module.sync_commands(None)

def sync_guild_commands(guild_id: int):
    """Sync guild-specific slash commands with Discord"""
    discord_module.sync_commands(guild_id)

def start_discord_bot():
    """Start the Discord bot"""
    discord_module.start_bot()

def reply_with_text(text: str):
    """Create a reply function"""
    return discord_module.reply_with(text)

def get_user_name(message):
    """Get the username from a message"""
    if hasattr(message, 'author') and hasattr(message.author, 'display_name'):
        return message.author.display_name
    return "User"

def get_message_content(message):
    """Get the content of a message"""
    if hasattr(message, 'content'):
        return message.content
    return ""

def get_interaction_user(interaction):
    """Get the user from an interaction"""
    if hasattr(interaction, 'user') and hasattr(interaction.user, 'display_name'):
        return interaction.user.display_name
    return "User"

def get_interaction_guild(interaction):
    """Get the guild from an interaction"""
    if hasattr(interaction, 'guild') and hasattr(interaction.guild, 'name'):
        return interaction.guild.name
    return "Unknown Server"

def get_interaction_channel(interaction):
    """Get the channel from an interaction"""
    if hasattr(interaction, 'channel') and hasattr(interaction.channel, 'name'):
        return interaction.channel.name
    return "Unknown Channel"

# Discord functions to be integrated into Convo builtins
try:
    from .discord_advanced import ADVANCED_DISCORD_FUNCTIONS
except ImportError:
    ADVANCED_DISCORD_FUNCTIONS = {}

try:
    from .discord_error_handling import DISCORD_ERROR_HANDLING
except ImportError:
    DISCORD_ERROR_HANDLING = {}

try:
    from .discord_ui import DISCORD_UI_FUNCTIONS
except ImportError:
    DISCORD_UI_FUNCTIONS = {}

DISCORD_FUNCTIONS = {
    'create_discord_bot': create_discord_bot,
    'listen_for_message': listen_for_message,
    'add_discord_command': add_discord_command,
    'create_global_slash_command': create_global_slash_command,
    'create_guild_slash_command': create_guild_slash_command,
    'create_slash_command': create_slash_command,
    'sync_discord_commands': sync_discord_commands,
    'sync_global_commands': sync_global_commands,
    'sync_guild_commands': sync_guild_commands,
    'start_discord_bot': start_discord_bot,
    'reply_with_text': reply_with_text,
    'get_user_name': get_user_name,
    'get_message_content': get_message_content,
    'get_interaction_user': get_interaction_user,
    'get_interaction_guild': get_interaction_guild,
    'get_interaction_channel': get_interaction_channel,
}

# Add advanced Discord functions
DISCORD_FUNCTIONS.update(ADVANCED_DISCORD_FUNCTIONS)

# Add error handling utilities
DISCORD_FUNCTIONS.update(DISCORD_ERROR_HANDLING)

# Add UI component functions
DISCORD_FUNCTIONS.update(DISCORD_UI_FUNCTIONS)
