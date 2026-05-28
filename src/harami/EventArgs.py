# SPDX-FileCopyrightText: © 2025 Shaun Wilson
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any


class EventArgs:

    empty: EventArgs
    args: tuple[Any, ...]
    kwargs: dict[str, Any]

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def get_by_name_or_index(self, name: str, index: int) -> Any:
        d = self.kwargs.get(name, None)
        return d if d is not None else self.args[index]


EventArgs.empty = EventArgs()


__all__ = ['EventArgs']
