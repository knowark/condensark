from pytest import fixture
from aiohttp import web
from injectark import Injectark
from integrark.core import config
from integrark.factories import strategy_builder, factory_builder
from integrark.presenters.rest import create_app


@fixture
def app(loop, aiohttp_client):
    """Create app testing client"""
    config['factory'] = 'CheckFactory'
    config['strategies'] = ['base', 'check']

    strategy = strategy_builder.build(config['strategies'])
    factory = factory_builder.build(config)

    injector = Injectark(strategy, factory)

    app = create_app(config, injector)

    return loop.run_until_complete(aiohttp_client(app))
