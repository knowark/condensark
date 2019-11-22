from typing import List, Awaitable, Any, Union
from asyncio import Future, isfuture, sleep
from pytest import fixture, raises
from integrark.infrastructure.query.graphql import (
    DataLoader, StandardDataLoader)


def test_dataloader_methods():
    abstract_methods = DataLoader.__abstractmethods__
    assert 'fetch' in abstract_methods


def standard_dataloader() -> DataLoader:
    async def dummy_fetch(ids: List[str]) -> List[Any]:
        return [{'id': id, 'value': f'Response: {id}'} for id in ids]

    return StandardDataLoader(dummy_fetch)


async def test_data_loader_optional_context():
    context = {'data': 'any'}

    dataloader = StandardDataLoader(lambda ids: [], context)

    assert context == dataloader.context


async def test_dataloader_queue():
    dataloader = standard_dataloader()

    future_1 = dataloader.load('1')
    future_2 = dataloader.load('2')
    future_3 = dataloader.load('3')

    assert isfuture(future_1)
    assert isfuture(future_2)
    assert isfuture(future_3)

    assert len(dataloader.queue) == 3


async def test_dataloader_load():
    dataloader = standard_dataloader()

    future_1 = dataloader.load('1')
    future_2 = dataloader.load('2')

    assert len(dataloader.queue) == 2
    assert future_1.done() is False
    assert future_2.done() is False

    await sleep(0.01)

    assert len(dataloader.queue) == 0
    assert future_1.done() is True
    assert future_2.done() is True

    result_1 = await future_1
    result_2 = await future_2

    assert result_1 == {'id': '1', 'value': f'Response: 1'}
    assert result_2 == {'id': '2', 'value': f'Response: 2'}


async def test_dataloader_load_many():
    dataloader = standard_dataloader()

    future_list = dataloader.load_many(['1', '2'])

    assert len(dataloader.queue) == 2
    assert future_list.done() is False

    await sleep(0.01)

    assert len(dataloader.queue) == 0
    assert future_list.done() is True

    result_list = await future_list

    assert result_list == [
        {'id': '1', 'value': f'Response: 1'},
        {'id': '2', 'value': f'Response: 2'}]


async def test_dataloader_cache():
    dataloader = standard_dataloader()

    future_1 = dataloader.load('1')
    future_2 = dataloader.load('2')
    future_3 = dataloader.load('1')

    assert len(dataloader.queue) == 2
    assert future_1.done() is False
    assert future_2.done() is False
    assert future_3.done() is False

    await sleep(0.01)

    assert len(dataloader.queue) == 0
    assert future_1.done() is True
    assert future_2.done() is True
    assert future_3.done() is True

    result_1 = await future_1
    result_2 = await future_2
    result_3 = await future_3

    assert result_1 == {'id': '1', 'value': f'Response: 1'}
    assert result_2 == {'id': '2', 'value': f'Response: 2'}
    assert result_3 == result_1


async def test_dataloader_load_exception():
    async def dummy_fetch(ids: List[str]) -> List[Any]:
        return [
            {'id': '1', 'value': 'Response: 1'},
            Exception('Error at retrieving id: <2>')
        ]

    dataloader = StandardDataLoader(dummy_fetch)

    future_1 = dataloader.load('1')
    future_2 = dataloader.load('2')

    assert len(dataloader.queue) == 2
    assert future_1.done() is False
    assert future_2.done() is False

    await sleep(0.01)

    assert len(dataloader.queue) == 0
    assert future_1.done() is True
    assert future_2.done() is True

    result_1 = await future_1

    with raises(Exception) as execinfo:
        result_2 = await future_2
        assert str(execinfo.value) == 'Error at retrieving id: <2>'

    assert result_1 == {'id': '1', 'value': f'Response: 1'}
