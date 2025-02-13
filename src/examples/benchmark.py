from main import TerminalUI
import time

from ui.text import Text


class BenchmarkUI(TerminalUI):
    def _rainbow_pattern(self, t: float) -> str:
        import math

        """Generate a rainbow color based on time and position."""
        return "#{:02x}{:02x}{:02x}".format(
            int(127 + 127 * (math.sin(t))),
            int(127 + 127 * (math.sin(t + 2.094))),
            int(127 + 127 * (math.sin(t + 4.188))),
        )

    def stress_test(self, duration=10):
        """Run an intensive stress test with rapidly changing colors."""
        import math

        start_time = time.time()
        frame_count = 0

        while time.time() - start_time < duration:
            t = time.time() * 5  # Speed multiplier
            screen_height = self.screen_buffer.height
            screen_width = self.screen_buffer.width

            # Create a plasma-like effect
            for y in range(screen_height):
                for x in range(screen_width):
                    # Calculate dynamic color based on position and time
                    color = self._rainbow_pattern(
                        t
                        + math.sin(x * 0.1)
                        + math.cos(y * 0.1)
                        + math.sin(
                            math.sqrt(
                                (x - screen_width / 2) ** 2
                                + (y - screen_height / 2) ** 2
                            )
                            * 0.1
                        )
                    )
                    self.draw_at(x, y, " ", color)

            frame_count += 1

        elapsed = time.time() - start_time
        fps = frame_count / elapsed
        return {
            "time": elapsed,
            "frames": frame_count,
            "fps": fps,
            "pixels_per_frame": screen_width * screen_height,
        }

    def benchmark(self, iterations=1000):
        """
        Comprehensive benchmark testing different drawing patterns.
        Returns detailed metrics for each pattern.
        """
        patterns = {
            "single_point": lambda: self.draw_at(0, 0, "X"),
            "diagonal_line": lambda: [self.draw_at(i, i, "X") for i in range(5)],
            "horizontal_line": lambda: [self.draw_at(i, 0, "X") for i in range(5)],
            "vertical_line": lambda: [self.draw_at(0, i, "X") for i in range(5)],
            "color_blocks": lambda: [
                self.draw_at(i, 0, " ", f"#{c}0000")
                for i, c in enumerate(["FF", "CC", "99", "66", "33"])
            ],
            "checkerboard": lambda: [
                self.draw_at(x, y, " ", "#FF0000" if (x + y) % 2 == 0 else "#000000")
                for x in range(5)
                for y in range(5)
            ],
            "stress_test": lambda: self.stress_test(duration=0.0001),
        }

        results = {}

        for pattern_name, pattern_func in patterns.items():
            # Clear the screen before each test
            # self.terminal.clear_screen()
            self.render()

            # Time the pattern
            start_time = time.time()
            frames = 0

            # Run for at least 1 second to get meaningful FPS
            while time.time() - start_time < 0.5:
                for _ in range(min(iterations // 10, 100)):  # Batch size
                    pattern_func()
                    self.render()
                    frames += 1

            elapsed_time = time.time() - start_time
            fps = frames / elapsed_time

            results[pattern_name] = {"time": elapsed_time, "frames": frames, "fps": fps}

        return results


def main():
    with BenchmarkUI() as tui:
        # Run the benchmark
        results = tui.benchmark()

        # Clear screen before showing results
        tui.terminal.clear_screen()

        width = tui.screen_buffer.width

        # Draw title centered at top
        tui.draw_string(0, 0, "Benchmark Results", width=width, align="center")
        tui.draw_string(0, 1, "=" * width, align="left")

        headers = ["Pattern", "Time", "Frames", "FPS"]
        data = [
            [
                pattern_name,
                f"{metrics['time']:.3f}",
                str(metrics["frames"]),
                f"{metrics['fps']:.1f}",
            ]
            for pattern_name, metrics in results.items()
        ]

        # Draw the table with fixed column widths
        tui.draw.table(0, 3, headers, data)

        # Draw footer
        footer_y = len(data) + 5  # Position after table plus some spacing
        tui.draw_string(
            0,
            footer_y,
            "Press Ctrl+C to exit",
            width=width,
            align="center",
        )
        tui.render()

        while True:
            time.sleep(0.1)


if __name__ == "__main__":
    main()
