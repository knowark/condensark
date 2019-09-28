from pytest import fixture, raises
from integrark.application.services import QueryService, StandardQueryService


def test_query_service_methods():
    abstract_methods = QueryService.__abstractmethods__

    assert 'run' in abstract_methods


@fixture
def query_service() -> StandardQueryService:
    return StandardQueryService(response={'data': 'response'})


def test_standard_query_service_instantiation(query_service):
    assert isinstance(query_service, QueryService)


async def test_standard_query_service_run(query_service):
    response = await query_service.run('QUERY')

    assert isinstance(response, dict)
    assert response == {'data': 'response'}
