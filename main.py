from core.focus import FocusManager
from core.keyboard import KeyboardHandler
from drawing.render import RenderContext
from src.core.color import ColorManager
from src.core.screen_buffer import ScreenBuffer
from src.core.term import TerminalController
from src.drawing.complex_shapes import ComplexShapes
from src.drawing.drawing_interface import DrawingInterface
from src.drawing.primitives import DrawingPrimitives
from src.ui.window import Window
from ui.container import Container
from ui.input import Input
from ui.text import Text


class TerminalUI:
    def __init__(self):
        self.terminal: TerminalController = TerminalController()
        self.keyboard = KeyboardHandler()
        self.quit = False

        self.focus_manager = FocusManager()

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
            "root", 0, 0, self.screen_buffer.width, self.screen_buffer.height
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
            self.quit = True
            print("\nGoodbye!")
            return True  # Suppress the KeyboardInterrupt

    def run(self):
        """Main event loop"""
        while not self.quit:
            self.render()

            key_event = self.keyboard.get_key()
            if key_event:
                self.keyboard.handle_key(key_event)

    def stop(self):
        """Stop the main loop"""
        self.quit = True

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
        tui.focus_manager.register(board_window)
        tui.focus_manager.register(eval_window)

        # Register keyboard handlers
        @tui.keyboard.on_key("up")
        def handle_focus(event):
            tui.focus_manager.focus_next()

        @tui.keyboard.on_key("q")
        def handle_quit(event):
            tui.stop()

        style = {"fg": "#2a2a2a", "bg": "#FFFFFF"}

        # container = Container(1, 1, 38, 18).style(style)
        # container.add(Text("Chess board here", 2, 2).width(36))
        # board_window.add(container)
        board_window.title = "Board"

        # eval_window.style(style)
        # eval_window.draw.rectangle(1, 1, 28, 18)
        eval_window.add(Text("Evaluation: +0.5", 2, 2).width(26))

        input_field: Input = Input(2, 4, width=24)
        input_field.set_keyboard_handler(tui.keyboard)
        eval_window.add(input_field)
        tui.focus_manager.register(input_field)

        tui.run()
