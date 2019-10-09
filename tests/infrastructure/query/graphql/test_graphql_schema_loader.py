from pathlib import Path
from pytest import fixture, raises
from integrark.infrastructure.query.graphql import GraphqlSchemaLoader


@fixture
def schema_loader() -> GraphqlSchemaLoader:
    directory = str(Path(__file__).parent / 'data/definitions/starwars')
    return GraphqlSchemaLoader(directory)


def test_graphql_schema_loader_load(
        schema_loader: GraphqlSchemaLoader):
    schema = schema_loader.load()
    assert list(schema.get_type('Human').fields.keys()) == [
        'id', 'name', 'friends', 'appearsIn', 'homePlanet']
    assert list(schema.get_type('Droid').fields.keys()) == [
        'id', 'name', 'friends', 'appearsIn', 'primaryFunction']
