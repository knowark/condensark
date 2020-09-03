from typing import Dict, Any
from injectark import FactoryBuilder
from .base_factory import BaseFactory
from .check_factory import CheckFactory
from .rest_factory import RestFactory
from .graphql_factory import GraphqlFactory
from .strategies import strategy_builder


factory_builder = FactoryBuilder([
    BaseFactory, CheckFactory, RestFactory, GraphqlFactory])

__all__ = [
    'strategy_builder',
    'factory_builder'
]
