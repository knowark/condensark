import inspect
from pytest import fixture
from injectark import Injectark
from integrark.infrastructure.core import Config
from integrark.infrastructure.factories import build_factory, Factory


@fixture
def mock_config():
    class MockConfig(Config):
        def __init__(self):
            self['factory'] = 'MemoryFactory'

    return MockConfig()


@fixture
def mock_strategy():
    return {
        "QueryService": {
            "method": "standard_query_service"
        },
        "ExecutionCoordinator": {
            "method": "execution_coordinator"
        },
        "JwtSupplier": {
            "method": "jwt_supplier"
        }
    }


def test_memory_factory(mock_config, mock_strategy):
    factory = build_factory(mock_config)
    resolver = Injectark(strategy=mock_strategy, factory=factory)

    for resource in mock_strategy.keys():
        result = resolver.resolve(resource)
        classes = inspect.getmro(type(result))
        assert resource in [item.__name__ for item in classes]
