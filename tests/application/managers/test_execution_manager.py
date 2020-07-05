from pytest import fixture
from integrark.application.services import StandardQueryService, QueryResult
from integrark.application.managers import ExecutionManager


@fixture
def execution_manager() -> ExecutionManager:
    response = QueryResult({'name': 'value'}, None)
    query_service = StandardQueryService(response)
    return ExecutionManager(query_service)


def test_execution_manager_instantiation(
        execution_manager: ExecutionManager) -> None:
    assert hasattr(execution_manager, 'execute')


async def test_execution_manager_execute(
        execution_manager: ExecutionManager) -> None:
    result = await execution_manager.execute('{query {name}}')

    assert isinstance(result, dict)
    assert result == {'data': {'name': 'value'}}


async def test_execution_manager_execute_errors(
        execution_manager: ExecutionManager) -> None:
    query_service = execution_manager.query_service
    setattr(query_service, 'response',
            QueryResult(None, [{'message': 'Fatal Error!'}]))

    result = await execution_manager.execute('{query {name}}')

    assert result == {
        'errors': [{'message': 'Fatal Error!'}]
    }
