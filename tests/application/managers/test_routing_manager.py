from pytest import fixture
from integrark.application.services import StandardRouteService
from integrark.application.managers import RoutingManager


@fixture
def routing_manager() -> RoutingManager:
    route_service = StandardRouteService(response={'data': 'response'})
    return RoutingManager(route_service)


def test_routing_manager_instantiation(
        routing_manager: RoutingManager) -> None:
    assert hasattr(routing_manager, 'route')


async def test_routing_manager_route(
        routing_manager: RoutingManager) -> None:
    result = await routing_manager.route('upstream_service',
                                             {'params': 'data'})

    assert isinstance(result, dict)
    assert result == {'data': 'response'}


# async def test_execution_manager_execute_errors(
#         execution_manager: ExecutionManager) -> None:
#     query_service = execution_manager.query_service
#     setattr(query_service, 'response',
#             QueryResult(None, [{'message': 'Fatal Error!'}]))

#     result = await execution_manager.execute('{query {name}}')

#     assert result == {
#         'errors': [{'message': 'Fatal Error!'}]
#     }
