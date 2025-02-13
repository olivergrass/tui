from typing import Optional, Dict
from dataclasses import dataclass

from core.color import ColorManager
from core.screen_buffer import ScreenBuffer
from drawing.complex_shapes import ComplexShapes
from drawing.drawing_interface import DrawingInterface
from drawing.primitives import DrawingPrimitives


@dataclass
class RenderResources:
    """Bundle of rendering resources for a specific context"""

    screen_buffer: ScreenBuffer
    primitives: DrawingPrimitives
    shapes: ComplexShapes
    draw: DrawingInterface
    color_manager: ColorManager


class RenderContext:
    _instance = None
    _color_manager = None # Class-level singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RenderContext, cls).__new__(cls)
            cls._instance._initialized = False
            cls._color_manager = ColorManager()
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._global_resources: Optional[RenderResources] = None
            self._local_resources: Dict[str, RenderResources] = {}
            self._initialized = True

    @classmethod
    def get_color_manager(cls) -> ColorManager:
        """Get the singleton ColorManager instance"""
        if cls._color_manager is None:
            cls._color_manager = ColorManager()
        return cls._color_manager

    def initialize(self, width: int, height: int):
        """Initialize the global rendering context"""
        screen_buffer = ScreenBuffer(width, height)
        primitives = DrawingPrimitives(screen_buffer, self._color_manager)
        shapes = ComplexShapes(primitives)
        draw = DrawingInterface(screen_buffer, self._color_manager)

        self._global_resources = RenderResources(
            screen_buffer=screen_buffer,
            primitives=primitives,
            shapes=shapes,
            draw=draw,
            color_manager=self._color_manager,
        )

    def create_local_context(
        self, name: str, width: int, height: int
    ) -> RenderResources:
        """Create a new local rendering context (e.g., for a window)"""
        screen_buffer = ScreenBuffer(width, height)
        primitives = DrawingPrimitives(screen_buffer, self._color_manager)
        shapes = ComplexShapes(primitives)
        draw = DrawingInterface(screen_buffer, self._color_manager)

        resources = RenderResources(
            screen_buffer=screen_buffer,
            primitives=primitives,
            shapes=shapes,
            draw=draw,
            color_manager=self._color_manager,
        )

        self._local_resources[name] = resources
        return resources

    def get_resources(self, context_name: Optional[str] = None) -> RenderResources:
        """Get resources for either global or local context"""
        if context_name is None:
            if not self._global_resources:
                raise RuntimeError("Global RenderContext not initialized")
            return self._global_resources

        if context_name not in self._local_resources:
            raise KeyError(f"No local context found for '{context_name}'")
        return self._local_resources[context_name]


class Renderable:
    """Mixin class for objects that need access to rendering resources"""

    def __init__(self, context_name: Optional[str] = None):
        self._context_name = context_name

    @property
    def context(self) -> RenderContext:
        return RenderContext()

    @property
    def resources(self) -> RenderResources:
        return self.context.get_resources(self._context_name)
