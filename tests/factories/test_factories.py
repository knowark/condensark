import inspect
from injectark import Injectark
from integrark.core import config
from integrark.factories import factory_builder


test_tuples = [
    ('BaseFactory', [
        ('QueryService', 'StandardQueryService'),
        ('RouteService', 'StandardRouteService'),
        ('ExecutionManager', 'ExecutionManager'),
        ('RoutingManager', 'RoutingManager'),
        ('JwtSupplier', 'JwtSupplier'),
        ('IntegrationImporter', 'IntegrationImporter'),
    ]),
    ('GraphqlFactory', [
        ('QueryService', 'GraphqlQueryService'),
    ]),
    ('RestFactory', [
        ('RouteService', 'RestRouteService'),
    ]),
]


def test_factories():
    for factory_name, dependencies in test_tuples:
        factory = factory_builder.build(config, name=factory_name)

        injector = Injectark(factory=factory)

        for abstract, concrete in dependencies:
            result = injector.resolve(abstract)
            assert type(result).__name__ == concrete
