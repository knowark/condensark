import inspect
from injectark import Injectark
from integrark.core import config
from integrark.factories import factory_builder, strategy_builder


test_tuples = [
    ('BaseFactory', ['base']),
    ('CheckFactory', ['base', 'check']),
    ('GraphqlFactory', ['base', 'rest', 'graphql']),
    ('RestFactory', ['base', 'rest']),
]


def test_factories():
    for factory_name, strategy_names in test_tuples:
        factory = factory_builder.build(config, name=factory_name)
        strategy = strategy_builder.build(strategy_names)

        injector = Injectark(strategy=strategy, factory=factory)

        for resource in strategy.keys():
            print('Resource>>>', factory_name, resource)
            result = injector.resolve(resource)
            classes = inspect.getmro(type(result))
            assert resource in [item.__name__ for item in classes]
