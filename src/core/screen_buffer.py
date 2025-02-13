class ScreenBuffer:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.buffer = [[" " for _ in range(width)] for _ in range(height)]
        self.changes = {}

    def set_char(self, x: int, y: int, char: str):
        """Set a character in the buffer and track the change."""
        if self.buffer[y][x] != char:
            self.buffer[y][x] = char
            self.changes[(y, x)] = char

    def clear(self):
        """Clear the screen buffer."""
        self.buffer = [[" " for _ in range(self.width)] for _ in range(self.height)]
        self.changes.clear()

    def get_char(self, x: int, y: int) -> str:
        """Get character at specified position."""
        return self.buffer[y][x]

    def get_changes(self) -> dict:
        """Get current changes and clear the change tracking."""
        changes = self.changes.copy()
        self.changes.clear()
        return changes
