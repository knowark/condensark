from typing import List, Dict, Any
from graphql import GraphQLSchema, graphql, format_error
from ....application.services import QueryService, QueryResult
from ...core import IntegrationImporter, Solution
from .graphql_schema_loader import GraphqlSchemaLoader


class GraphqlQueryService(QueryService):

    def __init__(self, schema_loader: GraphqlSchemaLoader,
                 integration_importer: IntegrationImporter) -> None:
        self.schema = schema_loader.load()
        self.solutions = integration_importer.solutions
        self.dataloaders_factory = integration_importer.dataloaders_factory
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
