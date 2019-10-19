from pathlib import Path
from typing import Dict, Any
from pytest import fixture, raises
from graphql.type import GraphQLResolveInfo
from integrark.infrastructure.query.graphql import (
    GraphqlDataloaderLoader)


@fixture
def dataloader_loader() -> GraphqlDataloaderLoader:
    directory = str(Path(__file__).parent / 'data/solutions/starwars')
    return GraphqlDataloaderLoader(directory)


async def test_graphql_dataloader_loader_load(
        dataloader_loader: GraphqlDataloaderLoader):

    dataloaders = dataloader_loader.load()

    for name, loader in dataloaders:
        assert isinstance(loader, object)
