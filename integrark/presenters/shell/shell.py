import sys
import json
import logging
from argparse import ArgumentParser, Namespace
from injectark import Injectark
from typing import List
from ...core import Config
from ..rest import create_app, run_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Shell:
    def __init__(self, config: Config, injector: Injectark) -> None:
        self.config = config
        self.injector = injector
        self.parser = ArgumentParser('Integrark')

    async def run(self, argv: List[str]):
        args = await self.parse(argv)
        await args.func(args)

    async def parse(self, argv: List[str]) -> Namespace:
        subparsers = self.parser.add_subparsers()

        # Serve
        serve_parser = subparsers.add_parser(
            'serve', help='Start HTTP server.')
        serve_parser.add_argument('-p', '--port')
        serve_parser.set_defaults(func=self.serve)

        if len(argv) == 0:
            self.parser.print_help()
            self.parser.exit()

        return self.parser.parse_args(argv)

    async def serve(self, args: Namespace) -> None:
        logger.info('SERVE')
        port = args.port or self.config['port']
        app = create_app(self.config, self.injector)
        await run_app(app, port)
