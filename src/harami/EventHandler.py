# SPDX-FileCopyrightText: © 2025 Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Callable, TypeAlias
from .EventArgs import EventArgs


EventHandler: TypeAlias = Callable[[object, 'EventArgs'], None]   # noqa: N801
