from pytest import fixture, raises
from integrark.infrastructure.importer import Location


@fixture
def location() -> Location:
    return Location()


def test_location(location):
    assert location.path == ''


def test_solution_default_resolver(location):
    location.path = 'upstream_service'
    result = location.route({'context': 'data'})

    assert result == "REST Proxy. Context: {'context': 'data'}"
