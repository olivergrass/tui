from .primitives import DrawingPrimitives
from .complex_shapes import ComplexShapes


class DrawingInterface:
    """Unified interface for all drawing operations"""

    def __init__(self, screen_buffer, color_manager):
        self.primitives = DrawingPrimitives(screen_buffer, color_manager)
        self.shapes = ComplexShapes(self.primitives)

        # Directly expose all methods from both classes
        self._delegates = {
            # Primitives
            "draw_char": self.primitives,
            "draw_string": self.primitives,
            "draw_at": self.primitives,
            # Complex shapes
            "draw_rectangle": self.shapes,
            "draw_matrix": self.shapes,
            "draw_table": self.shapes,
            "draw_progress_bar": self.shapes,
        }

    def __getattr__(self, name):
        """Automatically delegate to appropriate drawing class"""
        if name in self._delegates:
            return getattr(self._delegates[name], name)
        # Try with draw_ prefix
        if f"draw_{name}" in self._delegates:
            return getattr(self._delegates[f"draw_{name}"], f"draw_{name}")
        raise AttributeError(f"No drawing method '{name}' found")
