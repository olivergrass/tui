import os


class ColorManager:
    def __init__(self):
        self.color_mode = self._detect_terminal_color_mode()

    def coloured_square(self, hex_string: str) -> str:
        """Returns a coloured square that you can print to a terminal."""
        hex_string = hex_string.strip("#")
        assert len(hex_string) == 6
        red = int(hex_string[:2], 16)
        green = int(hex_string[2:4], 16)
        blue = int(hex_string[4:6], 16)

        if self.color_mode == "truecolor":
            return f"\033[48:2::{red}:{green}:{blue}m \033[49m"
        elif self.color_mode == "256":
            closest_256 = self._rgb_to_256(red, green, blue)
            return f"\033[48;5;{closest_256}m \033[49m"
        else:
            basic_colors = {
                "00": 0,  # Black
                "ff": 1,  # Red
                "00ff00": 2,  # Green
                "ffff00": 3,  # Yellow
                "0000ff": 4,  # Blue
                "ff00ff": 5,  # Magenta
                "00ffff": 6,  # Cyan
                "ffffff": 7,  # White
            }
            hex_value = f"{red:02x}{green:02x}{blue:02x}"
            closest_basic = min(
                basic_colors, key=lambda x: abs(int(hex_value, 16) - int(x, 16))
            )
            return f"\033[48;5;{basic_colors[closest_basic]}m \033[49m"

    def _rgb_to_256(self, red, green, blue):
        """Map RGB to the 256-color palette."""
        return (
            int(round((red / 255) * 5)) * 36
            + int(round((green / 255) * 5)) * 6
            + int(round((blue / 255) * 5))
        )

    def _detect_terminal_color_mode(self) -> str:
        """Detects the color mode of the terminal."""
        term = os.environ.get("TERM", "").lower()
        colorterm = os.environ.get("COLORTERM", "").lower()
        if "truecolor" in colorterm or "24bit" in term:
            return "truecolor"
        elif "256" in term:
            return "256"
        else:
            return "basic"

    def format_color_codes(self, fg: str = None, bg: str = None) -> str:
        """Create ANSI color codes for foreground and background colors."""
        codes = []

        if fg:
            fg = fg.strip("#")
            r, g, b = int(fg[:2], 16), int(fg[2:4], 16), int(fg[4:], 16)
            if self.color_mode == "truecolor":
                codes.append(f"\033[38;2;{r};{g};{b}m")
            elif self.color_mode == "256":
                color_256 = self._rgb_to_256(r, g, b)
                codes.append(f"\033[38;5;{color_256}m")

        if bg:
            bg = bg.strip("#")
            r, g, b = int(bg[:2], 16), int(bg[2:4], 16), int(bg[4:], 16)
            if self.color_mode == "truecolor":
                codes.append(f"\033[48;2;{r};{g};{b}m")
            elif self.color_mode == "256":
                color_256 = self._rgb_to_256(r, g, b)
                codes.append(f"\033[48;5;{color_256}m")

        return "".join(codes)

    def hsv_to_hex(self, h: float, s: float, v: float) -> str:
        """
        Convert HSV color values to hex string.

        Args:
            h: Hue (0.0 to 1.0)
            s: Saturation (0.0 to 1.0)
            v: Value (0.0 to 1.0)

        Returns:
            Hex color string (e.g., "#FF0000")
        """
        r, g, b = self.hsv_to_rgb(h, s, v)
        return f"#{r:02x}{g:02x}{b:02x}"

    def hsv_to_rgb(self, h: float, s: float, v: float) -> tuple[int, int, int]:
        """
        Convert HSV color values to RGB.

        Args:
            h: Hue (0.0 to 1.0)
            s: Saturation (0.0 to 1.0)
            v: Value (0.0 to 1.0)

        Returns:
            Tuple of (r, g, b) values (0-255)
        """
        if s == 0.0:
            rgb = (v, v, v)
        else:
            i = int(h * 6.0)
            f = (h * 6.0) - i
            p = v * (1.0 - s)
            q = v * (1.0 - s * f)
            t = v * (1.0 - s * (1.0 - f))
            i = i % 6

            if i == 0:
                rgb = (v, t, p)
            elif i == 1:
                rgb = (q, v, p)
            elif i == 2:
                rgb = (p, v, t)
            elif i == 3:
                rgb = (p, q, v)
            elif i == 4:
                rgb = (t, p, v)
            else:
                rgb = (v, p, q)

        # Convert to 0-255 range
        return tuple(int(x * 255) for x in rgb)
