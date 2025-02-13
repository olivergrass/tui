from drawing.render import Renderable
from ui.component import Component, transform_coordinates
from ui.selectable import Selectable


class Input(Component, Renderable, Selectable):
    def __init__(self, x: int = 0, y: int = 0, width: int = 20):
        Component.__init__(self, x, y)
        Renderable.__init__(self)
        Selectable.__init__(self)
        self._width = width
        self._value = ""
        self._cursor_pos = 0
        self._keyboard = None  # Keyboard handler

    def set_keyboard_handler(self, keyboard_handler):
        """Set keyboard handler reference"""
        self._keyboard = keyboard_handler

    def on_focus_changed(self, focused: bool):
        """Register/unregister handlers when focus changes"""
        if not self._keyboard:
            return

        if focused:
            self._keyboard.on_text(self._handle_text)
            self._keyboard.on_key("backspace")(self._handle_backspace)
        else:
            self._keyboard.text_handler = None
            if "backspace" in self._keyboard.handlers:
                del self._keyboard.handlers["backspace"]

    def _handle_text(self, event):
        """Handle text input"""
        if len(self._value) < self._width and event.char.isprintable():
            # Insert at cursor position
            self._value = (
                self._value[: self._cursor_pos]
                + event.char
                + self._value[self._cursor_pos :]
            )
            self._cursor_pos += 1

    def _handle_backspace(self, event):
        """Handle backspace key"""
        if self._cursor_pos > 0:
            # Remove character before cursor
            self._value = (
                self._value[: self._cursor_pos - 1] + self._value[self._cursor_pos :]
            )
            self._cursor_pos -= 1

    @transform_coordinates
    def render_to(self, target_buffer):
        style = self.effective_style
        draw = self.resources.draw

        # Draw border
        draw.draw_rectangle( self.x - 1, self.y - 1, self._width, 3)

        # Draw input value with cursor
        display_text = (
            self._value[: self._cursor_pos]
            + ("█" if self.focused else " ")
            + self._value[self._cursor_pos :]
        )

        draw.draw_string(
            self.x,
            self.y,
            display_text[: self._width],  # Ensure we don't exceed width
            width=self._width,
            fg=style.fg,
            bg=style.bg,
        )
