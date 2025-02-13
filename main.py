import time

from drawing.render import RenderContext
from src.core.color import ColorManager
from src.core.screen_buffer import ScreenBuffer
from src.core.term import TerminalController
from src.drawing.complex_shapes import ComplexShapes
from src.drawing.drawing_interface import DrawingInterface
from src.drawing.primitives import DrawingPrimitives
from src.ui.window import Window
from ui.text import Text


class TerminalUI:
    def __init__(self):
        self.terminal: TerminalController = TerminalController()

        # Initialize global render context
        self.context: RenderContext = RenderContext()
        self.color_manager: ColorManager = self.context.get_color_manager()
        self.context.initialize(*self.terminal.get_size())

        # Get global resources
        resources = self.context.get_resources()
        self.screen_buffer: ScreenBuffer = resources.screen_buffer
        self.primitives: DrawingPrimitives = resources.primitives
        self.shapes: ComplexShapes = resources.shapes
        self.draw: DrawingInterface = resources.draw

        self.draw: DrawingInterface = DrawingInterface(
            self.screen_buffer, self.color_manager
        )

        # Create root window
        self.root_window = Window(
            "root",
            0, 0, self.screen_buffer.width, self.screen_buffer.height
        )

        # Use main screen buffer for root window
        self.root_window.buffer = self.screen_buffer
        self.root_window.primitives = self.primitives
        self.root_window.shapes = self.shapes

        self.windows: dict[str, Window] = {}
        self.first_render = True

        # Define which object handles which methods
        self._delegates = {
            "draw_at": self.primitives,
            "draw_string": self.primitives,
            "draw_rectangle": self.shapes,
            "draw_line": self.shapes,
        }

    def __getattr__(self, name):
        """Automatically delegate method calls to appropriate internal objects"""
        if name in self._delegates:
            return getattr(self._delegates[name], name)
        raise AttributeError(f"'TerminalUI' has no attribute '{name}'")

    def __enter__(self) -> None:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.terminal._restore_cursor()
        self.terminal._show_cursor()
        self.terminal._use_main_screen()
        if exc_type is KeyboardInterrupt:
            print("\nGoodbye!")
            return True  # Suppress the KeyboardInterrupt

    def create_window(
        self, name: str, x: int, y: int, width: int, height: int, title: str = ""
    ) -> Window:
        """Create a new window with given dimensions"""
        window = Window(name, x, y, width, height, title)
        self.windows[name] = window
        return window

    def create_horizontal_split(
        self, names: list[str], ratios: list[float] = None
    ) -> list[Window]:
        """Create horizontally split windows with optional width ratios"""
        if ratios is None:
            ratios = [1 / len(names)] * len(names)

        total_width = self.screen_buffer.width
        current_x = 0
        windows = []

        for name, ratio in zip(names, ratios, strict=True):
            width = int(total_width * ratio)
            window = self.create_window(
                name, current_x, 0, width, self.screen_buffer.height
            )
            windows.append(window)
            current_x += width

        return windows

    def render(self):
        """Render only the changed parts of the screen"""
        if self.first_render:
            self.terminal.clear_screen()
            self.first_render = False

        # Clear main buffer
        # self.screen_buffer.clear()

        # Render each window to main buffer:
        for window in self.windows.values():
            window.render_to(self.screen_buffer)

        changes = self.screen_buffer.get_changes()

        for (y, x), _ in changes.items():
            # Move cursor to (x+1, y+1) since ANSI uses 1-based indexing
            print(
                f"\033[{y+1};{x+1}H{self.screen_buffer.get_char(x, y)}",
                end="",
                flush=True,
            )


if __name__ == "__main__":
    with TerminalUI() as tui:
        # Create a chess board window (60%) and eval window (40%)
        board_window, eval_window = tui.create_horizontal_split(
            ["board", "eval"], [0.6, 0.4]
        )
        style = {"fg": "#2a2a2a", "bg": "#FFFFFF"}

        # Draw using the drawing interface

        board_window.style(style)
        board_window.draw.rectangle(1, 1, 38, 18)
        board_window.add(Text("Chess board here", 2, 2).width(36))

        # Draw directly using window's drawing capabilities
        eval_window.style(style)
        eval_window.draw.rectangle(1, 1, 28, 18)
        eval_window.add(Text("Evaluation: +0.5", 2, 2).width(26))

        tui.render()
        while True:
            time.sleep(0.1)
