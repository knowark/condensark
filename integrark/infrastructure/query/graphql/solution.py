from typing import Dict, Any, Callable, cast
from typing_extensions import Protocol
from graphql.type import GraphQLResolveInfo


class Resolver(Protocol):
    def __call__(self, parent: Any, info: GraphQLResolveInfo,
                 *args, **kwargs) -> Any: ...


class Solution:
    type = 'Query'

    def resolve(self, field: str) -> Resolver:
        return getattr(self, f'resolve__{field}', None)
