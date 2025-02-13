from main import TerminalUI
import time
import math

from ui.text import Text


def main():
    with TerminalUI() as tui:
        # Create a window for our demo
        window = tui.create_window("demo", 2, 2, 60, 20, "Progress Bar Demo")

        # Define some test scenarios
        scenarios = [
            ("Default", "default", "#00FF00", "#333333"),
            ("Blocks", "blocks", "#5555FF", "#222222"),
            ("Dots", "dots", "#FF5555", "#222222"),
            ("Lines", "lines", "#FFFF55", "#222222"),
            ("Rainbow", "default", None, "#222222"),  # Color will be dynamic
        ]

        start_time = time.time()

        # Draw title
        window.add(Text("Progress Bar Styles Demo", 2, 1).align("center"))
        window.add(Text("=" * len("Progress Bar Styles Demo"), 2, 2,).align("center"))
        window.add(Text("Press Ctrl+C to exit", 2, window.height - 2).align("center"))
        while True:
            t = time.time() - start_time

            # Clear window
            # window.buffer.clear()


            # Draw each progress bar style
            for i, (name, style, color, bg_color) in enumerate(scenarios):
                y_pos = i * 3 + 4

                # Calculate progress based on time
                progress = (math.sin(t + i) + 1) / 2

                # For rainbow style, calculate dynamic color
                if color is None:
                    hue = (t * 0.2 + i * 0.2) % 1.0
                    color = tui.color_manager.hsv_to_hex(hue, 1.0, 1.0)

                # Draw label
                window.draw.string(2, y_pos, f"{name}:")

                # Draw progress bar
                window.draw.progress_bar(
                    15,
                    y_pos,
                    40,
                    progress,
                    style=style,
                    fg_color=color,
                    bg_color=bg_color,
                )


            tui.render()
            time.sleep(0.03)


if __name__ == "__main__":
    main()
