from typing import List, Dict, Any
from modelark import Repository
from .dataloader import StandardDataLoader


class Joiner:
    def __init__(
        self, join: Repository, target: str = '',
        link: Repository = None, source: str = ''
    ) -> None:
        self.join = join
        self.target = target
        self.link = link
        self.source = source

    def build(self, context: Dict[str, Any] = None):
        fetch = self._many_to_one_fetch
        if self.join and self.target:
            fetch = self._one_to_many_fetch

        return StandardDataLoader(fetch, context)

    async def _many_to_one_fetch(self, ids: List[str]):
        field = self.source or 'id'
        return await self.join.search([(field, 'in', ids)])

    async def _one_to_many_fetch(self, ids: List[str]):
        items = await self.join.search([(self.target, 'in', ids)])
        index: Dict = {}
        for item in items:
            index.setdefault(
                getattr(item, self.target), []).append(item)

        return [index.get(id_, []) for id_ in ids]
