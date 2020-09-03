from pytest import fixture, raises
from integrark.core import Location


@fixture
def location() -> Location:
    return Location()


def test_location(location):
    assert location.path == ''


async def test_solution_default_resolver(location):
    location.path = 'upstream_service'
    result = await location.route({'context': 'data'})

    assert result == "REST Proxy. Context: {'context': 'data'}"
