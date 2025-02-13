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


class KeyboardHandler:
    def __init__(self) -> None:
        self.handlers: dict[str, Callable[[KeyEvent], None]] = {}

    def on_key(self, key: str) -> Callable:
        """Decorator to register a key handler"""
        def decorator(func: Callable[[KeyEvent], None]):
            self.handlers[key] = func
            return func
        return decorator

    def handle_key(self, event: KeyEvent) -> None:
        """Handle a key event if a handler exists"""
        if event.key in self.handlers:
            self.handlers[event.key](event)

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
                    next_char = (
                        sys.stdin.read(1)
                        if select.select([sys.stdin], [], [], 0.1)[0]
                        else None
                    )
                    if next_char == "[":
                        key = sys.stdin.read(1)
                        return self._handle_special_key(key)
                    return KeyEvent(key="esc")
                elif ord(char) < 32:  # Control characters
                    return KeyEvent(key=chr(ord(char) + 64), ctrl=True)
                return KeyEvent(key=char)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return None
