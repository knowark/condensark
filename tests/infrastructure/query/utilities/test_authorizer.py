import jwt
import rapidjson as json
from pytest import fixture, raises
from integrark.infrastructure.core import Authorizer, AuthorizationError


@fixture
def permissions():
    return {
        "default": {
            'create': ['admin'],
            'delete': ['admin'],
            'update': ['admin'],
            'read': {
                'admin': lambda user: []
            }
        },
        "projects": {
            'create': ['admin', 'manager'],
            'delete': ['admin'],
            'update': ['admin', 'manager'],
            'read': {
                'admin': lambda user: [],
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
                'admin': lambda user: [],
                'manager': lambda user: ['manager_id', '=', user['uid']],
                'user': lambda user: ['created_by', '=', user['uid']]
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


def test_authorizer_secure(authorizer):
    user = {
        'uid': '001',
        'name': 'Pepe Pérez',
        'email': 'pp@mail.com',
        'roles': ['user', 'manager', 'admin']
    }
    original_domain = json.dumps(
        [('city', '=', 'Popayán'), ('type', '=', 'normal')])
    resource = 'tasks'

    result = authorizer.secure(original_domain, user, resource)

    expected_domain = [
        ['city', '=', 'Popayán'],
        ['type', '=', 'normal'],
        '|',
        ['created_by', '=', '001'],
        ['manager_id', '=', '001']
    ]
    assert result == expected_domain


def test_authorizer_secure_not_authorized(authorizer):
    user = {
        'uid': '001',
        'name': 'Pepe Pérez',
        'email': 'pp@mail.com',
        'roles': ['external']
    }
    original_domain = json.dumps(
        [('city', '=', 'Popayán'), ('type', '=', 'normal')])
    resource = 'tasks'

    with raises(AuthorizationError):
        result = authorizer.secure(original_domain, user, resource)
