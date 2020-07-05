from pytest import fixture
from injectark import Injectark
from integrark.core import Config, TrialConfig
from integrark.factories import build_factory
from integrark.presenters.shell import Shell


@fixture
def shell() -> Shell:
    """Create app testing client"""
    config = TrialConfig()
    strategy = config['strategy']
    factory = build_factory(config)

    resolver = Injectark(strategy, factory)

    return Shell(config, resolver)
