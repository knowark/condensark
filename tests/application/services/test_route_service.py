from pytest import fixture, raises
from integrark.application.services import RouteService, StandardRouteService


def test_route_service_methods():
    abstract_methods = RouteService.__abstractmethods__

    assert 'route' in abstract_methods


@fixture
def route_service() -> StandardRouteService:
    return StandardRouteService(response={'data': 'response'})


def test_standard_route_service_instantiation(route_service):
    assert isinstance(route_service, RouteService)


async def test_standard_route_service_route(route_service):
    response = await route_service.route('upstream_service')

    assert isinstance(response, dict)
    assert response == {'data': 'response'}
