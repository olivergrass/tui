from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Optional, TypeVar

from core.screen_buffer import ScreenBuffer


@dataclass
class Style:
    fg: Optional[str] = None
    bg: Optional[str] = None
    align: str = "left"
    width: Optional[str] = None

    def merge(self, other: "Style") -> "Style":
        """Merge two styles, with other taking precedence."""
        return Style(
            fg=other.fg if other.fg is not None else self.fg,
            bg=other.bg if other.bg is not None else self.bg,
            align=other.align if other.align != "left" else self.align,
            width=other.width if other.width is not None else self.width,
        )


class Component(ABC):
    def __init__(self, x: int = 0, y: int = 0):
        self._style = Style()
        self._parent = None
        self.x = x
        self.y = y

    @property
    def absolute_position(self) -> tuple[int, int]:
        """Get absolute coordinates by combining with parent positions"""
        if not self._parent:
            return (self.x, self.y)
        parent_x, parent_y = self._parent.absolute_position
        return (parent_x + self.x, parent_y + self.y)

    def get_absolute_coords(self, rel_x: int, rel_y: int) -> tuple[int, int]:
        """Convert component-relative coordinates to absolute screen coordinates"""
        abs_x, abs_y = self.absolute_position
        return (abs_x + rel_x, abs_y + rel_y)

    @property
    def effective_style(self) -> Style:
        """Get the effective style including inherited styles."""
        if not self._parent:
            return self._style
        return self._parent.effective_style.merge(self._style)

    def style(self, options: dict[str, Any]) -> "Component":
        """Apply styling options."""
        for key, value in options.items():
            if hasattr(self._style, key):
                setattr(self._style, key, value)
        return self

    def align(self, alignment: str) -> "Component":
        self._style.align = alignment
        return self

    def fg(self, color: str) -> "Component":
        self._style.fg = color
        return self

    def bg(self, color: str) -> "Component":
        self._style.bg = color
        return self

    def width(self, width: int) -> "Component":
        self._style.width = width
        return self

    @abstractmethod
    def render_to(self, target_buffer: ScreenBuffer) -> None:
        pass


T = TypeVar('T')

def transform_coordinates(render_method: Callable[..., T]) -> Callable[..., T]:
    """Decorator that transforms relative coordinates to absolute before rendering"""
    @wraps(render_method)
    def wrapper(self: Component, target_buffer: ScreenBuffer, *args, **kwargs):
        # Store original coordinates
        original_x, original_y = self.x, self.y

        # Calculate and set absolute position
        if self._parent:
            parent_x, parent_y = self._parent.absolute_position
            self.x += parent_x
            self.y += parent_y

        try:
            # Execute the render method with transformed coordinates
            return render_method(self, target_buffer, *args, **kwargs)
        finally:
            # Restore original relative coordinates
            self.x, self.y = original_x, original_y

    return wrapper
