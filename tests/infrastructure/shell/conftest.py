from pytest import fixture
from injectark import Injectark
from integrark.infrastructure.core import Config, TrialConfig
from integrark.infrastructure.factories import build_factory
from integrark.infrastructure.shell import Shell


@fixture
def shell() -> Shell:
    """Create app testing client"""
    config = TrialConfig()
    strategy = config['strategy']
    factory = build_factory(config)

    resolver = Injectark(strategy, factory)

    return Shell(config, resolver)
