import contextlib
from typing import List
from unittest.mock import AsyncMock
from argparse import ArgumentParser, Namespace
from pytest import raises
from integrark.infrastructure.shell import Shell
from integrark.infrastructure.shell import shell as shell_module


def test_shell_instantiation(shell):
    assert shell is not None


async def test_shell_run(shell):
    mock_parse = AsyncMock()
    shell.parse = mock_parse
    argv: List = []
    await shell.run(argv)

    assert mock_parse.call_count == 1


async def test_shell_parse(shell):
    called = False
    argv = ['serve']
    result = await shell.parse(argv)

    assert result is not None


async def test_shell_parse_empty_argv(shell):
    with raises(SystemExit) as e:
        result = await shell.parse([])


async def test_shell_serve(shell, monkeypatch):
    called = False
    application = None
    port = None
    namespace = Namespace()

    def mock_create_app(config, injector):

        return {'Application': 'app'}

    monkeypatch.setattr(
        shell_module, 'create_app', mock_create_app)

    async def mock_run_app(app, port_):
        nonlocal called
        nonlocal port
        nonlocal application
        called = True
        port = port_
        application = app

    monkeypatch.setattr(
        shell_module, 'run_app', mock_run_app)

    namespace.port = 7777

    result = await shell.serve(namespace)

    assert called
    assert application == {'Application': 'app'}
    assert port == 7777
