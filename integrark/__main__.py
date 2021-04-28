import sys
import logging
import asyncio
import uvloop
from injectark import Injectark
from .presenters.shell import Shell
from .factories import factory_builder
from .core import config


async def main(args=None):  # pragma: no cover
    logging.basicConfig()
    logging.getLogger().setLevel(config['loglevel'])
    factory = factory_builder.build(config)
    injector = Injectark(factory=factory)

    await Shell(config, injector).run(args or [])


if __name__ == '__main__':  # pragma: no cover
    uvloop.install()
    asyncio.run(main(sys.argv[1:]))
