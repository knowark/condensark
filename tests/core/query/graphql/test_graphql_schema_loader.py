from pathlib import Path
from pytest import fixture
from graphql import GraphQLSchema
from integrark.core.query import GraphqlSchemaLoader


def test_graphql_schema_loader_load():
    directory = str(Path(__file__).parent / 'data/definitions/starwars')
    schema_loader = GraphqlSchemaLoader(directory)
    schema = schema_loader.load()

    human_type = schema.get_type('Human')
    assert human_type
    human_fields = getattr(human_type, 'fields', None)
    assert list(human_fields.keys()) == [
        'id', 'name', 'friends', 'appearsIn', 'homePlanet']

    droid_type = schema.get_type('Droid')
    assert droid_type
    droid_fields = getattr(droid_type, 'fields', None)
    assert list(droid_fields.keys()) == [
        'id', 'name', 'friends', 'appearsIn', 'primaryFunction']
