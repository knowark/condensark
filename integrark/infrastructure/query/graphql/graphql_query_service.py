from typing import List, Dict, Any
from graphql import GraphQLSchema, graphql
from ....application.services import QueryService, QueryResult
from .graphql_schema_loader import GraphqlSchemaLoader
from .graphql_solution_loader import GraphqlSolutionLoader
from .solution import Solution


class GraphqlQueryService(QueryService):

    def __init__(self, schema_loader: GraphqlSchemaLoader,
                 solution_loader: GraphqlSolutionLoader) -> None:
        self.schema_loader = schema_loader
        self.solution_loader = solution_loader

    async def run(self, query: str,
                  context: Dict[str, Any] = None) -> QueryResult:

        schema = self.schema_loader.load()
        solutions = self.solution_loader.load()
        schema = self._bind_schema(schema, solutions)

        result = await graphql(schema, query, context_value=context)

        return result

    def _bind_schema(self, schema: GraphQLSchema,
                     solutions: List[Solution]) -> GraphQLSchema:

        for solution in solutions:
            fields = schema.get_type(solution.type).fields
            for name, field in fields.items():
                field.resolve = solution.resolve(name)

        return schema
