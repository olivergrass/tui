from core.screen_buffer import ScreenBuffer
from drawing.render import RenderResources, Renderable
from ui.component import Component, transform_coordinates


class Container(Component, Renderable):
    def __init__(self, x: int = 0, y: int = 0, width: int = None, height: int = None):
        Component.__init__(self, x, y)
        # Don't initialize Renderable with a context_name - we'll get it from parent
        Renderable.__init__(self)

        self._width = width
        self._height = height
        self.children: list[Component] = []

        if width is not None:
            super().width(width)

    def add(self, child: Component) -> Component:
        """Add a child element that will inherit styles"""
        child._parent = self
        self.children.append(child)
        return child

    @property
    def resources(self) -> RenderResources:
        """Get resources from parent's context"""
        if not self._parent:
            raise RuntimeError("Container must be added to a parent before use")
        return self._parent.resources

    @transform_coordinates
    def render_to(self, target_buffer: ScreenBuffer) -> None:
        """Render container and its children"""
        style = self.effective_style

        # If we have dimensions and a background color, fill the container
        if self._width and self._height and style.bg:
            self.resources.shapes.draw_rectangle(
                self.x,
                self.y,
                self._width,
                self._height,
                fill=" ",
                color=style.bg,
                border=False,
            )

        # Render all children
        for child in self.children:
            child.render_to(target_buffer)
