from typing import List, Dict, Any
from graphql import GraphQLSchema, graphql
from ....application.services import QueryService, QueryResult
from .graphql_schema_loader import GraphqlSchemaLoader
from .graphql_solution_loader import GraphqlSolutionLoader
from .solution import Solution


class GraphqlQueryService(QueryService):

    def __init__(self, schema_loader: GraphqlSchemaLoader,
                 solution_loader: GraphqlSolutionLoader) -> None:
        self.schema = schema_loader.load()
        self.solutions = solution_loader.load()

    async def run(self, query: str,
                  context: Dict[str, Any] = None) -> QueryResult:

        schema = self._bind_schema(self.schema, self.solutions)

        graphql_result = await graphql(schema, query, context_value=context)

        data = graphql_result.data
        errors: List[Dict[str, Any]] = []

        for graphql_error in graphql_result.errors or []:
            error: Dict[str, Any] = {'message': graphql_error.message}

            if graphql_error.locations:
                error['locations'] = [
                    {'line': location.line, 'column': location.column}
                    for location in graphql_error.locations]
            if graphql_error.path:
                error['path'] = [item for item in graphql_error.path]
            errors.append(error)

        return QueryResult(data, errors)

    def _bind_schema(self, schema: GraphQLSchema,
                     solutions: List[Solution]) -> GraphQLSchema:

        for solution in solutions:
            fields = schema.get_type(solution.type).fields
            for name, field in fields.items():
                field.resolve = solution.resolve(name)

        return schema
