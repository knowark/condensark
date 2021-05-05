from pytest import fixture, raises
from types import SimpleNamespace as SN
from modelark import Repository, MemoryRepository
from integrark.core.common.security import (
    Enforcer, AuthorizationError)


@fixture
def location_repository():
    class MockLocationRepository(MemoryRepository): pass
    return MockLocationRepository().load({
        'default': {
            'L001': SN(id='L001', name='Campanario', country="Colombia"),
            'L002': SN(id='L002', name='Castellana', country="España"),
            'L003': SN(id='L003', name='Terraplaza', country="Colombia")
        }
    })


@fixture
def policy_repository():
    class MockPolicyRepository(MemoryRepository): pass
    return MockPolicyRepository().load({
        'default': {
            'P001': SN(id='P001', role_id='abc123',
                      resource='order', active=True, privilege='cr')
        }
    })


@fixture
def restriction_repository():
    class MockRestrictionRepository(MemoryRepository): pass
    return MockRestrictionRepository().load({
        'default': {
            'R001': SN(id='R001', policy_id='P001', sequence=0,
                      name="Colombian Locations", target='location',
                      domain='[["country", "=", "Colombia"]]'),
            'R002': SN(id='R002', policy_id='P001', sequence=1,
                      name="Colombian Orders", target='order',
                      domain=('[["location_id", "in", '
                              '[location.id for location in previous]]]'))
        }
    })


@fixture
def resolver(location_repository, policy_repository, restriction_repository):
    class MockResolver:
        def resolve(self, target: str) -> Repository:
            if target == 'policy':
                return policy_repository
            if target == 'restriction':
                return restriction_repository
            if target == 'location':
                return location_repository
    return MockResolver()


def test_enforcer_instantiation(resolver):
    enforcer = Enforcer(resolver)


async def test_enforcer_check(resolver):
    enforcer = Enforcer(resolver)

    context = {
        'user': {
            'id': '007',
            'username': 'jdoe',
            'roles': [
                'clerk|abc123'
            ]
        }
    }

    result = await enforcer.check('order', 'r', context)
    assert result is None
    result = await enforcer.check('order', 'c', context)
    assert result is None


async def test_enforcer_check_denied(resolver):
    enforcer = Enforcer(resolver)

    context = {
        'user': {
            'id': '007',
            'username': 'jdoe',
            'roles': [
                'clerk|abc123'
            ]
        }
    }

    with raises(AuthorizationError):
        await enforcer.check('order', 'd', context)


async def test_enforcer_secure(resolver):
    enforcer = Enforcer(resolver)

    context = {
        'user': {
            'id': '007',
            'username': 'jdoe',
            'roles': [
                'clerk|abc123'
            ]
        }
    }

    domain = await enforcer.secure('order', context)

    assert domain == [["location_id", "in", ["L001", "L003"]]]
