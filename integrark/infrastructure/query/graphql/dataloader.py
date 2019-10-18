from abc import ABC, abstractmethod
from asyncio import Future, get_event_loop, ensure_future
from typing import Union, List, Callable, Any, NamedTuple, Awaitable


FetchFunction = Callable[[List[str]], Awaitable[List[Any]]]


class DataLoader(ABC):
    def __init__(self):
        self.loop = get_event_loop()
        self.queue: List[Loader] = []

    def load(self, id: str) -> Awaitable[Any]:
        future = self.loop.create_future()
        self.queue.append(Loader(id, future))
        if len(self.queue) == 1:
            self._schedule_dispatch()
        return future

    @abstractmethod
    async def fetch(self, ids: List[str]) -> List[Any]:
        """Fetch method to be implemented by subclasses"""

    def _schedule_dispatch(self):
        self.loop.call_soon(ensure_future, self._dispatch())

    async def _dispatch(self):
        queue = self.queue
        self.queue = []

        ids = [item.id for item in queue]
        values = await self.fetch(ids)
        for item, value in zip(queue, values):
            item.future.set_result(value)


class StandardDataLoader(DataLoader):
    def __init__(self, fetch_function: FetchFunction) -> None:
        super().__init__()
        self.fetch_function = fetch_function

    async def fetch(self, ids: List[str]) -> List[Any]:
        return await self.fetch_function(ids)


class Loader(NamedTuple):
    id: str
    future: Future
