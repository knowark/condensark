from pytest import fixture
from integrark.application.coordinators import ExecutionCoordinator


@fixture
def execution_coordinator() -> ExecutionCoordinator:
    return ExecutionCoordinator()


def test_execution_coordinator_instantiation(
        execution_coordinator: ExecutionCoordinator) -> None:
    assert hasattr(execution_coordinator, 'execute')


async def test_execution_coordinator_execute(
        execution_coordinator: ExecutionCoordinator) -> None:

    result = await execution_coordinator.execute('{query {name}}')
    assert isinstance(result, dict)
