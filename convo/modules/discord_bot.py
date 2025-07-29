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
        self.bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
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
    return discord_module.create_bot(token, prefix)

def listen_for_message(condition: str, action: Callable):
    """Listen for messages matching condition"""
    discord_module.listen_for_messages(condition, action)

def add_discord_command(name: str, description: str, action: Callable):
    """Add a Discord command"""
    discord_module.add_command(name, description, action)

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

# Discord functions to be integrated into Convo builtins
DISCORD_FUNCTIONS = {
    'create_discord_bot': create_discord_bot,
    'listen_for_message': listen_for_message,
    'add_discord_command': add_discord_command,
    'start_discord_bot': start_discord_bot,
    'reply_with_text': reply_with_text,
    'get_user_name': get_user_name,
    'get_message_content': get_message_content,
}
