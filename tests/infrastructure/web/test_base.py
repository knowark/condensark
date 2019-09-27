from aiohttp.web import Application
from injectark import Injectark
from integrark.infrastructure.core import build_config
from integrark.infrastructure.factories import build_factory
from integrark.infrastructure.web import create_app


def test_create_app():
    config = build_config('', 'TEST')
    strategy = config['strategy']
    factory = build_factory(config)

    injector = Injectark(strategy, factory)

    app = create_app(config, injector)

    assert app is not None
    assert isinstance(app, Application)
