
class Solution:
    type = 'Query'

    def __init__(self, config):
        self.config = config
        self.data = self.config['data']
        self.human_data = self.data['human_data']
        self.droid_data = self.data['droid_data']

    def resolve(self, field):
        return getattr(self, f'resolve__{field}')

    def resolve__hero(self, parent, info, episode):
        return (
            self.human_data['1000'] if episode == 5 else
            self.droid_data['2001'])

    def resolve__human(self, parent, info, id):
        return self.human_data.get(id)

    def resolve__droid(self, parent, info, id):
        return self.droid_data.get(id)
