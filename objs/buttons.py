from typing import Any
from collections.abc import Callable


class MenuSelect:
    def __init__(self: "MenuSelect",
                 message: str,
                 func: Callable[[], bool],
                 selected: bool =False) -> None:
        self.message: str = message
        self.func: Callable[[], bool] = func
        self.selected: bool = selected

    def get_message(self: "MenuSelect") -> str:
        return (self.message)

    def is_selected(self: "MenuSelect") -> bool:
        return (self.selected)

    def press(self: "MenuSelect") -> bool:
        return (self.func())

    def select(self: "MenuSelect") -> None:
        self.selected = True

    def unselect(self: "MenuSelect") -> None:
        self.selected = False
