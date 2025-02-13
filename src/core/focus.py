from typing import Optional

from ui.selectable import Selectable


class FocusManager:
    """Manages focus state between selectable components"""

    def __init__(self):
        self.selectables: list[Selectable] = []
        self.current_index: Optional[int] = None

    def register(self, item: Selectable) -> None:
        self.selectables.append(item)
        if len(self.selectables) == 1:
            self.focus_next()

    def unregister(self, item: Selectable) -> None:
        if item in self.selectables:
            idx = self.selectables.index(item)
            self.selectables.pop(idx)
            if idx == self.current_index:
                self.current_index = None
                self.focus_next()

    def focus_next(self) -> None:
        if not self.selectables:
            return

        # Unfocus current
        if self.current_index is not None:
            self.selectables[self.current_index].focused = False

        # Focus next
        self.current_index = (
            0
            if self.current_index is None
            else (self.current_index + 1) % len(self.selectables)
        )
        self.selectables[self.current_index].focused = True

    def focus_previous(self) -> None:
        if not self.selectables:
            return

        # Unfocus current
        if self.current_index is not None:
            self.selectables[self.current_index].focused = False

        # Focus previous
        self.current_index = (
            len(self.selectables) - 1
            if self.current_index is None
            else (self.current_index - 1) % len(self.selectables)
        )
        self.selectables[self.current_index].focused = True
