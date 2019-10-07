from pytest import fixture, raises
from integrark.application.services import QueryService
from integrark.infrastructure.query import GraphqlQueryService


@fixture
def query_service() -> GraphqlQueryService:
    return GraphqlQueryService()


def test_standard_auth_service(query_service):
    assert issubclass(GraphqlQueryService, QueryService)
    assert isinstance(query_service, GraphqlQueryService)


async def test_graphql_query_service_run(query_service):
    pass
