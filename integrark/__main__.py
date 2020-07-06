import os
import sys
import asyncio
import logging
import uvloop
from injectark import Injectark
from .core import build_config
from .factories import build_factory
from .presenters.shell import Shell


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main(args=None):  # pragma: no cover
    config_path = os.environ.get('INTEGRARK_CONFIG', 'config.json')
    logger.info(f'Configuration: {config_path}')
    config = build_config(config_path, 'PROD')

    factory = build_factory(config)
    strategy = config['strategy']

    resolver = Injectark(strategy=strategy, factory=factory)

    await Shell(config, resolver).run(args or [])


if __name__ == '__main__':  # pragma: no cover
    uvloop.install()
    asyncio.run(main(sys.argv[1:]))
