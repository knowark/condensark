from injectark import StrategyBuilder
from .base import base
from .check import check
from .graphql import graphql
from .rest import rest


strategy_builder = StrategyBuilder({
    'base': base,
    'check': check,
    'graphql': graphql,
    'rest': rest
})
