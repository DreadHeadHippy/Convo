"""
Built-in functions for the Convo programming language
"""

import math
import random
import os
import json
from typing import Any, List, Dict

# Import Discord functions if available
try:
    from .modules.discord_bot import DISCORD_FUNCTIONS
except ImportError:
    DISCORD_FUNCTIONS = {}

class ConvoBuiltins:
    """Container for all built-in Convo functions"""
    
    @staticmethod
    def length(obj):
        """Get the length of a string, list, or dictionary"""
        if hasattr(obj, '__len__'):
            return len(obj)
        else:
            raise TypeError(f"Object of type {type(obj).__name__} has no length")
    
    @staticmethod
    def append(lst, item):
        """Add an item to the end of a list"""
        if isinstance(lst, list):
            lst.append(item)
            return lst
        else:
            raise TypeError("Can only append to lists")
    
    @staticmethod
    def remove(lst, item):
        """Remove the first occurrence of an item from a list"""
        if isinstance(lst, list):
            if item in lst:
                lst.remove(item)
            return lst
        else:
            raise TypeError("Can only remove from lists")
    
    @staticmethod
    def contains(container, item):
        """Check if an item is in a container"""
        return item in container
    
    @staticmethod
    def keys(dictionary):
        """Get all keys from a dictionary"""
        if isinstance(dictionary, dict):
            return list(dictionary.keys())
        else:
            raise TypeError("Can only get keys from dictionaries")
    
    @staticmethod
    def values(dictionary):
        """Get all values from a dictionary"""
        if isinstance(dictionary, dict):
            return list(dictionary.values())
        else:
            raise TypeError("Can only get values from dictionaries")
    
    # Math functions
    @staticmethod
    def abs(number):
        """Get absolute value of a number"""
        return abs(number)
    
    @staticmethod
    def sqrt(number):
        """Get square root of a number"""
        return math.sqrt(number)
    
    @staticmethod
    def power(base, exponent):
        """Raise base to the power of exponent"""
        return base ** exponent
    
    @staticmethod
    def round(number, digits=0):
        """Round a number to specified decimal places"""
        return round(number, digits)
    
    @staticmethod
    def floor(number):
        """Get the floor of a number"""
        return math.floor(number)
    
    @staticmethod
    def ceiling(number):
        """Get the ceiling of a number"""
        return math.ceil(number)
    
    @staticmethod
    def random():
        """Get a random number between 0 and 1"""
        return random.random()
    
    @staticmethod
    def random_int(min_val, max_val):
        """Get a random integer between min and max (inclusive)"""
        return random.randint(min_val, max_val)
    
    # String functions
    @staticmethod
    def upper(text):
        """Convert text to uppercase"""
        return str(text).upper()
    
    @staticmethod
    def lower(text):
        """Convert text to lowercase"""
        return str(text).lower()
    
    @staticmethod
    def trim(text):
        """Remove whitespace from beginning and end of text"""
        return str(text).strip()
    
    @staticmethod
    def split(text, separator=" "):
        """Split text by separator into a list"""
        return str(text).split(separator)
    
    @staticmethod
    def join(lst, separator=""):
        """Join a list of items into a string with separator"""
        return separator.join(str(item) for item in lst)
    
    @staticmethod
    def replace(text, old, new):
        """Replace all occurrences of old with new in text"""
        return str(text).replace(old, new)
    
    @staticmethod
    def starts_with(text, prefix):
        """Check if text starts with prefix"""
        return str(text).startswith(prefix)
    
    @staticmethod
    def ends_with(text, suffix):
        """Check if text ends with suffix"""
        return str(text).endswith(suffix)
    
    # File I/O functions
    @staticmethod
    def read_file(filename):
        """Read contents of a file"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            raise RuntimeError(f"File not found: {filename}")
        except Exception as e:
            raise RuntimeError(f"Error reading file: {e}")
    
    @staticmethod
    def write_file(filename, content):
        """Write content to a file"""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(str(content))
            return True
        except Exception as e:
            raise RuntimeError(f"Error writing file: {e}")
    
    @staticmethod
    def append_file(filename, content):
        """Append content to a file"""
        try:
            with open(filename, 'a', encoding='utf-8') as file:
                file.write(str(content))
            return True
        except Exception as e:
            raise RuntimeError(f"Error appending to file: {e}")
    
    @staticmethod
    def file_exists(filename):
        """Check if a file exists"""
        return os.path.exists(filename)
    
    @staticmethod
    def delete_file(filename):
        """Delete a file"""
        try:
            os.remove(filename)
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            raise RuntimeError(f"Error deleting file: {e}")
    
    # Type conversion functions
    @staticmethod
    def to_number(value):
        """Convert value to a number"""
        try:
            if '.' in str(value):
                return float(value)
            else:
                return int(value)
        except ValueError:
            raise RuntimeError(f"Cannot convert '{value}' to number")
    
    @staticmethod
    def to_text(value):
        """Convert value to text"""
        return str(value)
    
    @staticmethod
    def to_list(value):
        """Convert value to a list"""
        if isinstance(value, str):
            return list(value)
        elif hasattr(value, '__iter__'):
            return list(value)
        else:
            return [value]
    
    # JSON functions
    @staticmethod
    def parse_json(text):
        """Parse JSON text into a dictionary or list"""
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON: {e}")
    
    @staticmethod
    def to_json(obj):
        """Convert an object to JSON text"""
        try:
            return json.dumps(obj, indent=2)
        except TypeError as e:
            raise RuntimeError(f"Cannot convert to JSON: {e}")

# Dictionary of all built-in functions
BUILTIN_FUNCTIONS = {
    # Collection functions
    'length': ConvoBuiltins.length,
    'append': ConvoBuiltins.append,
    'remove': ConvoBuiltins.remove,
    'contains': ConvoBuiltins.contains,
    'keys': ConvoBuiltins.keys,
    'values': ConvoBuiltins.values,
    
    # Math functions
    'abs': ConvoBuiltins.abs,
    'sqrt': ConvoBuiltins.sqrt,
    'power': ConvoBuiltins.power,
    'round': ConvoBuiltins.round,
    'floor': ConvoBuiltins.floor,
    'ceiling': ConvoBuiltins.ceiling,
    'random': ConvoBuiltins.random,
    'random_int': ConvoBuiltins.random_int,
    
    # String functions
    'upper': ConvoBuiltins.upper,
    'lower': ConvoBuiltins.lower,
    'trim': ConvoBuiltins.trim,
    'split': ConvoBuiltins.split,
    'join': ConvoBuiltins.join,
    'replace': ConvoBuiltins.replace,
    'starts_with': ConvoBuiltins.starts_with,
    'ends_with': ConvoBuiltins.ends_with,
    
    # File I/O functions
    'read_file': ConvoBuiltins.read_file,
    'write_file': ConvoBuiltins.write_file,
    'append_file': ConvoBuiltins.append_file,
    'file_exists': ConvoBuiltins.file_exists,
    'delete_file': ConvoBuiltins.delete_file,
    
    # Type conversion functions
    'to_number': ConvoBuiltins.to_number,
    'to_text': ConvoBuiltins.to_text,
    'to_list': ConvoBuiltins.to_list,
    
    # JSON functions
    'parse_json': ConvoBuiltins.parse_json,
    'to_json': ConvoBuiltins.to_json,
}

# Add Discord functions if available
BUILTIN_FUNCTIONS.update(DISCORD_FUNCTIONS)
