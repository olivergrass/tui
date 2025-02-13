import sys
import select
import tty
import termios
from dataclasses import dataclass
from typing import Optional, Callable


@dataclass
class KeyEvent:
    key: str
    ctrl: bool = False
    alt: bool = False
    char: str = ""


class KeyboardHandler:
    def __init__(self) -> None:
        self.handlers: dict[str, Callable[[KeyEvent], None]] = {}
        self.text_handler: Optional[Callable[[KeyEvent], None]] = None

    def on_key(self, key: str) -> Callable:
        """Decorator to register a key handler"""

        def decorator(func: Callable[[KeyEvent], None]):
            self.handlers[key] = func
            return func

        return decorator

    def on_text(self, func: Callable[[KeyEvent], None]) -> Callable:
        """Decorator to register a text input handler"""
        self.text_handler = func
        return func

    def handle_key(self, event: KeyEvent) -> None:
        """Handle a key event if a handler exists"""
        # First check if it's a single character that has a specific handler
        if event.key == "text" and event.char in self.handlers:
            self.handlers[event.char](KeyEvent(key=event.char))
        # Then check other key handlers
        elif event.key in self.handlers:
            self.handlers[event.key](event)
        # Finally, treat it as text input
        elif event.key == "text" and self.text_handler:
            self.text_handler(event)

    def _handle_special_key(self, key: str) -> KeyEvent:
        """Handle special keys like arrows"""
        key_mapping = {"A": "up", "B": "down", "C": "right", "D": "left"}
        return KeyEvent(key=key_mapping.get(key, key))

    def get_key(self, timeout=0.1) -> Optional[KeyEvent]:
        """Get a single keypress with timeout"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ready, _, _ = select.select([sys.stdin], [], [], timeout)
            if ready:
                char = sys.stdin.read(1)
                if char == "\x1b":  # ESC sequence
                    char = sys.stdin.read(1)
                    if char == "[":
                        key = sys.stdin.read(1)
                        return self._handle_special_key(key)
                    return KeyEvent(key="esc")
                elif char == "\x7f":  # Backspace
                    return KeyEvent(key="backspace")
                elif ord(char) < 32:  # Control characters
                    return KeyEvent(key=chr(ord(char) + 64), ctrl=True)
                else:  # Regular text input
                    return KeyEvent(key="text", char=char)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return None
