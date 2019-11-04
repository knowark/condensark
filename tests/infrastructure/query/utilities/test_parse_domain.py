import json
from pytest import fixture, raises
from integrark.infrastructure.query import parse_domain


def test_parse_domain():
    filter = '[["id", "=", "001"]]'

    domain = parse_domain(filter)

    assert isinstance(domain, list)


def test_parse_domain_wrong_json():
    filter = '[("id", "=", "001")]'

    with raises(json.JSONDecodeError):
        domain = parse_domain(filter)
