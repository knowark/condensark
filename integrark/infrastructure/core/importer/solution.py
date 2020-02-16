from typing import Callable


class Solution:
    type = 'Query'

    def resolve(self, field: str) -> Callable:
        return getattr(self, f'resolve__{field}', None)
