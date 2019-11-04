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


def test_parse_domain_alias():
    filter = ('[["id", "=", "001"], ["siteId", "=", "003"], '
              '["mainPhone", "=", "123456"]]')

    alias = {'siteId': 'site_id', 'mainPhone': 'main_phone'}
    domain = parse_domain(filter, alias)

    assert domain == [["id", "=", "001"], ["site_id", "=", "003"],
                      ["main_phone", "=", "123456"]]


def test_parse_domain_default_snake_case():
    filter = ('[["id", "=", "001"], ["siteId", "=", "003"], '
              '["mainPhone", "=", "123456"]]')

    domain = parse_domain(filter, snake=True)

    assert domain == [["id", "=", "001"], ["site_id", "=", "003"],
                      ["main_phone", "=", "123456"]]
