"""
Discord UI Components for Convo Programming Language

This file contains Discord UI functionality including:
- Interactive buttons
- Modal dialogs
- Select dropdown menus
- View components
- Context menus
- Auto-complete for slash commands
"""

from typing import Any, Callable, Dict, List, Optional, Union

def create_button(label: str, style: str = "primary", custom_id: Optional[str] = None, emoji: Optional[str] = None, disabled: bool = False):
    """Create an interactive button for Discord messages
    
    Args:
        label: Button text
        style: Button style ("primary", "secondary", "success", "danger", "link")
        custom_id: Unique identifier for the button
        emoji: Emoji to display on button
        disabled: Whether the button is disabled
    """
    try:
        import discord
        
        # Map style names to Discord button styles
        style_map = {
            "primary": discord.ButtonStyle.primary,
            "secondary": discord.ButtonStyle.secondary,
            "success": discord.ButtonStyle.success,
            "danger": discord.ButtonStyle.danger,
            "link": discord.ButtonStyle.link
        }
        
        button_style = style_map.get(style.lower(), discord.ButtonStyle.primary)
        
        # Create button
        button = discord.ui.Button(
            label=label,
            style=button_style,
            custom_id=custom_id or f"btn_{label.lower().replace(' ', '_')}",
            emoji=emoji,
            disabled=disabled
        )
        
        return button
        
    except ImportError:
        raise ImportError("Discord.py is required for button functionality. Install with: pip install discord.py")
    except Exception as e:
        raise RuntimeError(f"Failed to create button: {e}")

def create_select_menu(placeholder: str, options: List[Dict[str, str]], custom_id: Optional[str] = None, min_values: int = 1, max_values: int = 1):
    """Create a select dropdown menu
    
    Args:
        placeholder: Placeholder text for the menu
        options: List of option dictionaries with 'label', 'value', 'description', 'emoji'
        custom_id: Unique identifier for the select menu
        min_values: Minimum number of selections
        max_values: Maximum number of selections
    """
    try:
        import discord
        
        # Convert options to Discord select options
        select_options = []
        for option in options:
            select_option = discord.SelectOption(
                label=option.get('label', 'Option'),
                value=option.get('value', option.get('label', 'option')),
                description=option.get('description'),
                emoji=option.get('emoji')
            )
            select_options.append(select_option)
        
        # Create select menu
        select = discord.ui.Select(
            placeholder=placeholder,
            options=select_options,
            custom_id=custom_id or "select_menu",
            min_values=min_values,
            max_values=max_values
        )
        
        return select
        
    except ImportError:
        raise ImportError("Discord.py is required for select menu functionality. Install with: pip install discord.py")
    except Exception as e:
        raise RuntimeError(f"Failed to create select menu: {e}")

def create_modal_input(label: str, placeholder: Optional[str] = None, required: bool = True, 
                      min_length: Optional[int] = None, max_length: Optional[int] = None, style: str = "short"):
    """Create a text input for modals
    
    Args:
        label: Input label
        placeholder: Placeholder text
        required: Whether the input is required
        min_length: Minimum length
        max_length: Maximum length
        style: Input style ("short", "long", "paragraph")
    """
    try:
        import discord
        
        style_map = {
            "short": discord.TextStyle.short,
            "long": discord.TextStyle.long,
            "paragraph": discord.TextStyle.paragraph
        }
        
        text_input = discord.ui.TextInput(
            label=label,
            placeholder=placeholder,
            required=required,
            min_length=min_length,
            max_length=max_length,
            style=style_map.get(style.lower(), discord.TextStyle.short)
        )
        
        return text_input
        
    except ImportError:
        raise ImportError("Discord.py is required for text input functionality. Install with: pip install discord.py")
    except Exception as e:
        raise RuntimeError(f"Failed to create text input: {e}")

def create_modal(title: str, custom_id: Optional[str] = None, inputs: Optional[List] = None):
    """Create a modal dialog for user input
    
    Args:
        title: Modal title
        custom_id: Unique identifier for the modal
        inputs: List of text inputs to add to the modal
    """
    try:
        import discord
        
        class ConvoModal(discord.ui.Modal, title=title):
            def __init__(self, custom_id: Optional[str] = None, inputs: Optional[List] = None):
                super().__init__(custom_id=custom_id or "convo_modal")
                self.callback_function = None
                self.input_values = {}
                
                # Add inputs if provided
                if inputs:
                    for text_input in inputs:
                        self.add_item(text_input)
            
            def set_callback(self, callback: Callable):
                """Set the callback function for when modal is submitted"""
                self.callback_function = callback
            
            async def on_submit(self, interaction: discord.Interaction):
                # Collect all field values
                field_values = {}
                for child in self.children:
                    if isinstance(child, discord.ui.TextInput):
                        field_name = child.label.lower().replace(' ', '_')
                        field_values[field_name] = child.value
                
                if self.callback_function:
                    try:
                        result = self.callback_function(interaction, field_values)
                        if result:
                            await interaction.response.send_message(str(result), ephemeral=True)
                        else:
                            await interaction.response.send_message("Modal submitted successfully!", ephemeral=True)
                    except Exception as e:
                        await interaction.response.send_message(f"Error processing modal: {e}", ephemeral=True)
                else:
                    await interaction.response.send_message("Modal submitted!", ephemeral=True)
        
        return ConvoModal(custom_id, inputs)
        
    except ImportError:
        raise ImportError("Discord.py is required for modal functionality. Install with: pip install discord.py")
    except Exception as e:
        raise RuntimeError(f"Failed to create modal: {e}")

def create_view(timeout: float = 180):
    """Create a view container for UI components"""
    try:
        import discord
        
        class ConvoView(discord.ui.View):
            def __init__(self, timeout: float = 180):
                super().__init__(timeout=timeout)
                self.component_callbacks = {}
            
            def add_button(self, button, callback: Optional[Callable] = None):
                """Add a button to the view with optional callback"""
                if callback:
                    # Create a dynamic callback for this button
                    async def button_callback(interaction: discord.Interaction):
                        try:
                            result = callback(interaction)
                            if result:
                                await interaction.response.send_message(str(result), ephemeral=True)
                            else:
                                await interaction.response.send_message("Button clicked!", ephemeral=True)
                        except Exception as e:
                            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
                    
                    button.callback = button_callback
                
                self.add_item(button)
                return button
            
            def add_select(self, select, callback: Optional[Callable] = None):
                """Add a select menu to the view with optional callback"""
                if callback:
                    # Create a dynamic callback for this select menu
                    async def select_callback(interaction: discord.Interaction):
                        try:
                            result = callback(interaction, select.values)
                            if result:
                                await interaction.response.send_message(str(result), ephemeral=True)
                            else:
                                await interaction.response.send_message(f"Selected: {', '.join(select.values)}", ephemeral=True)
                        except Exception as e:
                            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
                    
                    select.callback = select_callback
                
                self.add_item(select)
                return select
            
            async def on_timeout(self):
                """Called when the view times out"""
                for item in self.children:
                    if isinstance(item, (discord.ui.Button, discord.ui.Select)):
                        item.disabled = True
        
        return ConvoView(timeout)
        
    except ImportError:
        raise ImportError("Discord.py is required for view functionality. Install with: pip install discord.py")
    except Exception as e:
        raise RuntimeError(f"Failed to create view: {e}")

def send_message_with_components(channel, content: Optional[str] = None, embed=None, view=None):
    """Send a message with UI components
    
    Args:
        channel: Discord channel to send to
        content: Message content
        embed: Discord embed
        view: View with UI components
    """
    try:
        import discord
        import asyncio
        
        async def send():
            return await channel.send(content=content, embed=embed, view=view)
        
        # Return the coroutine to be awaited by the bot
        return send()
        
    except ImportError:
        raise ImportError("Discord.py is required for sending messages with components. Install with: pip install discord.py")
    except Exception as e:
        raise RuntimeError(f"Failed to send message with components: {e}")

def create_embed_with_components(title: str, description: str, color: Optional[str] = None, 
                                buttons: Optional[List] = None, select_menu = None):
    """Create an embed with interactive components
    
    Args:
        title: Embed title
        description: Embed description
        color: Embed color (hex string like "#FF0000")
        buttons: List of buttons to add
        select_menu: Select menu to add
    """
    try:
        import discord
        
        # Create embed
        embed = discord.Embed(title=title, description=description)
        
        # Set color if provided
        if color and color.startswith('#'):
            embed.color = int(color[1:], 16)
        
        # Create view for components
        view = create_view()
        
        # Add buttons if provided
        if buttons:
            for button in buttons:
                view.add_button(button)
        
        # Add select menu if provided
        if select_menu:
            view.add_select(select_menu)
        
        return embed, view
        
    except ImportError:
        raise ImportError("Discord.py is required for embed functionality. Install with: pip install discord.py")
    except Exception as e:
        raise RuntimeError(f"Failed to create embed with components: {e}")

def show_modal(interaction, modal):
    """Show a modal to the user
    
    Args:
        interaction: Discord interaction
        modal: Modal to show
    """
    try:
        import discord
        import asyncio
        
        async def send_modal():
            await interaction.response.send_modal(modal)
        
        return send_modal()
        
    except ImportError:
        raise ImportError("Discord.py is required for showing modals. Install with: pip install discord.py")
    except Exception as e:
        raise RuntimeError(f"Failed to show modal: {e}")

def create_context_menu_user(name: str):
    """Create a user context menu command
    
    Args:
        name: Command name
    """
    def decorator(func):
        func._context_menu_name = name
        func._context_menu_type = "user"
        return func
    return decorator

def create_context_menu_message(name: str):
    """Create a message context menu command
    
    Args:
        name: Command name
    """
    def decorator(func):
        func._context_menu_name = name
        func._context_menu_type = "message"
        return func
    return decorator

def create_autocomplete_choices(choices: List[str]):
    """Create static autocomplete choices
    
    Args:
        choices: List of static choices
    """
    return {
        'type': 'static',
        'choices': choices
    }

def create_dynamic_autocomplete(function: Callable):
    """Create dynamic autocomplete choices
    
    Args:
        function: Function that returns choices based on current input
    """
    return {
        'type': 'dynamic',
        'function': function
    }

# UI Component functions dictionary
DISCORD_UI_FUNCTIONS = {
    'create_button': create_button,
    'create_select_menu': create_select_menu,
    'create_modal_input': create_modal_input,
    'create_modal': create_modal,
    'create_view': create_view,
    'send_message_with_components': send_message_with_components,
    'create_embed_with_components': create_embed_with_components,
    'show_modal': show_modal,
    'create_context_menu_user': create_context_menu_user,
    'create_context_menu_message': create_context_menu_message,
    'create_autocomplete_choices': create_autocomplete_choices,
    'create_dynamic_autocomplete': create_dynamic_autocomplete,
}
