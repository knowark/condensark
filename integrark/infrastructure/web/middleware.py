from typing import Dict, List, Callable, Any
from aiohttp import web
from jwt import PyJWTError
from injectark import Injectark


def user_middleware_factory(injector: Injectark) -> Callable:

    jwt_supplier = injector['JwtSupplier']

    @web.middleware
    async def user_middleware(
            request: web.Request, handler: Callable) -> web.Response:

        authorization = request.headers.get('Authorization', "")
        token = authorization.replace('Bearer ', '')

        try:
            token_payload = jwt_supplier.decode(token)
        except PyJWTError:
            token_payload = {}

        request['user'] = extract_user(token_payload)

        response = await handler(request)

        return response

    return user_middleware


def extract_user(payload: Dict[str, Any]) -> Dict[str, Any]:
    user = {
        'tid': '',
        'uid': '',
        'name': '<<PUBLIC>>',
        'email': '',
        'attributes': {},
        'authorization': {}
    }
    user.update(payload)
    return user


def middlewares(injector: Injectark) -> List[Callable]:
    return [
        user_middleware_factory(injector)
    ]
