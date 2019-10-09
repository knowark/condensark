from pytest import fixture, raises
from integrark.infrastructure.query.graphql import Solution


@fixture
def solution() -> Solution:
    return Solution()


def test_solution(solution):
    assert solution.type == 'Query'


def test_solution_default_resolver(solution):
    resolver = solution.resolve('any')

    assert resolver(None, None) == []
