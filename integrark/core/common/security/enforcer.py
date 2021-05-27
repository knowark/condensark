import json
from itertools import groupby
from operator import itemgetter
from modelark import Repository, Domain
from filtrark import SafeEval
from .common import AuthorizationError, SecurityContext, Resolver


class Enforcer:
    def __init__(self, resolver: Resolver) -> None:
        self.safe_eval = SafeEval(prefix='')
        self.resolver = resolver
        self.policy_repository = self.resolver.resolve('policy')
        self.restriction_repository = self.resolver.resolve('restriction')

    async def check(self, resource: str, operation: str,
                    context: SecurityContext) -> None:
        policies = await self._get_policies(resource, context)
        privileges = "".join([policy.privilege for policy in policies])
        if operation not in privileges:
            raise AuthorizationError(
                f'Operation <{operation}> for resource <{resource}> '
                f'missing in roles {context["user"]["roles"]}')

    async def secure(self, resource: str,
                     context: SecurityContext) -> Domain:
        policies = await self._get_policies(resource, context)
        restrictions = await self.restriction_repository.search(
            [('policy_id', 'in', [policy.id for policy in policies])])

        domain = []
        for _, items in groupby(restrictions, key=lambda item: item.policy_id):
            domain.extend(await self._compute_domain(context, items))

        return domain

    async def _get_policies(self, resource: str, context: SecurityContext):
        user = context['user']
        role_ids = [role.split('|')[-1] for role in user['roles']]
        return await self.policy_repository.search(
            [('resource', '=', resource), ('role_id', 'in', role_ids)])

    async def _compute_domain(self, context, restrictions) -> Domain:
        restrictions = sorted(restrictions, key=lambda item: item.sequence)
        last_restriction = restrictions.pop()
        for restriction in restrictions:
            domain = self.safe_eval(restriction.domain, context)
            repository = self.resolver.resolve(restriction.target)
            context['previous'] = await repository.search(domain)
        return self.safe_eval(last_restriction.domain, context)
