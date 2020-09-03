from pytest import fixture
from injectark import Injectark
from integrark.core import config
from integrark.factories import strategy_builder, factory_builder
from integrark.presenters.shell import Shell


@fixture
def shell() -> Shell:
    """Create app testing client"""
    config['factory'] = 'CheckFactory'
    config['strategies'] = ['base', 'check']

    strategy = strategy_builder.build(config['strategies'])
    factory = factory_builder.build(config)

    injector = Injectark(strategy, factory)

    return Shell(config, injector)
