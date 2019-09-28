from pytest import fixture
from aiohttp import web
from injectark import Injectark
from integrark.infrastructure.core import build_config
from integrark.infrastructure.factories import build_factory
from integrark.infrastructure.web import create_app


@fixture
def app(loop, aiohttp_client):
    """Create app testing client"""
    config = build_config('', 'TEST')
    strategy = config['strategy']
    factory = build_factory(config)

    resolver = Injectark(strategy, factory)

    app = create_app(config, resolver)

    return loop.run_until_complete(aiohttp_client(app))
