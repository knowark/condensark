from ..core import Config
from .factory import Factory


class MemoryFactory(Factory):
    def __init__(self, config: Config) -> None:
        self.config = config
