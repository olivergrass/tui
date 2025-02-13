class DrawingPrimitives:
    def __init__(self, screen_buffer, color_manager):
        self.screen_buffer = screen_buffer
        self.color_manager = color_manager
        self.width = screen_buffer.width
        self.height = screen_buffer.height

    def draw_char(self, x: int, y: int, char: str, fg: str = None, bg: str = None):
        """Draw a character with optional foreground and background colors."""
        if 0 <= x < self.width and 0 <= y < self.height:
            formatted_char = char
            if fg or bg:
                color_codes = self.color_manager.format_color_codes(fg, bg)
                formatted_char = f"{color_codes}{char}\033[0m"

            self.screen_buffer.set_char(x, y, formatted_char)

    def draw_string(
        self,
        x: int,
        y: int,
        text: str,
        width: int = None,
        align: str = "left",
        fg: str = None,
        bg: str = None,
    ):
        """
        Draw a string with alignment options and colors.

        Args:
            x (int): Starting x coordinate
            y (int): Starting y coordinate
            text (str): Text to draw
            width (int): Width of the text field. If None, uses remaining screen width
            align (str): Alignment option - "left", "right", "center"
            fg (str): Foreground color in hex format (e.g. "#FFFFFF")
            bg (str): Background color in hex format (e.g. "#000000")
        """
        text = str(text)  # Convert to string to handle numbers

        # If no width specified, use text length
        if width is None:
            width = len(text)

        # Calculate starting position based on alignment
        if align == "right":
            start_x = x + width - len(text)
        elif align == "center":
            start_x = x + (width - len(text)) // 2
        else:  # left alignment
            start_x = x

        # Ensure we don't start before the specified x position
        start_x = max(x, start_x)

        # Draw the text
        current_x = x
        for i in range(width):
            if current_x >= self.width:
                break

            # Calculate if we're in the text region
            text_pos = i - (start_x - x)

            if 0 <= text_pos < len(text):
                # We're in the text region
                self.draw_char(current_x, y, text[text_pos], fg, bg)
            else:
                # We're in the padding region
                self.draw_char(current_x, y, " ", fg, bg)

            current_x += 1

    def draw_at(self, x: int, y: int, char: str, color: str = "#FFFFFF"):
        """Draw a character at a specific screen coordinate."""
        if 0 <= x < self.width and 0 <= y < self.height:
            if len(str(char)) > 1:  # If we got a string instead of a single char
                self.draw_string(x, y, char, color=color)
            else:
                new_char = (
                    self.color_manager.coloured_square(color) if char == " " else char
                )
                self.screen_buffer.set_char(x, y, new_char)
