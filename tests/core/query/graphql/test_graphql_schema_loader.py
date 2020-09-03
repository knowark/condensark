from pathlib import Path
from pytest import fixture
from integrark.core.query import GraphqlSchemaLoader


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


def test_graphql_schema_loader_load_builtin_directives(
        schema_loader: GraphqlSchemaLoader):
    schema = schema_loader.load()

    directives_dict = {}
    for directive in schema.directives:
        directives_dict[directive.name] = directive

    auth_directive = directives_dict['auth']

    assert auth_directive is not None
    assert 'roles' in auth_directive.args
    assert 'FIELD_DEFINITION' == auth_directive.locations[0].name
