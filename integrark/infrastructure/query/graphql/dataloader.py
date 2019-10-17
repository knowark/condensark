from abc import ABC, abstractmethod
from asyncio import Task
from typing import Union, List, Callable, Any, NamedTuple

Id = Union[str, int]

FetchFunction = Callable[[List[Id]], List[Any]]


class DataLoader(ABC):
    def __init__(self):
        self.queue: List[Loader] = []

    @abstractmethod
    def fetch(self) -> List[Any]:
        """Fetch method to be implemented by subclasses"""


class StandardDataLoader(DataLoader):
    def __init__(self, fetch_function: FetchFunction) -> None:
        super().__init__()
        self.fetch_function = fetch_function

    def fetch(self):
        return self.fetch_function()


class Loader(NamedTuple):
    id: Id
    future: Task
