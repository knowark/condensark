import os
from pathlib import Path
from typing import Dict, Any


Config = Dict[str, Any]

config: Config = {
    'port': int(os.environ.get('INTEGRARK_PORT', 8765)),
    'auto': bool(os.environ.get('INTEGRARK_AUTO', True)),
    'factory': os.environ.get('INTEGRARK_FACTORY', 'GraphqlFactory'),
    'strategies': os.environ.get(
        'INTEGRARK_STRATEGIES', 'base,rest,graphql').split(','),
    'definitions_directory': os.environ.get(
        'INTEGRARK_DEFINITIONS_DIRECTORY', 'schema/definitions'),
    'integrations_directory': os.environ.get(
        'INTEGRARK_INTEGRATIONS_DIRECTORY', 'schema/integrations'),
    'secrets': {
        'jwt': os.environ.get('INTEGRARK_SECRETS_JWT_FILE',
                              str(Path.home().joinpath('sign.txt')))
    }
}


# class Config(defaultdict, ABC):
# @ abstractmethod
# def __init__(self):
# self['mode'] = 'BASE'
# self['port'] = 8765
# self['strategy'] = {
# "QueryService": {
# "method": "standard_query_service"
# },
# "RouteService": {
# "method": "standard_route_service"
# },
# "ExecutionManager": {
# "method": "execution_manager"
# },
# "RoutingManager": {
# "method": "routing_manager"
# },
# "JwtSupplier": {
# "method": "jwt_supplier"
# },
# "IntegrationImporter": {
# "method": "integration_importer"
# }
# }
# self['schema_definitions_directory'] = 'schema/definitions'
# self['schema_solutions_directory'] = 'schema/solutions/default'
# self['integrations_directory'] = 'integrations/default'
# self['secrets'] = {
# "jwt": str(Path.home().joinpath('sign.txt'))
# }


# class TrialConfig(Config):
# def __init__(self):
# super().__init__()
# self['mode'] = 'TEST'
# self['factory'] = 'TrialFactory'
# self['strategy'].update({

# })


# class DevelopmentConfig(Config):
# def __init__(self):
# super().__init__()
# self["mode"] = 'DEV'
# self['factory'] = 'MemoryFactory'
# self["strategy"].update({

# })


# class ProductionConfig(Config):
# def __init__(self):
# super().__init__()
# self["mode"] = 'PROD'
# self['factory'] = 'GraphqlFactory'
# self["strategy"].update({
# "QueryService": {
# "method": "graphql_query_service"
# },
# "RouteService": {
# "method": "rest_route_service"
# },
# "GraphqlSchemaLoader": {
# "method": "graphql_schema_loader"
# },
# "GraphqlSolutionLoader": {
# "method": "graphql_solution_loader"
# }
# })
