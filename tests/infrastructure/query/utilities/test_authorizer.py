import jwt
from pytest import fixture, raises
from integrark.infrastructure.query import Authorizer, AuthorizationError


@fixture
def permissions():
    return {
        "default": {
            'create': ['admin'],
            'delete': ['admin'],
            'update': ['admin'],
            'read': {
                'admin': lambda user: ['id', '!=', '']
            }
        },
        "projects": {
            'create': ['admin', 'manager'],
            'delete': ['admin'],
            'update': ['admin', 'manager'],
            'read': {
                'admin': lambda user: ['id', '!=', ''],
                'manager': lambda user: [
                    'city', '=', user['attributes']['city']],
                'user': lambda user: ['id', '=', user['uid']]
            }
        },
        "tasks": {
            'create': ['admin', 'user'],
            'delete': ['admin'],
            'update': ['admin', 'manager', 'user'],
            'read': {
                'admin': lambda user: ['id', '!=', ''],
                'manager': lambda user: [
                    'city', '=', user['attributes']['city']],
                'user': lambda user: ['id', '=', user['uid']]
            }
        }
    }


@fixture
def authorizer(permissions):
    return Authorizer(permissions)


def test_authorizer_instantiation(authorizer):
    assert authorizer is not None
    assert authorizer.default_resource == 'default'
    assert authorizer.default_operation == 'create'
    assert authorizer.read_operation == 'read'


def test_authorizer_check(authorizer):
    user = {
        'uid': '001',
        'name': 'Pepe Pérez',
        'email': 'pp@mail.com',
        'roles': ['user']
    }

    resource = 'tasks'
    result = authorizer.check(user, resource)

    assert result is None


def test_authorizer_check_unauthorized_resource(authorizer):
    user = {
        'uid': '001',
        'name': 'Pepe Pérez',
        'email': 'pp@mail.com',
        'roles': ['user']
    }

    resource = 'project'
    with raises(AuthorizationError):
        result = authorizer.check(user, resource)
