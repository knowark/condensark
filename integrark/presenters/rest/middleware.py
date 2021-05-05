import logging
from json import dumps
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


def errors_middleware_factory(injector: Injectark) -> Callable:

    @web.middleware
    async def middleware(request: web.Request, handler: Callable):
        try:
            return await handler(request)
        except Exception as error:
            type_ = type(error).__name__
            status = getattr(error, 'status', 500)
            message = str(error)

            logging.exception('Service Error')

            return web.json_response({"errors": [{
                "type": type_,
                "message": message,
            }]}, status=status, dumps=dumps)

    return middleware


def extract_user(payload: Dict[str, Any]) -> Dict[str, Any]:
    user = {
        'tid': '',
        'uid': '',
        'tenant': '',
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
        user_middleware_factory(injector),
        errors_middleware_factory(injector)
    ]
