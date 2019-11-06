from typing import Dict, Callable, Any
from aiohttp import web


@web.middleware
async def user_middleware(
        request: web.Request, handler: Callable) -> web.Response:

    request['user'] = extract_user(request)

    response = await handler(request)
    return response


def extract_user(request: web.Response) -> Dict[str, Any]:
    user = {
        'tid': '',
        'uid': '',
        'name': '<<PUBLIC>>',
        'email': '',
        'attributes': {},
        'authorization': {}
    }
    return user


MIDDLEWARES = [
    user_middleware
]
