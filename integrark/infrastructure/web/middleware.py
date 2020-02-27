from typing import Dict, List, Callable, Any
from aiohttp import web
from injectark import Injectark


def user_middleware_factory(injector: Injectark) -> Callable:

    jwt_supplier = injector['JwtSupplier']

    @web.middleware
    async def user_middleware(
            request: web.Request, handler: Callable) -> web.Response:

        token = request.headers.get(
            'Authorization', '').replace('Bearer ', '')
        token = token or request.query.get('access_token', '')

        token_payload = jwt_supplier.decode(token) or {}

        request['user'] = extract_user(token_payload)

        return await handler(request)

    return user_middleware


def extract_user(payload: Dict[str, Any]) -> Dict[str, Any]:
    user = {
        'tid': '',
        'uid': '',
        'name': '<<PUBLIC>>',
        'email': '',
        'attributes': {},
        'authorization': {},
        'roles': []
    }
    user.update(payload)
    return user


def middlewares(injector: Injectark) -> List[Callable]:
    return [
        user_middleware_factory(injector)
    ]
