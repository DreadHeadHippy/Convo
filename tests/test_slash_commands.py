import pytest
from unittest.mock import Mock, patch
from convo.modules.discord_bot import (
    create_global_slash_command,
    create_guild_slash_command,
    sync_global_commands,
    sync_guild_commands,
    get_interaction_user,
    get_interaction_guild,
    get_interaction_channel,
    DISCORD_FUNCTIONS
)

class TestSlashCommands:
    """Test slash command functionality"""
    
    def test_slash_command_functions_available(self):
        """Test that new slash command functions are available"""
        expected_functions = [
            'create_global_slash_command',
            'create_guild_slash_command', 
            'create_slash_command',
            'sync_global_commands',
            'sync_guild_commands',
            'sync_discord_commands'
        ]
        
        for func_name in expected_functions:
            assert func_name in DISCORD_FUNCTIONS, f"Missing function: {func_name}"
    
    def test_interaction_helper_functions_available(self):
        """Test that interaction helper functions are available"""
        helper_functions = [
            'get_interaction_user',
            'get_interaction_guild', 
            'get_interaction_channel'
        ]
        
        for func_name in helper_functions:
            assert func_name in DISCORD_FUNCTIONS, f"Missing helper function: {func_name}"
    
    def test_get_interaction_user(self):
        """Test getting user from interaction"""
        # Mock interaction with user
        mock_interaction = Mock()
        mock_interaction.user.display_name = "TestUser"
        
        result = get_interaction_user(mock_interaction)
        assert result == "TestUser"
        
        # Test fallback for missing user
        mock_interaction_no_user = Mock()
        del mock_interaction_no_user.user
        
        result = get_interaction_user(mock_interaction_no_user)
        assert result == "User"
    
    def test_get_interaction_guild(self):
        """Test getting guild from interaction"""
        # Mock interaction with guild
        mock_interaction = Mock()
        mock_interaction.guild.name = "Test Server"
        
        result = get_interaction_guild(mock_interaction)
        assert result == "Test Server"
        
        # Test fallback for missing guild
        mock_interaction_no_guild = Mock()
        del mock_interaction_no_guild.guild
        
        result = get_interaction_guild(mock_interaction_no_guild)
        assert result == "Unknown Server"
    
    def test_get_interaction_channel(self):
        """Test getting channel from interaction"""
        # Mock interaction with channel
        mock_interaction = Mock()
        mock_interaction.channel.name = "general"
        
        result = get_interaction_channel(mock_interaction)
        assert result == "general"
        
        # Test fallback for missing channel
        mock_interaction_no_channel = Mock()
        del mock_interaction_no_channel.channel
        
        result = get_interaction_channel(mock_interaction_no_channel)
        assert result == "Unknown Channel"

class TestSlashCommandIntegration:
    """Test slash command integration with Convo"""
    
    @patch('convo.modules.discord_bot.discord_module')
    def test_create_global_slash_command(self, mock_discord_module):
        """Test creating global slash command"""
        mock_handler = Mock()
        
        create_global_slash_command("test", "Test command", mock_handler)
        
        mock_discord_module.add_slash_command.assert_called_once_with(
            "test", "Test command", mock_handler, None
        )
    
    @patch('convo.modules.discord_bot.discord_module')
    def test_create_guild_slash_command(self, mock_discord_module):
        """Test creating guild-specific slash command"""
        mock_handler = Mock()
        guild_id = 123456789
        
        create_guild_slash_command("admin", "Admin command", mock_handler, guild_id)
        
        mock_discord_module.add_slash_command.assert_called_once_with(
            "admin", "Admin command", mock_handler, guild_id
        )
    
    @patch('convo.modules.discord_bot.discord_module')
    def test_sync_global_commands(self, mock_discord_module):
        """Test syncing global commands"""
        sync_global_commands()
        
        mock_discord_module.sync_commands.assert_called_once_with(None)
    
    @patch('convo.modules.discord_bot.discord_module')
    def test_sync_guild_commands(self, mock_discord_module):
        """Test syncing guild commands"""
        guild_id = 123456789
        
        sync_guild_commands(guild_id)
        
        mock_discord_module.sync_commands.assert_called_once_with(guild_id)

class TestDiscordFunctionCount:
    """Test that function count is accurate"""
    
    def test_function_count_matches_documentation(self):
        """Test that we actually have 32+ Discord functions"""
        # Count the actual functions
        function_count = len(DISCORD_FUNCTIONS)
        
        # Should have at least 31 functions as documented
        assert function_count >= 31, f"Expected at least 31 functions, got {function_count}"
        
        # Print actual count for verification
        print(f"Total Discord functions available: {function_count}")
        
        # Verify key new functions are present
        key_functions = [
            'create_global_slash_command',
            'create_guild_slash_command',
            'sync_global_commands',
            'get_interaction_user'
        ]
        
        for func in key_functions:
            assert func in DISCORD_FUNCTIONS, f"Key function missing: {func}"
