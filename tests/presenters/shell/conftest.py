from pytest import fixture
from injectark import Injectark
from integrark.core import config
from integrark.factories import factory_builder
from integrark.presenters.shell import Shell


@fixture
def shell() -> Shell:
    """Create app testing client"""
    config['factory'] = 'CheckFactory'

    factory = factory_builder.build(config)

    injector = Injectark(factory)

    return Shell(config, injector)
