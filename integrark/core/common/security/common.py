from typing import List, Any, Protocol, TypedDict
from modelark import Repository


class AuthorizationError(Exception):
    pass


class User(TypedDict):
    id: str
    roles: List[str]


class SecurityContext(TypedDict):
    user: User
    request: Any


class Resolver(Protocol):
    def resolve(self, target: str) -> Repository:
        """Resolve method to be provided"""
