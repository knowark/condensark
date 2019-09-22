import contextlib
from typing import List
from unittest.mock import Mock
from argparse import ArgumentParser, Namespace
from pytest import raises
from integrark.infrastructure.cli import Cli


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
    namespace = Namespace()

    result = cli.serve(namespace)

#     assert called
