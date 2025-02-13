from abc import ABC
from dataclasses import dataclass


@dataclass
class SelectionStyle:
    border_fg: str = "#00FF00"
    border_bg: str = None


class Selectable(ABC):
    """Component that can receive focus"""

    def __init__(self):
        self._focused = False
        self._selection_style = SelectionStyle()

    @property
    def focused(self) -> bool:
        return self._focused

    @focused.setter
    def focused(self, value: bool):
        if self._focused != value:
            self._focused = value
            self.on_focus_changed(value)

    def on_focus_changed(self, focused: bool):  # noqa: B027
        """Called when focus state changes"""
        pass
