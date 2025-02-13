import os


class TerminalController:
    def __init__(self) -> None:
        self._hide_cursor()
        self._save_cursor()
        self._use_alternate_screen()

    def __del__(self):
        self._show_cursor()
        self._restore_cursor()
        # self._use_main_screen()
        # pass

    def _hide_cursor(self):
        """Hide the terminal cursor."""
        print("\033[?25l", end="", flush=True)

    def _show_cursor(self):
        """Show the terminal cursor."""
        print("\033[?25h", end="", flush=True)

    def _save_cursor(self):
        """Save cursor position."""
        print("\033[s", end="", flush=True)

    def _restore_cursor(self):
        """Restore cursor position."""
        print("\033[u", end="", flush=True)

    def _use_alternate_screen(self):
        """Switch to alternate screen buffer."""
        print("\033[?1049h", end="", flush=True)

    def _use_main_screen(self):
        """Switch back to main screen buffer."""
        print("\033[?1049l", end="", flush=True)

    def get_size(self):
        """Get the terminal size (columns, rows)."""
        rows, columns = os.popen("stty size", "r").read().split()
        return int(columns), int(rows)

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")
