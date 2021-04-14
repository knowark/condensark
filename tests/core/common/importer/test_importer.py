from pathlib import Path
from typing import Dict, Any
from pytest import fixture, raises
from graphql.type import GraphQLResolveInfo
from integrark.core import (
    IntegrationImporter, DataLoader)
from .sample_data import human_data, droid_data


@fixture
def integration_importer() -> IntegrationImporter:
    directory = str(Path(__file__).parent / 'data/integrations/dev')
    return IntegrationImporter(directory)


async def test_integration_importer_load(
        integration_importer: IntegrationImporter):

    config: Dict[str, Any] = {
        'data': {
            'human_data': human_data,
            'droid_data': droid_data
        }
    }

    integration_importer.load()

    solutions = integration_importer.solutions
    locations = integration_importer.locations
    dataloaders_factory = integration_importer.dataloaders_factory

    query_solution = next(solution for solution in solutions
                          if solution.type == 'Query')

    droid_solution = next(solution for solution in solutions
                          if solution.type == 'Droid')

    media_location = next(location for location in locations
                          if location.path == 'media')

    auth_location = next(location for location in locations
                         if location.path == 'auth')

    hero_resolver = query_solution.resolve('hero')

    name_resolver = droid_solution.resolve('name')

    class Info:
        context = {
            'data': {
                'human_data': human_data,
                'droid_data': droid_data
            }
        }

    dataloaders = dataloaders_factory(Info.context)

    assert (await hero_resolver(None, Info(), 1))['name'] == 'R2-D2'

    assert (await name_resolver(None, Info(), 1)) == 'R2-D2'

    assert (await media_location.route({'context': 'data'})) == (
        "HTTP Response from 'media' with context {'context': 'data'}")

    assert (await auth_location.route({'context': 'data'})) == (
        "HTTP Response from 'auth' with context {'context': 'data'}")

    assert len(dataloaders)
    for name, loader in dataloaders.items():
        assert isinstance(loader, DataLoader)
        assert loader.context == Info.context


async def test_integration_importer_load_nonpackage(
        integration_importer: IntegrationImporter):

    directory = str(Path(__file__).parent / 'data/integrations/nonpackage')
    integration_importer.path = directory

    integration_importer.load()

    assert integration_importer.solutions == []
    assert integration_importer.locations == []
    assert integration_importer.dataloaders_factory({}) == {}
