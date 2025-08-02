"""
Enhanced Error Handling for Discord Integration in Convo

This module provides improved error handling, logging, and debugging
capabilities for Discord bot functionality.
"""

import logging
import traceback
import sys
from typing import Any, Dict, Optional
from datetime import datetime

# Set up logging for Discord integration
def setup_discord_logging(log_level='INFO', log_file=None):
    """Set up logging for Discord integration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
    """
    logger = logging.getLogger('convo_discord')
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Initialize logger
discord_logger = setup_discord_logging()

class DiscordError(Exception):
    """Base class for Discord-related errors"""
    def __init__(self, message: str, error_code: str = None, details: Dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.timestamp = datetime.now()
        
        # Log the error
        discord_logger.error(f"Discord Error [{error_code}]: {message}")
        if details:
            discord_logger.error(f"Error details: {details}")

class DiscordConnectionError(DiscordError):
    """Error connecting to Discord API"""
    pass

class DiscordAuthenticationError(DiscordError):
    """Error authenticating with Discord"""
    pass

class DiscordPermissionError(DiscordError):
    """Error with Discord permissions"""
    pass

class DiscordRateLimitError(DiscordError):
    """Error due to Discord rate limiting"""
    pass

class DiscordConfigurationError(DiscordError):
    """Error in Discord bot configuration"""
    pass

def handle_discord_error(func):
    """Decorator to handle Discord API errors with enhanced error reporting"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ImportError as e:
            error = DiscordConfigurationError(
                "Discord.py library not available. Install with: pip install discord.py",
                error_code="DISCORD_LIB_MISSING",
                details={"import_error": str(e)}
            )
            return {"error": True, "message": error.message, "code": error.error_code}
        except Exception as e:
            # Categorize the error
            error_message = str(e)
            error_code = "DISCORD_UNKNOWN_ERROR"
            
            if "Invalid Token" in error_message or "Unauthorized" in error_message:
                error_code = "DISCORD_INVALID_TOKEN"
                error = DiscordAuthenticationError(
                    "Invalid Discord bot token. Check your DISCORD_TOKEN environment variable.",
                    error_code=error_code,
                    details={"original_error": error_message}
                )
            elif "Forbidden" in error_message or "Missing Permissions" in error_message:
                error_code = "DISCORD_PERMISSION_ERROR"
                error = DiscordPermissionError(
                    "Discord bot lacks required permissions for this action.",
                    error_code=error_code,
                    details={"original_error": error_message}
                )
            elif "Rate limit" in error_message or "Too Many Requests" in error_message:
                error_code = "DISCORD_RATE_LIMIT"
                error = DiscordRateLimitError(
                    "Discord API rate limit exceeded. Please wait before retrying.",
                    error_code=error_code,
                    details={"original_error": error_message}
                )
            elif "Connection" in error_message or "Network" in error_message:
                error_code = "DISCORD_CONNECTION_ERROR"
                error = DiscordConnectionError(
                    "Failed to connect to Discord API. Check your internet connection.",
                    error_code=error_code,
                    details={"original_error": error_message}
                )
            else:
                error = DiscordError(
                    f"Discord operation failed: {error_message}",
                    error_code=error_code,
                    details={"original_error": error_message, "traceback": traceback.format_exc()}
                )
            
            return {"error": True, "message": error.message, "code": error.error_code}
    
    return wrapper

def validate_discord_config(token: str = None, **kwargs) -> Dict[str, Any]:
    """Validate Discord bot configuration
    
    Args:
        token: Discord bot token
        **kwargs: Additional configuration parameters
        
    Returns:
        Dict with validation results
    """
    errors = []
    warnings = []
    
    # Check token
    if not token:
        errors.append("Discord bot token is required")
    elif len(token) < 50:  # Discord tokens are typically much longer
        warnings.append("Discord token appears to be too short")
    elif not token.startswith(('Bot ', 'Bearer ')):
        warnings.append("Discord token should typically start with 'Bot ' for bot tokens")
    
    # Check for common configuration issues
    if 'intents' in kwargs:
        intents = kwargs['intents']
        if isinstance(intents, dict):
            if intents.get('message_content', False):
                warnings.append("Message content intent requires verification for large bots")
    
    result = {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }
    
    if errors:
        discord_logger.error(f"Discord configuration validation failed: {errors}")
    if warnings:
        discord_logger.warning(f"Discord configuration warnings: {warnings}")
    
    return result

def get_discord_help(error_code: str = None) -> str:
    """Get helpful information for Discord errors
    
    Args:
        error_code: Specific error code to get help for
        
    Returns:
        Help message string
    """
    help_messages = {
        "DISCORD_LIB_MISSING": """
Discord.py library is not installed. To fix this:

1. Install the library:
   pip install discord.py

2. For voice support (optional):
   pip install discord.py[voice]

3. Verify installation:
   python -c "import discord; print('Discord.py installed successfully')"
""",
        "DISCORD_INVALID_TOKEN": """
Invalid Discord bot token. To fix this:

1. Go to https://discord.com/developers/applications
2. Select your application
3. Go to the 'Bot' section
4. Copy the token (click 'Reset Token' if needed)
5. Set the token in your environment:
   - Windows: set DISCORD_TOKEN=your_token_here
   - Linux/Mac: export DISCORD_TOKEN=your_token_here
6. Use the token in your Convo program:
   Let token be get_env("DISCORD_TOKEN")
""",
        "DISCORD_PERMISSION_ERROR": """
Discord bot lacks required permissions. To fix this:

1. Go to your Discord server
2. Right-click on your bot's role
3. Select 'Edit Role'
4. Grant necessary permissions in the 'Permissions' tab
5. Common permissions needed:
   - Send Messages
   - Read Message History
   - Use Slash Commands
   - Manage Messages (for reactions)
   - Connect/Speak (for voice)
""",
        "DISCORD_RATE_LIMIT": """
Discord API rate limit exceeded. To fix this:

1. Wait before making more requests (usually 1-60 seconds)
2. Implement request throttling in your bot
3. Avoid sending too many messages quickly
4. Use bulk operations when possible
5. Consider using Discord's gateway events instead of REST API
""",
        "DISCORD_CONNECTION_ERROR": """
Failed to connect to Discord API. To fix this:

1. Check your internet connection
2. Verify Discord services are online: https://discordstatus.com
3. Check if your firewall is blocking the connection
4. Try using a different network
5. Ensure your system time is correct
"""
    }
    
    if error_code and error_code in help_messages:
        return help_messages[error_code]
    
    return """
General Discord troubleshooting:

1. Check Discord.py installation: pip install discord.py
2. Verify bot token is correct and properly set
3. Ensure bot has necessary permissions
4. Check Discord API status: https://discordstatus.com
5. Review bot logs for specific error messages
6. Test with a simple bot first

For more help, visit:
- Discord.py documentation: https://discordpy.readthedocs.io/
- Discord Developer Portal: https://discord.com/developers/docs
"""

def debug_discord_environment() -> Dict[str, Any]:
    """Debug Discord environment and report status
    
    Returns:
        Dict with environment debug information
    """
    debug_info = {
        "timestamp": datetime.now().isoformat(),
        "python_version": sys.version,
        "discord_py_available": False,
        "discord_py_version": None,
        "token_configured": False,
        "system_info": {
            "platform": sys.platform
        }
    }
    
    # Check discord.py availability
    try:
        import discord
        debug_info["discord_py_available"] = True
        debug_info["discord_py_version"] = discord.__version__
    except ImportError:
        pass
    
    # Check token configuration
    import os
    if os.environ.get('DISCORD_TOKEN'):
        debug_info["token_configured"] = True
    
    return debug_info

# Enhanced function wrappers with error handling
def safe_create_discord_bot(token: str, **kwargs):
    """Safely create a Discord bot with enhanced error handling"""
    validation = validate_discord_config(token, **kwargs)
    if not validation["valid"]:
        return {
            "error": True,
            "message": f"Configuration validation failed: {', '.join(validation['errors'])}",
            "code": "DISCORD_CONFIG_INVALID",
            "help": get_discord_help("DISCORD_INVALID_TOKEN")
        }
    
    try:
        # Import the original function
        from .discord_bot import create_discord_bot
        return create_discord_bot(token, **kwargs)
    except Exception as e:
        return handle_discord_error(lambda: create_discord_bot(token, **kwargs))()

# Error handling utilities for Convo integration
DISCORD_ERROR_HANDLING = {
    'setup_discord_logging': setup_discord_logging,
    'handle_discord_error': handle_discord_error,
    'validate_discord_config': validate_discord_config,
    'get_discord_help': get_discord_help,
    'debug_discord_environment': debug_discord_environment,
    'safe_create_discord_bot': safe_create_discord_bot,
}
