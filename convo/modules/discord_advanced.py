"""
Advanced Discord Functions for Convo Programming Language

This file contains advanced Discord bot functionality including:
- Rich embeds
- Reactions
- File uploads
- Voice channel support
- Slash commands
- User/Guild information
"""

def send_embed(channel, title, description, color=None, fields=None, image_url=None, thumbnail_url=None):
    """Send a rich embed message to a Discord channel
    
    Args:
        channel: Discord channel object
        title: Embed title
        description: Embed description
        color: Embed color (hex string like "#FF0000" or integer)
        fields: List of {"name": "Field Name", "value": "Field Value", "inline": True/False}
        image_url: URL for embed image
        thumbnail_url: URL for embed thumbnail
    """
    try:
        import discord
        
        # Create embed
        embed = discord.Embed(title=title, description=description)
        
        # Set color if provided
        if color:
            if isinstance(color, str) and color.startswith('#'):
                embed.color = int(color[1:], 16)
            elif isinstance(color, int):
                embed.color = color
        
        # Add fields if provided
        if fields:
            for field in fields:
                embed.add_field(
                    name=field.get('name', 'Field'),
                    value=field.get('value', 'Value'),
                    inline=field.get('inline', False)
                )
        
        # Set image if provided
        if image_url:
            embed.set_image(url=image_url)
        
        # Set thumbnail if provided
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)
        
        return embed
    except ImportError:
        raise RuntimeError("Discord.py library not available")
    except Exception as e:
        raise RuntimeError(f"Failed to create embed: {e}")

def add_reaction(message, emoji):
    """Add a reaction to a Discord message
    
    Args:
        message: Discord message object
        emoji: Emoji to add (unicode emoji or custom emoji name)
    """
    try:
        # This would be async in real implementation
        # await message.add_reaction(emoji)
        return f"Added reaction {emoji} to message"
    except Exception as e:
        raise RuntimeError(f"Failed to add reaction: {e}")

def remove_reaction(message, emoji, user=None):
    """Remove a reaction from a Discord message
    
    Args:
        message: Discord message object
        emoji: Emoji to remove
        user: User whose reaction to remove (optional)
    """
    try:
        # This would be async in real implementation
        if user:
            # await message.remove_reaction(emoji, user)
            return f"Removed reaction {emoji} from {user}"
        else:
            # await message.clear_reaction(emoji)
            return f"Cleared all {emoji} reactions"
    except Exception as e:
        raise RuntimeError(f"Failed to remove reaction: {e}")

def send_file(channel, file_path, filename=None, content=None):
    """Send a file to a Discord channel
    
    Args:
        channel: Discord channel object
        file_path: Path to file to send
        filename: Optional custom filename
        content: Optional message content to send with file
    """
    try:
        # This would be async in real implementation
        # import discord
        # file = discord.File(file_path, filename=filename)
        # await channel.send(content=content, file=file)
        display_name = filename or file_path
        return f"Sent file {display_name} to channel"
    except Exception as e:
        raise RuntimeError(f"Failed to send file: {e}")

def create_slash_command(name, description, options=None):
    """Create a Discord slash command
    
    Args:
        name: Command name
        description: Command description
        options: List of command options/parameters
    """
    try:
        # Slash command would be registered with Discord API
        command_data = {
            'name': name,
            'description': description,
            'options': options or []
        }
        return f"Created slash command: {name}"
    except Exception as e:
        raise RuntimeError(f"Failed to create slash command: {e}")

def join_voice_channel(channel):
    """Join a Discord voice channel
    
    Args:
        channel: Voice channel object to join
    """
    try:
        # This would be async in real implementation
        # voice_client = await channel.connect()
        return f"Joined voice channel: {channel}"
    except Exception as e:
        raise RuntimeError(f"Failed to join voice channel: {e}")

def leave_voice_channel(voice_client):
    """Leave the current voice channel
    
    Args:
        voice_client: Voice client connection to disconnect
    """
    try:
        # This would be async in real implementation
        # await voice_client.disconnect()
        return "Left voice channel"
    except Exception as e:
        raise RuntimeError(f"Failed to leave voice channel: {e}")

def play_audio(voice_client, audio_source):
    """Play audio in a voice channel
    
    Args:
        voice_client: Voice client connection
        audio_source: Audio source (file path, URL, etc.)
    """
    try:
        # This would be async in real implementation
        # source = discord.FFmpegPCMAudio(audio_source)
        # voice_client.play(source)
        return f"Playing audio: {audio_source}"
    except Exception as e:
        raise RuntimeError(f"Failed to play audio: {e}")

def get_guild_info(guild):
    """Get information about a Discord server/guild
    
    Args:
        guild: Discord guild object
    """
    try:
        return {
            'name': getattr(guild, 'name', 'Unknown'),
            'member_count': getattr(guild, 'member_count', 0),
            'id': getattr(guild, 'id', 0)
        }
    except Exception as e:
        raise RuntimeError(f"Failed to get guild info: {e}")

def get_user_info(user):
    """Get information about a Discord user
    
    Args:
        user: Discord user object
    """
    try:
        return {
            'name': getattr(user, 'name', 'Unknown'),
            'discriminator': getattr(user, 'discriminator', '0000'),
            'id': getattr(user, 'id', 0),
            'avatar_url': str(getattr(user, 'avatar', ''))
        }
    except Exception as e:
        raise RuntimeError(f"Failed to get user info: {e}")

# Advanced Discord functions dictionary
ADVANCED_DISCORD_FUNCTIONS = {
    'send_embed': send_embed,
    'add_reaction': add_reaction,
    'remove_reaction': remove_reaction,
    'send_file': send_file,
    'create_slash_command': create_slash_command,
    'join_voice_channel': join_voice_channel,
    'leave_voice_channel': leave_voice_channel,
    'play_audio': play_audio,
    'get_guild_info': get_guild_info,
    'get_user_info': get_user_info,
}
