# src/modules/input.py

import readline
from typing import NamedTuple

class ProcessedInput(NamedTuple):
    text: str
    is_command: bool
    command: str = None

def get_input(prompt: str) -> str:
    """Get input from the user with command history support."""
    return input(prompt)

def process_input(user_input: str) -> ProcessedInput:
    """Process user input to determine if it's a command or regular text."""
    stripped_input = user_input.strip()
    if stripped_input.startswith('/'):
        command = stripped_input[1:].lower()
        return ProcessedInput(text=stripped_input, is_command=True, command=command)
    return ProcessedInput(text=stripped_input, is_command=False)

def handle_command(command: str) -> str:
    """Handle various commands."""
    if command in ['q', 'quit', 'exit']:
        return 'quit'
    elif command == 'help':
        return 'help'
    # Add more command handlers as needed
    return 'unknown'

def get_multiline_input(prompt: str = "") -> str:
    """Get multiline input from the user."""
    print(prompt)
    lines = []
    while True:
        try:
            line = input()
            if line == "":
                break
            lines.append(line)
        except EOFError:
            break
    return '\n'.join(lines)

# You can add more utility functions related to input handling here

__all__ = ['get_input', 'process_input', 'handle_command', 'get_multiline_input', 'ProcessedInput']
