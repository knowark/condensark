from ..core import Config
from .memory_factory import MemoryFactory


class TrialFactory(MemoryFactory):
    def __init__(self, config: Config) -> None:
        self.config = config
