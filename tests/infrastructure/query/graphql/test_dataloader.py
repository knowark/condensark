from pytest import fixture, raises
from integrark.infrastructure.query.graphql import DataLoader


def test_dataloader_methods():
    abstract_methods = DataLoader.__abstractmethods__

    assert 'fetch' in abstract_methods


# @fixture
# def dataloader() -> DataLoader:
#     return DataLoader()


# def test_loader(dataloader):
#     assert loader.type == 'Query'


# def test_loader_default_resolver(loader):
#     resolver = loader.resolve('any')

#     assert resolver(None, None) == []
