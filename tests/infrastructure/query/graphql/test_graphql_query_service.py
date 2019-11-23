from pytest import fixture, raises
from graphql import GraphQLSchema, build_schema, graphql
from integrark.application.services import QueryService
from integrark.infrastructure.query import GraphqlQueryService
from integrark.infrastructure.query.graphql import (
    GraphqlSchemaLoader, GraphqlSolutionLoader)


@fixture
def schema_loader() -> GraphqlSchemaLoader:
    class MockGraphqlSchemaLoader(GraphqlSchemaLoader):
        def load(self):
            content = super().load()
            content += """
            type Doctor {
                name: String!
                specialty: String!
                age: Int @auth(roles: ["HR_MANAGER"])
            }

            type Query {
                doctors: [Doctor]
                veterinary: Doctor
            }
            """
            return build_schema(content)

    return MockGraphqlSchemaLoader('/tmp/fake')


@fixture
def solution_loader() -> GraphqlSolutionLoader:
    class MockSolution:
        type = 'Query'

        def resolve(self, field):
            return getattr(self, f'resolve__{field}', None)

        async def resolve__doctors(self, parent, info):
            return [
                {'name': 'Hugo', 'specialty': 'Cardiology'},
                {'name': 'Paco', 'specialty': 'Psychiatry'},
                {'name': 'Luis', 'specialty': 'Oncology'}
            ]

        async def resolve__veterinary(self, parent, info):
            raise Exception('The veterinary field has not been implemented.')

    class MockGraphqlSolutionLoader(GraphqlSolutionLoader):
        def load(self):
            return [MockSolution()], lambda context: {}

    return MockGraphqlSolutionLoader('/tmp/fake')


@fixture
def query_service(schema_loader, solution_loader) -> GraphqlQueryService:
    return GraphqlQueryService(schema_loader, solution_loader)


@fixture
def schema():
    content = """
    type Student {
        name: String!
        age: Int!
    }

    type Query {
        students: [Student]
    }
    """
    return build_schema(content)


@fixture
def students():
    return [
        {'name': 'Esteban', 'age': 30},
        {'name': 'Gabriel', 'age': 27},
        {'name': 'Valentina', 'age': 35},
    ]


@fixture
def solutions(students):
    class Solution:
        type = 'Query'

        def resolve(self, field):
            return getattr(self, f'resolve__{field}', None)

        async def resolve__students(self, parent, info):
            return students

    return [
        Solution()
    ]


def test_graphql_query_service(query_service):
    assert issubclass(GraphqlQueryService, QueryService)
    assert isinstance(query_service, GraphqlQueryService)


async def test_graphql_query_service_run(query_service):
    query = """
    {
        doctors {
            specialty
        }
    }
    """

    result = await query_service.run(query)

    assert result.data == {
        'doctors': [
            {'specialty': 'Cardiology'},
            {'specialty': 'Psychiatry'},
            {'specialty': 'Oncology'}
        ]
    }
    assert result.errors is None


async def test_graphql_query_service_bind_schema(
        query_service, schema, solutions, students):

    schema = query_service._bind_schema(schema, solutions)

    query = """
    {
        students {
            name
            age
        }
    }
    """

    result = await graphql(schema, query)

    assert result.data['students'] == students
    assert result.errors is None


async def test_graphql_query_service_run_location_errors(query_service):
    query = """
    {
        doctors {
            name
            address
        }
    }
    """

    result = await query_service.run(query)

    assert result.data is None
    assert result.errors == [
        {'message': "Cannot query field 'address' on type 'Doctor'.",
         'locations': [{'line': 5, 'column': 13}], 'path': None}]


async def test_graphql_query_service_run_path_errors(query_service):
    query = """
    {
        doctors {
            name
        }
        veterinary {
            name
        }
    }
    """

    result = await query_service.run(query)

    assert result.data == {
        'doctors': [
            {'name': 'Hugo'},
            {'name': 'Paco'},
            {'name': 'Luis'}
        ],
        'veterinary': None
    }

    assert result.errors == [
        {'message': 'The veterinary field has not been implemented.',
         'locations': [{'line': 6, 'column': 9}],
         'path': ['veterinary']}
    ]
