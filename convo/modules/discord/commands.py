"""
Convo Discord Command Framework
Provides natural language command registration and handling for Convo bots
"""
from typing import Callable, Dict

class CommandRegistry:
    def __init__(self):
        self.commands: Dict[str, Callable] = {}

    def add_command(self, name: str, handler: Callable):
        self.commands[name] = handler

    def get_command(self, name: str):
        return self.commands.get(name)

    def all_commands(self):
        return self.commands.keys()
