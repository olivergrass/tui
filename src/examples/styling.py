import time

from main import TerminalUI
from ui.container import Container
from ui.text import Text
from ui.window import Window


def main():
    with TerminalUI() as tui:
        window: Window = tui.create_window("main", 0, 0, 80, 24)
        window.bg("#00FF00")

        container = Container(5, 5, 30, 10)
        container.bg("#333333")

        text = Text("Hello, World!").style({"fg": "#FF0000"})
        container.add(text)

        window.draw.draw_rectangle(0, 0, 20, 20)
        window.add(container)

        while True:
            tui.render()
            time.sleep(0.1)

if __name__ == "__main__":
    main()
