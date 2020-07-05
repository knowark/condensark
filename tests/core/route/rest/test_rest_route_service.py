from pytest import fixture, raises
from integrark.application.services import RouteService
from integrark.core.importer.location import Location
from integrark.core.route import RestRouteService
from integrark.core import IntegrationImporter


@fixture
def integration_importer() -> IntegrationImporter:
    class MockLocation(Location):
        path = 'media'

        async def route(self, context):
            return f"Multimedia data with context: {context}"

    class MockIntegrationImporter(IntegrationImporter):
        def load(self):
            self.locations = [MockLocation()]

    integration_importer = MockIntegrationImporter('/tmp/fake')
    integration_importer.load()
    return integration_importer


@fixture
def route_service(integration_importer) -> RestRouteService:
    return RestRouteService(integration_importer)


def test_rest_route_service(route_service):
    assert issubclass(RestRouteService, RouteService)
    assert isinstance(route_service, RestRouteService)


async def test_rest_route_service_route(route_service):
    location = 'media'
    context = {'request': 'data'}

    result = await route_service.route(location, context)

    assert result == "Multimedia data with context: {'request': 'data'}"
