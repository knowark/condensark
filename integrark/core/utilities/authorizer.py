from typing import List, Dict, Any
from .parse_domain import parse_domain, join_domains


class Authorizer:
    def __init__(self, permissions: Dict[str, Any] = None,
                 default_resource='default',
                 default_operation='create',
                 read_operation='read') -> None:
        self.permissions = permissions or {}
        self.default_resource = default_resource
        self.default_operation = default_operation
        self.read_operation = read_operation

    def check(self, user: Dict[str, Any], resource: str = None,
              operation: str = None):
        resource = resource or self.default_resource
        operation = operation or self.default_operation

        roles = user['roles']
        resource_permissions = self.permissions.get(resource, {})
        required_roles = resource_permissions.get(operation, [])

        authorized = any(role in required_roles for role in roles)
        if not authorized:
            raise AuthorizationError(
                f"User <{user['name']}> not authorized.")

    def secure(self, domain: str, user: Dict[str, Any],
               resource: str = None, operation: str = None) -> List[Any]:
        original_domain = parse_domain(domain)
        resource = resource or self.default_resource
        operation = operation or self.read_operation

        secured_domain = []

        roles = user['roles']
        resource_permissions = self.permissions.get(resource, {})
        read_functions = resource_permissions.get(operation, [])

        authorized = any(role in read_functions for role in roles)
        if not authorized:
            raise AuthorizationError(
                f"User <{user['name']}> not authorized.")

        for role in roles:
            read_function = read_functions.get(role)
            if read_function:
                read_domain = read_function(user)
                if not read_domain:
                    continue
                secured_domain.append(read_domain)

        secured_domain = original_domain + join_domains(secured_domain)

        return secured_domain


class AuthorizationError(Exception):
    pass
