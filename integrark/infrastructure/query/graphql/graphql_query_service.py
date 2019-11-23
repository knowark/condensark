from typing import List, Dict, Any
from graphql import GraphQLSchema, graphql, format_error
from ....application.services import QueryService, QueryResult
from .graphql_schema_loader import GraphqlSchemaLoader
from .graphql_solution_loader import GraphqlSolutionLoader
from .solution import Solution


class GraphqlQueryService(QueryService):

    def __init__(self, schema_loader: GraphqlSchemaLoader,
                 solution_loader: GraphqlSolutionLoader) -> None:
        self.schema = schema_loader.load()
        self.solutions, self.dataloaders_factory = solution_loader.load()
        self.schema = self._bind_schema(self.schema, self.solutions)

    async def run(self, query: str,
                  context: Dict[str, Any] = None) -> QueryResult:
        context = context or {}
        graphql_kwargs = context.pop('graphql', {'context_value': {}})
        graphql_context = graphql_kwargs['context_value']
        graphql_context.update({
            'dataloaders': self.dataloaders_factory(graphql_context)
        })

        graphql_result = await graphql(self.schema, query, **graphql_kwargs)

        data = graphql_result.data
        errors = graphql_result.errors if graphql_result.errors is None else [
            format_error(error) for error in graphql_result.errors]

        return QueryResult(data, errors)

    def _bind_schema(self, schema: GraphQLSchema,
                     solutions: List[Solution]) -> GraphQLSchema:

        for solution in solutions:
            fields = schema.get_type(solution.type).fields
            for name, field in fields.items():
                field.resolve = solution.resolve(name)

        return schema
