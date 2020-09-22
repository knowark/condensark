import os
from pathlib import Path
from typing import Dict, Any


Config = Dict[str, Any]

config: Config = {
    'port': int(os.environ.get('INTEGRARK_PORT', 8765)),
    'auto': bool(os.environ.get('INTEGRARK_AUTO', True)),
    'loglevel': int(os.environ.get('INTEGRARK_LOGLEVEL', 30)),
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
