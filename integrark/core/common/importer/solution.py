from typing import Callable, Awaitable, Any


class Solution:
    type = 'Query'

    def resolve(self, field: str) -> Callable[[Any], Awaitable[Any]]:
        return getattr(self, f'resolve__{field}', None)
