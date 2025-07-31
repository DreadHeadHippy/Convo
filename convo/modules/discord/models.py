"""
Convo Discord Models
Simple wrappers for Discord objects for use in Convo programs
"""
from discord import Message, User, TextChannel

class ConvoMessage:
    def __init__(self, message: Message):
        self.id = message.id
        self.content = message.content
        self.author = ConvoUser(message.author)
        self.channel = ConvoChannel(message.channel)

class ConvoUser:
    def __init__(self, user):
        self.id = getattr(user, 'id', None)
        self.name = getattr(user, 'name', None)
        self.display_name = getattr(user, 'display_name', self.name)


class ConvoChannel:
    def __init__(self, channel):
        self.id = getattr(channel, 'id', None)
        self.name = getattr(channel, 'name', None)
        self.type = type(channel).__name__

from typing import Optional

class ConvoEmbed:
    """Wrapper for Discord Embed objects."""
    def __init__(self, title: Optional[str] = None, description: Optional[str] = None, color: Optional[int] = None):
        self.title = title
        self.description = description
        self.color = color
        self.fields = []

    def add_field(self, name: str, value: str, inline: bool = False):
        self.fields.append({
            'name': name,
            'value': value,
            'inline': inline
        })

class ConvoReaction:
    """Wrapper for Discord Reaction objects."""
    def __init__(self, emoji, user):
        self.emoji = emoji
        self.user = ConvoUser(user)
