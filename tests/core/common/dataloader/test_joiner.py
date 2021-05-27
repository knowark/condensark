from typing import List, Awaitable, Any, Union
from types import SimpleNamespace as SN
from asyncio import sleep
from modelark import MemoryRepository
from pytest import fixture, raises
from integrark.core import StandardDataLoader, Joiner


@fixture
def join_repository():
    return MemoryRepository().load({
        'default': {
            '001': SN(id='001', name='alpha', reference='x'),
            '002': SN(id='002', name='beta', reference='x'),
            '003': SN(id='003', name='gamma', reference='y'),
        }
    })


@fixture
def link_repository():
    return MemoryRepository().load({
        'default': {
            '001': SN(id='001', color='blue', letter_id='001'),
            '002': SN(id='002', color='blue', letter_id='002'),
            '003': SN(id='003', color='red', letter_id='003'),
        }
    })


def test_join_dataloader_instantiation(join_repository):
    joiner = Joiner(join_repository)

    assert joiner.join is join_repository


async def test_join_dataloader_build(join_repository):
    joiner = Joiner(join_repository)

    dataloader = joiner.build()

    assert isinstance(dataloader, StandardDataLoader)


async def test_join_dataloader_build_many_to_one(join_repository):
    joiner = Joiner(join_repository)

    dataloader = joiner.build()

    future_1 = dataloader.load('001')
    future_2 = dataloader.load('002')

    assert len(dataloader.queue) == 2
    assert future_1.done() is False
    assert future_2.done() is False

    await sleep(0.01)

    assert len(dataloader.queue) == 0
    assert future_1.done() is True
    assert future_2.done() is True

    item_1 = future_1.result()
    item_2 = future_2.result()

    assert item_1.name == 'alpha'
    assert item_2.name == 'beta'


async def test_join_dataloader_build_one_to_many(join_repository):
    joiner = Joiner(join_repository, 'reference')

    dataloader = joiner.build()

    future_1 = dataloader.load('x')
    future_2 = dataloader.load('z')

    assert len(dataloader.queue) == 2
    assert future_1.done() is False
    assert future_2.done() is False

    await sleep(0.01)

    assert len(dataloader.queue) == 0
    assert future_1.done() is True
    assert future_2.done() is True

    item_1 = future_1.result()
    item_2 = future_2.result()

    assert item_1[0].name == 'alpha'
    assert item_1[1].name == 'beta'
    assert item_2 == []


async def test_join_dataloader_build_many_to_many(
    join_repository, link_repository):

    joiner = Joiner(
        join_repository, 'letter_id', link_repository, 'color')

    dataloader = joiner.build()

    future_1 = dataloader.load('blue')
    future_2 = dataloader.load('red')

    assert len(dataloader.queue) == 2
    assert future_1.done() is False
    assert future_2.done() is False

    await sleep(0.01)

    assert len(dataloader.queue) == 0
    assert future_1.done() is True
    assert future_2.done() is True

    item_1 = future_1.result()
    item_2 = future_2.result()

    assert len(item_1) == 2
    assert item_1[0].name == 'alpha'
    assert item_1[1].name == 'beta'
    assert len(item_2) == 1
    assert item_2[0].name == 'gamma'
