from ....application.services import QueryService, QueryResult


class GraphqlQueryService(QueryService):

    def __init__(self, response=None) -> None:
        self.response = response or {}

    async def run(self, query: str) -> QueryResult:
        return self.response
