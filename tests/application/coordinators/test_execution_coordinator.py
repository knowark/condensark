from pytest import fixture
from integrark.application.services import StandardQueryService, QueryResult
from integrark.application.coordinators import ExecutionCoordinator


@fixture
def execution_coordinator() -> ExecutionCoordinator:
    response = QueryResult({'name': 'value'}, None)
    query_service = StandardQueryService(response)
    return ExecutionCoordinator(query_service)


def test_execution_coordinator_instantiation(
        execution_coordinator: ExecutionCoordinator) -> None:
    assert hasattr(execution_coordinator, 'execute')


async def test_execution_coordinator_execute(
        execution_coordinator: ExecutionCoordinator) -> None:
    result = await execution_coordinator.execute('{query {name}}')

    assert isinstance(result, dict)
    assert result == {'data': {'name': 'value'}}


async def test_execution_coordinator_execute_errors(
        execution_coordinator: ExecutionCoordinator) -> None:
    query_service = execution_coordinator.query_service
    setattr(query_service, 'response',
            QueryResult(None, [{'message': 'Fatal Error!'}]))

    result = await execution_coordinator.execute('{query {name}}')

    assert result == {
        'errors': [{'message': 'Fatal Error!'}]
    }
