from pytest import fixture
from integrark.application.services import StandardRouteService
from integrark.application.coordinators import RoutingCoordinator


@fixture
def routing_coordinator() -> RoutingCoordinator:
    route_service = StandardRouteService(response={'data': 'response'})
    return RoutingCoordinator(route_service)


def test_routing_coordinator_instantiation(
        routing_coordinator: RoutingCoordinator) -> None:
    assert hasattr(routing_coordinator, 'route')


async def test_routing_coordinator_route(
        routing_coordinator: RoutingCoordinator) -> None:
    result = await routing_coordinator.route('upstream_service',
                                             {'params': 'data'})

    assert isinstance(result, dict)
    assert result == {'data': 'response'}


# async def test_execution_coordinator_execute_errors(
#         execution_coordinator: ExecutionCoordinator) -> None:
#     query_service = execution_coordinator.query_service
#     setattr(query_service, 'response',
#             QueryResult(None, [{'message': 'Fatal Error!'}]))

#     result = await execution_coordinator.execute('{query {name}}')

#     assert result == {
#         'errors': [{'message': 'Fatal Error!'}]
#     }
