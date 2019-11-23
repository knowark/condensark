from asyncio import sleep
from integrark.tools import DataLoader


class DroidLoader(DataLoader):

    async def fetch(self, site_ids):
        await sleep(0.1)
        return []


class EpisodeLoader(DataLoader):

    async def fetch(self, user_ids):
        await sleep(0.1)
        return []
