from typing import List, Dict, Any
from modelark import Repository
from .dataloader import StandardDataLoader


class Joiner:
    def __init__(
        self, join: Repository, target: str = None,
        link: Repository = None, source: str = None
    ) -> None:
        self.join = join
        self.target = target
        self.link = link
        self.source = source

    def build(self, context: Dict[str, Any] = None):
        fetch = self._many_to_one_fetch


        return StandardDataLoader(fetch, context)

    async def _many_to_one_fetch(self, ids: List[str]):
        field = self.target or 'id'
        return await self.join.search([(field, 'in', ids)])

