from core.screen_buffer import ScreenBuffer
from drawing.render import Renderable
from ui.component import Component, transform_coordinates


class Text(Component, Renderable):
    def __init__(self, content: str, x: int = 0, y: int = 0):
        Component.__init__(self, x, y)
        Renderable.__init__(self)
        self.content = str(content)

    def handle_text_input(self, text: str) -> bool:
        """Handle text input when focused"""
        if not self.focused:
            return False

        if text.isprintable() and len(self._value) < self._width:
            self._value += text
            self._cursor_pos += 1
            return True
        return False

    @transform_coordinates
    def render_to(self, target_buffer: ScreenBuffer) -> None:
        style = self.effective_style
        self.resources.primitives.draw_string(
            self.x,
            self.y,
            self.content,
            width=style.width,
            align=style.align,
            fg=style.fg,
            bg=style.bg,
        )
