from pathlib import Path
from typing import Dict, Any
from pytest import fixture, raises
from graphql.type import GraphQLResolveInfo
from integrark.infrastructure.query.graphql import (
    GraphqlSolutionLoader, DataLoader)
from .sample_data import human_data, droid_data


@fixture
def solution_loader() -> GraphqlSolutionLoader:
    directory = str(Path(__file__).parent / 'data/solutions/starwars')
    return GraphqlSolutionLoader(directory)


async def test_graphql_solution_loader_load(
        solution_loader: GraphqlSolutionLoader):

    config: Dict[str, Any] = {
        'data': {
            'human_data': human_data,
            'droid_data': droid_data
        }
    }

    solutions, dataloaders = solution_loader.load()

    query_solution = next(solution for solution in solutions
                          if solution.type == 'Query')

    hero_resolver = query_solution.resolve('hero')

    class Info:
        context = {
            'data': {
                'human_data': human_data,
                'droid_data': droid_data
            }
        }

    assert (await hero_resolver(None, Info(), 1))['name'] == 'R2-D2'
    for name, loader in dataloaders:
        assert isinstance(loader, DataLoader)


async def test_graphql_solution_loader_load_nonpackage(
        solution_loader: GraphqlSolutionLoader):

    directory = str(Path(__file__).parent / 'data/solutions/nonpackage')
    solution_loader.path = directory

    solutions = solution_loader.load()

    assert solutions == ([], {})
