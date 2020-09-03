from abc import ABC, abstractmethod
from asyncio import Future, get_event_loop, ensure_future, gather
from typing import Union, List, Dict, Callable, Any, NamedTuple, Awaitable


FetchFunction = Callable[[List[str]], Awaitable[List[Any]]]


class DataLoader(ABC):
    def __init__(self, context: Dict[str, Any] = None) -> None:
        self.loop = get_event_loop()
        self.queue: List[Loader] = []
        self.cache: Dict[str, Any] = {}
        self.context: Dict[str, Any] = context or {}

    def load(self, id: str) -> Awaitable[Any]:
        cached_result = self.cache.get(id)
        if cached_result is not None:
            return cached_result

        future = self.loop.create_future()
        self.cache[id] = future

        self.queue.append(Loader(id, future))
        if len(self.queue) == 1:
            self._schedule_dispatch()
        return future

    def load_many(self, ids: List[str]) -> Awaitable[List[Any]]:
        return gather(*[self.load(id) for id in ids])

    @abstractmethod
    async def fetch(self, ids: List[str]) -> List[Any]:
        """Fetch method to be implemented by subclasses"""

    def _schedule_dispatch(self):
        self.loop.call_soon(ensure_future, self._dispatch())

    async def _dispatch(self):
        ids = [item.id for item in self.queue]
        values = (await self.fetch(ids)) or []
        if len(values) != len(ids):
            return self._terminate(TypeError(
                "Unequal number of elements returned by fetch: "
                f"<ids>: {ids} <values>: {values}"))

        queue, self.queue = self.queue, []
        for item, value in zip(queue, values):
            if item.future.done():
                continue
            if isinstance(value, Exception):
                item.future.set_exception(value)
            else:
                item.future.set_result(value)

    def _terminate(self, error: Exception):
        self.cache = {}
        queue, self.queue = self.queue, []
        for item in queue:
            item.future.set_exception(error)


class StandardDataLoader(DataLoader):
    def __init__(self, fetch_function: FetchFunction,
                 context: Dict[str, Any] = None) -> None:
        super().__init__(context)
        self.fetch_function = fetch_function

    async def fetch(self, ids: List[str]) -> List[Any]:
        return await self.fetch_function(ids)


class Loader(NamedTuple):
    id: str
    future: Future
