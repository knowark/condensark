
class Solution:
    type = 'Query'

    def resolve(self, field):
        return getattr(self, f'resolve__{field}', None)

    async def resolve__hero(self, parent, info, episode):
        self.human_data = info.context['data']['human_data']
        self.droid_data = info.context['data']['droid_data']

        return (
            self.human_data['1000'] if episode == 5 else
            self.droid_data['2001'])

    async def resolve__human(self, parent, info, id):
        self.human_data = info.context['data']['human_data']
        return self.human_data.get(id)

    async def resolve__droid(self, parent, info, id):
        self.droid_data = info.context['data']['droid_data']
        return self.droid_data.get(id)
