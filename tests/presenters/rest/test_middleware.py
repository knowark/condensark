from pytest import fixture
from integrark.presenters.rest.middleware import (
    user_middleware_factory, errors_middleware_factory)
from integrark.core import JwtSupplier
from integrark.presenters.rest import middleware


async def test_user_middleware_default_user():
    user = None

    class MockRequest(dict):
        def __init__(self):
            self.headers = {}
            self.query = {}

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
        'tenant': '',
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
            #     "tenant": "Knowark",
            #     "name": "John Doe",
            #     "email": "john@doe.com"
            # }
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0aWQiOiIwMDEiLCJ1aWQiOi"
            "IwMDEiLCJ0ZW5hbnQiOiJLbm93YXJrIiwibmFtZSI6IkpvaG4gRG9lIiwiZW1ha"
            "WwiOiJqb2huQGRvZS5jb20ifQ.udlkUWVOatst5IoDRlJsQVn"
            "U_atCAltOelOJvRCr8BY"
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
        "tenant": "Knowark",
        "name": "John Doe",
        "email": "john@doe.com",
        'attributes': {},
        'authorization': {},
        'roles': []
    }

async def test_error_middleware(headers, monkeypatch):
    class MockRequest(dict):
        def __init__(self):
            self.headers = headers

    class MockWeb:
        @property
        def Request(self):
            return

        @property
        def middleware(self):
            def decorator(function):
                return function
            return decorator

        def json_response(self, *args, **kwargs):
            return args, kwargs

    mock_request = MockRequest()

    async def handler(request):
        raise Exception('Request processing error.')

    class MockInjector(dict):
        def __init__(self):
            pass

    mock_web = MockWeb()
    monkeypatch.setattr(middleware, 'web', mock_web)

    errors_middleware = errors_middleware_factory(MockInjector())

    args, kwargs = await errors_middleware(mock_request, handler)

    assert args == ({'errors': [{'message': 'Request processing error.',
                                 'type': 'Exception'}]},)
    assert kwargs['status'] == 500

