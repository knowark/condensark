from pytest import fixture
from aiohttp import web
from integrark.infrastructure.web.middleware import user_middleware_factory
from integrark.infrastructure.core import JwtSupplier


async def test_user_middleware_default_user():
    user = None

    class MockRequest(dict):
        def __init__(self):
            self.headers = {}

    mock_request = MockRequest()

    async def handler(request):
        nonlocal user
        user = request['user']

    class MockInjector(dict):
        def __init__(self):
            self['JwtSupplier'] = JwtSupplier('WRONG')

    user_middleware = user_middleware_factory(MockInjector())

    await user_middleware(mock_request, handler)

    assert user == {
        'tid': '',
        'uid': '',
        'name': '<<PUBLIC>>',
        'email': '',
        'attributes': {},
        'authorization': {},
        'roles': []
    }


@fixture
def headers() -> dict:

    return {
        "Authorization":  (
            # Password: INTEGRARK_SECRET
            # Payload:
            # {
            #     "tid": "001",
            #     "uid": "001",
            #     "name": "John Doe",
            #     "email": "john@doe.com"
            # }
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0aWQiOiIwMDEiLCJ1aWQiOi"
            "IwMDEiLCJuYW1lIjoiSm9obiBEb2UiLCJlbWFpbCI6ImpvaG5AZG9lLmNvbSJ9."
            "y9UEPbviFHpH9H-1fv1kv3Sgf4UnKkiQ3B3BqihZpD4"
        )
    }


async def test_user_middleware_authorization_token_user(headers):
    user = None

    class MockRequest(dict):
        def __init__(self):
            self.headers = headers

    mock_request = MockRequest()

    async def handler(request):
        nonlocal user
        user = request['user']

    class MockInjector(dict):
        def __init__(self):
            self['JwtSupplier'] = JwtSupplier('INTEGRARK_SECRET')

    user_middleware = user_middleware_factory(MockInjector())

    await user_middleware(mock_request, handler)

    assert user == {
        "tid": "001",
        "uid": "001",
        "name": "John Doe",
        "email": "john@doe.com",
        'attributes': {},
        'authorization': {},
        'roles': []
    }
