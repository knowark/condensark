import os
import sys
import asyncio
import uvloop
from injectark import Injectark
from .infrastructure.core import build_config
from .infrastructure.factories import build_factory
from .infrastructure.cli import Cli


async def main(args=None):  # pragma: no cover
    mode = os.environ.get('INTEGRARK_MODE', 'PROD')
    config_path = os.environ.get('INTEGRARK_CONFIG', 'config.json')
    config = build_config(config_path, mode)

    factory = build_factory(config)
    strategy = config['strategy']

    resolver = Injectark(strategy=strategy, factory=factory)

    await Cli(config, resolver).run(args or [])


if __name__ == '__main__':  # pragma: no cover
    uvloop.install()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sys.argv[1:]))
    loop.close()
