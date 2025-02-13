from dataclasses import dataclass


@dataclass
class KeyEvent:
    key: str
    ctrl: bool = False
    alt: bool = False


