from aiohttp import web
from integrark.infrastructure.web.middleware import user_middleware


async def test_user_middleware(monkeypatch):
    user = None

    mock_request = {}

    async def handler(request):
        nonlocal user
        user = request['user']

    await user_middleware(mock_request, handler)

    assert user == {
        'tid': '',
        'uid': '',
        'name': '<<PUBLIC>>',
        'email': '',
        'attributes': {},
        'authorization': {}
    }
