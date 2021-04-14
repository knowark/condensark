from pytest import fixture
from integrark.presenters.rest.middleware import user_middleware_factory
from integrark.core import JwtSupplier


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
