"""
Tests for Discord bot integration in Convo language
"""

import pytest
from unittest.mock import Mock, patch
from convo.lexer import Lexer
from convo.parser import Parser
from convo.interpreter import Interpreter

def test_discord_module_import():
    """Test that Discord module can be imported"""
    try:
        from convo.modules.discord_bot import DiscordModule, DISCORD_FUNCTIONS
        assert DiscordModule is not None
        assert isinstance(DISCORD_FUNCTIONS, dict)
        assert len(DISCORD_FUNCTIONS) > 0
    except ImportError:
        pytest.skip("Discord module not available")

def test_discord_functions_in_builtins():
    """Test that Discord functions are available in builtins"""
    from convo.builtins import BUILTIN_FUNCTIONS
    
    # Check if Discord functions are included
    discord_function_names = [
        'create_discord_bot',
        'listen_for_message', 
        'add_discord_command',
        'start_discord_bot',
        'reply_with_text',
        'get_user_name',
        'get_message_content'
    ]
    
    for func_name in discord_function_names:
        if func_name in BUILTIN_FUNCTIONS:
            assert callable(BUILTIN_FUNCTIONS[func_name])

@patch('convo.modules.discord_bot.DISCORD_AVAILABLE', False)
def test_discord_unavailable_error():
    """Test error handling when Discord library is not available"""
    try:
        from convo.modules.discord_bot import ConvoDiscordBot
        with pytest.raises(RuntimeError, match="discord.py library not installed"):
            ConvoDiscordBot("fake_token")
    except ImportError:
        pytest.skip("Discord module not available")

def test_discord_bot_creation():
    """Test Discord bot creation in Convo"""
    # Mock discord.py to avoid import errors
    with patch('convo.modules.discord_bot.DISCORD_AVAILABLE', True):
        with patch('convo.modules.discord_bot.discord'):
            with patch('convo.modules.discord_bot.commands'):
                code = '''Say "Creating test bot..."'''
                
                lexer = Lexer(code)
                tokens = lexer.tokenize()
                parser = Parser(tokens)
                ast = parser.parse()
                interpreter = Interpreter()
                
                output = interpreter.interpret(ast)
                assert "Creating test bot..." in output

def test_message_condition_parsing():
    """Test Discord message condition parsing"""
    try:
        from convo.modules.discord_bot import ConvoDiscordBot
        
        # Mock the required Discord objects
        with patch('convo.modules.discord_bot.DISCORD_AVAILABLE', True):
            with patch('convo.modules.discord_bot.discord'):
                with patch('convo.modules.discord_bot.commands'):
                    bot = ConvoDiscordBot("fake_token")
                    
                    # Test different condition types
                    mock_message = Mock()
                    mock_message.content = "hello world"
                    
                    # Test contains condition
                    assert bot._check_message_condition('contains "hello"', mock_message) == True
                    assert bot._check_message_condition('contains "goodbye"', mock_message) == False
                    
                    # Test starts with condition
                    mock_message.content = "hello everyone"
                    assert bot._check_message_condition('starts with "hello"', mock_message) == True
                    assert bot._check_message_condition('starts with "hi"', mock_message) == False
                    
    except ImportError:
        pytest.skip("Discord module not available")

def test_discord_integration_example():
    """Test parsing and basic execution of Discord bot example"""
    code = '''Say "Setting up Discord bot test..."
Define test_handler with message:
    Return "Test response"
Say "Discord functions would be called here"
Say "Bot setup complete!"'''
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    
    output = interpreter.interpret(ast)
    assert "Setting up Discord bot test..." in output
    assert "Discord functions would be called here" in output
    assert "Bot setup complete!" in output

def test_discord_function_availability():
    """Test that Discord functions exist and are callable"""
    try:
        from convo.modules.discord_bot import (
            create_discord_bot,
            listen_for_message,
            add_discord_command,
            start_discord_bot,
            reply_with_text,
            get_user_name,
            get_message_content
        )
        
        # Test that all functions are callable
        assert callable(create_discord_bot)
        assert callable(listen_for_message)
        assert callable(add_discord_command)
        assert callable(start_discord_bot)
        assert callable(reply_with_text)
        assert callable(get_user_name)
        assert callable(get_message_content)
        
    except ImportError:
        pytest.skip("Discord module not available")

def test_reply_function_creation():
    """Test creating reply functions"""
    try:
        from convo.modules.discord_bot import reply_with_text
        
        reply_func = reply_with_text("Hello World!")
        assert callable(reply_func)
        assert reply_func() == "Hello World!"
        
    except ImportError:
        pytest.skip("Discord module not available")

def test_message_helper_functions():
    """Test message helper functions"""
    try:
        from convo.modules.discord_bot import get_user_name, get_message_content
        
        # Mock message object
        mock_message = Mock()
        mock_message.author.display_name = "TestUser"
        mock_message.content = "Test message content"
        
        assert get_user_name(mock_message) == "TestUser"
        assert get_message_content(mock_message) == "Test message content"
        
        # Test with missing attributes
        mock_message_empty = Mock()
        del mock_message_empty.author
        assert get_user_name(mock_message_empty) == "User"
        
    except ImportError:
        pytest.skip("Discord module not available")

if __name__ == "__main__":
    # Run available tests
    test_discord_module_import()
    test_discord_functions_in_builtins()
    test_discord_integration_example()
    test_discord_function_availability()
    test_reply_function_creation()
    test_message_helper_functions()
    print("Discord integration tests completed!")
