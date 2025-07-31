"""
Convo Discord Client (V0.0.1)
A natural language Discord bot interface for Convo programs
Version: V0.0.1
"""
from typing import Callable, Optional
import discord
import asyncio

class DiscordClient(discord.Client):
    VERSION = "V0.0.1"

    def __init__(self, token: str, on_message: Optional[Callable] = None):
        super().__init__(intents=discord.Intents.default())
        self.token = token
        self.on_message_callback = on_message
        from .commands import CommandRegistry
        from .events import EventRegistry
        self.commands = CommandRegistry()
        self.events = EventRegistry()
    def add_command(self, name: str, handler: Callable):
        self.commands.add_command(name, handler)

    def add_event_handler(self, event: str, handler: Callable):
        self.events.add_event_handler(event, handler)

    async def on_ready(self):
        print(f"Convo Discord Bot is online as {self.user}")

    async def on_message(self, message):
        # Run registered event handlers for 'on_message'
        for handler in self.events.get_handlers('on_message'):
            await handler(self, message)
        # Command handling
        if message.content and message.content.startswith('!'):
            cmd = message.content.split()[0][1:]
            handler = self.commands.get_command(cmd)
            if handler:
                await handler(self, message)
        # Legacy callback
        if self.on_message_callback:
            await self.on_message_callback(self, message)

    def run_bot(self):
        asyncio.run(self._start())

    async def _start(self):
        await self.start(self.token)

    async def send_message(self, channel_id: int, content: str):
        channel = self.get_channel(channel_id)
        from discord import TextChannel, DMChannel
        if isinstance(channel, (TextChannel, DMChannel)):
            await channel.send(content)
        else:
            print(f"Channel {channel_id} not found or not a text/DM channel.")
