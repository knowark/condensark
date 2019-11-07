from typing import Dict, Any


class Authorizer:
    def __init__(self, permissions: Dict[str, Any] = None,
                 default_resource='default',
                 default_operation='create',
                 read_operation='read') -> None:
        self.permissions = permissions or {}
        self.default_resource = default_resource
        self.default_operation = default_operation
        self.read_operation = read_operation

    def check(self, user, resource: str = None, operation: str = None):
        resource = resource or self.default_resource
        operation = operation or self.default_operation

        roles = user['roles']
        resource_permissions = self.permissions.get(resource, {})
        required_roles = resource_permissions.get(operation, [])

        authorized = any(role in required_roles for role in roles)
        if not authorized:
            raise AuthorizationError(
                f"User <{user['name']}> not authorized.")


class AuthorizationError(Exception):
    pass
