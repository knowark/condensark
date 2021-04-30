from typing import List, Awaitable, Any, Union
from types import SimpleNamespace as SN
from asyncio import sleep
from modelark import MemoryRepository
from pytest import fixture, raises
from integrark.core import StandardDataLoader, Joiner


@fixture
def join_repository():
    repository = MemoryRepository()
    repository.load({
        'default': {
            '001': SN(id='001', name='alpha', reference='x'),
            '002': SN(id='002', name='beta', reference='x'),
            '003': SN(id='003', name='gamma', reference='y'),
        }
    })

    return repository


# @fixture
# def link_repository():
    # repository = MemoryRepository()
    # repository.load({
        # 'default': {
            # '001': SN(id='001', name='alpha'),
            # '002': SN(id='002', name='beta'),
            # '003': SN(id='003', name='gamma'),
        # }
    # })

    # return repository


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
    joiner = Joiner(join_repository)
    joiner.target = 'reference'

    dataloader = joiner.build()

    future_1 = dataloader.load('x')

    assert len(dataloader.queue) == 1
    assert future_1.done() is False

    await sleep(0.01)

    assert len(dataloader.queue) == 0
    assert future_1.done() is True

    item_1 = future_1.result()

    assert item_1[0].name == 'alpha'
    assert item_1[1].name == 'beta'
