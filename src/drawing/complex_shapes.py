from .primitives import DrawingPrimitives


class ComplexShapes:
    def __init__(self, primitives: DrawingPrimitives):
        self.primitives = primitives
        self.width = primitives.width
        self.height = primitives.height

    def draw_rectangle(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        fill: str = " ",
        color: str = "#FFFFFF",
        border: bool = True,
    ):
        """Draw a rectangle with optional border and fill."""
        # Draw fill
        for dy in range(height):
            for dx in range(width):
                self.primitives.draw_at(x + dx, y + dy, fill, color)

        # Draw border if requested
        if border:
            self._draw_border(x, y, width, height)

    def _draw_border(self, x: int, y: int, width: int, height: int):
        """Helper method to draw box borders using Unicode characters."""
        BOX = {
            "top_left": "┌",
            "top_right": "┐",
            "bottom_left": "└",
            "bottom_right": "┘",
            "horizontal": "─",
            "vertical": "│",
        }

        # Draw corners
        self.primitives.draw_char(x, y, BOX["top_left"])
        self.primitives.draw_char(x + width - 1, y, BOX["top_right"])
        self.primitives.draw_char(x, y + height - 1, BOX["bottom_left"])
        self.primitives.draw_char(x + width - 1, y + height - 1, BOX["bottom_right"])

        # Draw edges
        for dx in range(1, width - 1):
            self.primitives.draw_char(x + dx, y, BOX["horizontal"])
            self.primitives.draw_char(x + dx, y + height - 1, BOX["horizontal"])
        for dy in range(1, height - 1):
            self.primitives.draw_char(x, y + dy, BOX["vertical"])
            self.primitives.draw_char(x + width - 1, y + dy, BOX["vertical"])

    def draw_matrix(
        self,
        x: int,
        y: int,
        matrix: list,
        cell_width: int = 3,
        cell_height: int = 3,
        show_borders: bool = False,
        colors: list = None,
    ):
        """Draw a 2D matrix as a grid/board with borders between cells."""
        if not matrix:
            return

        rows, cols = len(matrix), len(matrix[0])

        # Draw cells
        for row in range(rows):
            for col in range(cols):
                # Calculate cell position accounting for grid lines
                cell_x = x + col * cell_width
                cell_y = y + row * cell_height

                # Get cell color
                color = colors[row][col] if colors and colors[row][col] else "#FFFFFF"

                # Draw cell (without borders)
                self.draw_rectangle(
                    cell_x,
                    cell_y,
                    cell_width,
                    cell_height,
                    fill=" ",
                    color=color,
                    border=False,
                )

                # Draw cell value
                if matrix[row][col]:
                    value = str(matrix[row][col])
                    center_x = cell_x + (cell_width - len(value)) // 2
                    center_y = cell_y + cell_height // 2
                    self.primitives.draw_string(center_x, center_y, value)

    def draw_table(self, x: int, y: int, headers: list, data: list, col_widths: list = None):
        """Draw a formatted table with headers and data."""
        if not col_widths:
            col_widths = [
                max(len(str(row[i])) for row in [headers] + data) + 2
                for i in range(len(headers))
            ]

        # Draw headers
        current_x = x
        for header, width in zip(headers, col_widths, strict=True):
            self.primitives.draw_string(
                current_x, y, header, width=width, align="center"
            )
            current_x += width + 1

        # Draw separator
        self.primitives.draw_string(
            x, y + 1, "─" * sum(col_widths + [len(col_widths) - 1])
        )

        # Draw data
        for row_idx, row in enumerate(data):
            current_x = x
            for cell, width in zip(row, col_widths, strict=True):
                self.primitives.draw_string(
                    current_x, y + row_idx + 2, str(cell), width=width, align="left"
                )
                current_x += width + 1

    def draw_progress_bar(
        self,
        x: int,
        y: int,
        width: int,
        progress: float,
        style: str = "default",
        fg_color: str = "#00FF00",
        bg_color: str = "#333333",
        show_percentage: bool = True,
    ):
        """
        Draw a progress bar with various styles.

        Args:
            x, y: Starting position
            width: Total width of the progress bar
            progress: Value between 0.0 and 1.0
            style: "default", "blocks", "dots", or "lines"
            fg_color: Color of the filled portion
            bg_color: Color of the unfilled portion
            show_percentage: Whether to show percentage in the middle
        """
        # Clamp progress between 0 and 1
        progress = max(0.0, min(1.0, progress))

        # Calculate filled width
        filled_width = int(progress * (width - 2))  # -2 for borders

        # Define style characters
        STYLES = {
            "default": ("█", "░"),
            "blocks": ("▰", "▱"),
            "dots": ("⣿", "⣀"),
            "lines": ("━", "─"),
        }
        fill_char, empty_char = STYLES.get(style, STYLES["default"])

        # Draw border and background
        self.primitives.draw_char(x, y, "⟨")
        self.primitives.draw_char(x + width - 1, y, "⟩")

        # Draw the filled portion
        for i in range(filled_width):
            self.primitives.draw_char(x + 1 + i, y, fill_char, fg=fg_color)

        # Draw the empty portion
        for i in range(filled_width, width - 2):
            self.primitives.draw_char(x + 1 + i, y, empty_char, fg=bg_color)

        # Draw percentage if requested
        if show_percentage:
            percentage = f" {int(progress * 100)}% "
            text_pos = x + (width - len(percentage)) // 2
            self.primitives.draw_string(text_pos, y, percentage)
