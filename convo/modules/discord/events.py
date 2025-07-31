"""
Convo Discord Event System
Allows registration and handling of Discord events in Convo bots.

Supported event types include:
- message (with or without embeds)
- reaction add/remove
- member join/leave
- custom events

Example event handler registration:

    def on_message_with_embed(message, embed):
        # Handle message with embed
        pass

    def on_reaction_add(message, reaction):
        # Handle reaction added to a message
        pass

    registry = EventRegistry()
    registry.add_event_handler('message_with_embed', on_message_with_embed)
    registry.add_event_handler('reaction_add', on_reaction_add)

See Convo syntax documentation below for usage in Convo programs.
"""
from typing import Callable, Dict, List

class EventRegistry:
    def __init__(self):
        """Initialize the event registry."""
        self.events: Dict[str, List[Callable]] = {}

    # Example handler signatures for reference:
    # def on_message_with_embed(message: ConvoMessage, embed: ConvoEmbed): ...
    # def on_reaction_add(message: ConvoMessage, reaction: ConvoReaction): ...

    def add_event_handler(self, event: str, handler: Callable):
        """Register a handler for a specific event."""
        if event not in self.events:
            self.events[event] = []
        self.events[event].append(handler)

    def remove_event_handler(self, event: str, handler: Callable) -> bool:
        """Remove a handler from an event. Returns True if removed, False if not found."""
        handlers = self.events.get(event)
        if handlers and handler in handlers:
            handlers.remove(handler)
            return True
        return False

    def get_handlers(self, event: str) -> List[Callable]:
        """Get all handlers registered for an event."""
        return self.events.get(event, [])

    def list_events(self) -> List[str]:
        """List all registered event names."""
        return list(self.events.keys())

    def clear_event_handlers(self, event: str):
        """Remove all handlers for a specific event."""
        if event in self.events:
            self.events[event] = []

    def clear_all(self):
        """Remove all event handlers for all events."""
        self.events.clear()
