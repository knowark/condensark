import multiprocessing
from collections import defaultdict
from typing import Dict, Any
from abc import ABC, abstractmethod
from json import loads, JSONDecodeError
from pathlib import Path


class Config(defaultdict, ABC):
    @abstractmethod
    def __init__(self):
        self['mode'] = 'BASE'
        self['strategy'] = {

        }


class TrialConfig(Config):
    def __init__(self):
        super().__init__()
        self['mode'] = 'TEST'
        self['factory'] = 'TrialFactory'
        self['strategy'].update({

        })


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self["mode"] = 'DEV'
        self['factory'] = 'MemoryFactory'
        self["strategy"].update({

        })


class ProductionConfig(Config):
    def __init__(self):
        super().__init__()
        self["mode"] = 'PROD'
        self['factory'] = 'MemoryFactory'
        self["strategy"].update({

        })
