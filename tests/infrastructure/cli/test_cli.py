import contextlib
from typing import List
from unittest.mock import Mock
from argparse import ArgumentParser, Namespace
from pytest import raises
from integrark.infrastructure.cli import Cli
from integrark.infrastructure.cli import cli as cli_module


def test_cli_instantiation(cli):
    assert cli is not None


def test_cli_run(cli):
    mock_parse = Mock()
    cli.parse = mock_parse
    argv: List = []
    cli.run(argv)

    assert mock_parse.call_count == 1


def test_cli_parse(cli):
    called = False
    argv = ['serve']
    result = cli.parse(argv)

    assert result is not None


def test_cli_parse_empty_argv(cli):
    with raises(SystemExit) as e:
        result = cli.parse([])


def test_cli_serve(cli, monkeypatch):
    called = False
    application = None
    port = None
    namespace = Namespace()

    def mock_create_app(config, injector):
        nonlocal port
        port = config.get('port')
        return {'Application': 'app'}

    monkeypatch.setattr(
        cli_module, 'create_app', mock_create_app)

    def mock_run_app(app):
        nonlocal called
        called = True
        nonlocal application
        application = app

    monkeypatch.setattr(
        cli_module, 'run_app', mock_run_app)

    namespace.port = 7777

    result = cli.serve(namespace)

    assert called
    assert application == {'Application': 'app'}
    assert port == 7777
