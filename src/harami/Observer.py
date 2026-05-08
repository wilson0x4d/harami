# SPDX-FileCopyrightText: © 2025 Shaun Wilson
# SPDX-License-Identifier: MIT


from typing import Any, Callable, Coroutine, TypeAlias, Union


Observer: TypeAlias = Callable[[Any], Union[None, Coroutine[Any, Any, None]]]   # noqa: N801
