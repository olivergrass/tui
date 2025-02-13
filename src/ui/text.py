from core.color import ColorManager
from core.screen_buffer import ScreenBuffer
from drawing.primitives import DrawingPrimitives
from ui.component import Component, transform_coordinates


class Text(Component):
    def __init__(self, content: str, x: int = 0, y: int = 0):
        super().__init__(x, y)
        self.content = str(content)

    @transform_coordinates
    def render_to(self, target_buffer: ScreenBuffer) -> None:
        style = self.effective_style
        color_manager = ColorManager()
        primitives = DrawingPrimitives(target_buffer, color_manager)
        primitives.draw_string(
            self.x,
            self.y,
            self.content,
            width=style.width,
            align=style.align,
            fg=style.fg,
            bg=style.bg,
        )
