import inspect
from pytest import fixture
from injectark import Injectark
from integrark.infrastructure.core import Config
from integrark.infrastructure.factories import build_factory, Factory


@fixture
def mock_config():
    class MockConfig(Config):
        def __init__(self):
            super().__init__()
            self['factory'] = 'GraphqlFactory'

    return MockConfig()


@fixture
def mock_strategy():
    return {
        "QueryService": {
            "method": "graphql_query_service"
        },
        "GraphqlSchemaLoader": {
            "method": "graphql_schema_loader"
        },
        "GraphqlSolutionLoader": {
            "method": "graphql_solution_loader"
        }
    }


def test_graphql_factory(mock_config, mock_strategy):
    factory = build_factory(mock_config)
    resolver = Injectark(strategy=mock_strategy, factory=factory)

    for resource in mock_strategy.keys():
        result = resolver.resolve(resource)
        classes = inspect.getmro(type(result))
        assert resource in [item.__name__ for item in classes]
