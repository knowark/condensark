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
        if self.join and self.link:
            fetch = self._many_to_many_fetch

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

    async def _many_to_many_fetch(self, ids: List[str]):
        assert self.link and self.source and self.target
        joints = await self.link.search([(self.source, 'in', ids)])

        index: Dict = {}
        for joint in filter(None, joints):  # type: ignore
            index.setdefault(
                getattr(joint, self.source), []).append(joint)

        links = [index.get(id_, []) for id_ in ids]

        ids_index: Dict = {}
        target_ids = set()
        for item_list in links:
            for item in item_list:
                source_id = getattr(item, self.source)
                target_id = getattr(item, self.target)
                ids_index.setdefault(
                    source_id, []).append(target_id)
                target_ids.add(target_id)

        target_index = {
            target.id: target for target in await self.join.search(
                [('id', 'in', list(target_ids))]) if target}

        # List of lists
        result = []
        for id_ in ids:
            targets = [target_index.get(target_id, [])
                       for target_id in ids_index.get(id_, [])]
            result.append(targets)

        return result
