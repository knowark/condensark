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
        'authorization': {}
    }
