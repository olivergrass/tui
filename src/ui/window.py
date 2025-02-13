from drawing.render import Renderable
from src.drawing.complex_shapes import ComplexShapes
from src.drawing.drawing_interface import DrawingInterface
from src.drawing.primitives import DrawingPrimitives
from src.core.screen_buffer import ScreenBuffer
from src.ui.component import Component, transform_coordinates


class Window(Component, Renderable):
    def __init__(self, name, x: int, y: int, width: int, height: int, title: str = ""):
        Component.__init__(self, x, y)
        Renderable.__init__(self, context_name=name)

        self._height = height
        self._width = width
        self.title = title
        self.children: list[Component] = []

        # Initialize window's local rendering context
        self._resources = self.context.create_local_context(name, width, height)

        # Explicitly set all resources as instance attributes
        self.buffer = self._resources.screen_buffer
        self.primitives = self._resources.primitives
        self.shapes = self._resources.shapes
        self.draw = self._resources.draw

        super().width(width)

    def __getattr__(self, name):
        """Delegate drawing methods to window's primitives or shapes"""
        if hasattr(self.primitives, name):
            return getattr(self.primitives, name)
        if hasattr(self.shapes, name):
            return getattr(self.shapes, name)
        raise AttributeError(f"'Window' has no attribute '{name}'")

    def add(self, child: Component) -> Component:
        """Add a child element that will inherit styles"""
        child._parent = self
        print(child._parent)
        self.children.append(child)
        return child

    @transform_coordinates
    def render_to(self, target_buffer: ScreenBuffer):
        """Render window contents to the main screen buffer"""
        style = self.effective_style
        local_buffer = self._resources.screen_buffer

        # Copy local buffer contents to main buffer
        for y in range(self._height):
            for x in range(self._width):
                char = self.buffer.get_char(x, y)
                target_x, target_y = self.x + x, self.y + y

                if char and char.strip():  # Only copy non-empty and non-space chars
                    # Copy window buffer contents
                    target_buffer.set_char(target_x, target_y, char)
                elif style.bg is not None:
                    # Fill entire window area with background color
                    self.primitives.draw_char(
                        target_x, target_y, " ", bg=style.bg
                    )

        # Render all children
        for child in self.children:
            child.render_to(target_buffer)
