import json
from jwt import decode, InvalidTokenError


class JwtSupplier:
    def __init__(self, secret: str) -> None:
        self.secret = secret

    def encode(self):
        return

    def decode(self, token: str, secret=None, verify=True):
        secret = secret or self.secret
        try:
            return decode(
                token, secret, verify=verify, algorithms=['HS256'])
        except InvalidTokenError:
            return None
