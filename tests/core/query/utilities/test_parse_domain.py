import rapidjson as json
from pytest import fixture, raises
from integrark.core import parse_domain, join_domains


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

    alias = {'siteId': 'site_id', 'mainPhone': 'telephone'}
    domain = parse_domain(filter, alias)

    assert domain == [["id", "=", "001"], ["site_id", "=", "003"],
                      ["telephone", "=", "123456"]]


def test_parse_domain_default_snake_case():
    filter = ('[["id", "=", "001"], ["siteId", "=", "003"], '
              '["mainPhone", "=", "123456"]]')

    domain = parse_domain(filter, snake=True)

    assert domain == [["id", "=", "001"], ["site_id", "=", "003"],
                      ["main_phone", "=", "123456"]]


def test_join_domains_and():
    filter = ('[["id", "=", "001"], ["siteId", "=", "003"], '
              '["mainPhone", "=", "123456"]]')

    domains = []
    or_joined_domains = join_domains(domains)
    assert or_joined_domains == []

    domains = [
        ["id", "=", "001"],
        ["site_id", "=", "003"],
    ]
    or_joined_domains = join_domains(domains)
    assert or_joined_domains == [
        '|',
        ["id", "=", "001"],
        ["site_id", "=", "003"],
    ]

    domains = [
        ["id", "=", "001"],
        ["site_id", "=", "003"],
        ["main_phone", "=", "123456"]
    ]
    or_joined_domains = join_domains(domains)
    assert or_joined_domains == [
        '|',
        ["id", "=", "001"],
        '|',
        ["site_id", "=", "003"],
        ["main_phone", "=", "123456"]
    ]

    domains = [
        ["id", "=", "001"],
        ["site_id", "=", "003"],
        ["main_phone", "=", "123456"],
        ["main_address", "=", "5th street 99"]
    ]
    or_joined_domains = join_domains(domains)
    assert or_joined_domains == [
        '|',
        ["id", "=", "001"],
        '|',
        ["site_id", "=", "003"],
        '|',
        ["main_phone", "=", "123456"],
        ["main_address", "=", "5th street 99"]
    ]
