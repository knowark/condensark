from typing import Dict, Any, Callable, cast
from typing_extensions import Protocol
from graphql.type import GraphQLResolveInfo


class Resolver(Protocol):
    def __call__(self, parent: Any, info: GraphQLResolveInfo,
                 *args, **kwargs) -> Any: ...


class Solution:

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self._type = 'Query'

    @property
    def type(self) -> str:
        return self._type

    def resolve(self, field: str) -> Resolver:
        return cast(Resolver, self._default_resolver)

    def _default_resolver(
        self, parent: Any, info: GraphQLResolveInfo,
            *args, **kwargs) -> Any:
        return []
