from ..core import Config
from .memory_factory import MemoryFactory
from ..query import GraphqlQueryService
from ..query.graphql import GraphqlSchemaLoader, GraphqlSolutionLoader


class GraphqlFactory(MemoryFactory):
    def __init__(self, config: Config) -> None:
        self.config = config

    def graphql_query_service(
            self, schema_loader: GraphqlSchemaLoader,
            solution_loader: GraphqlSolutionLoader) -> GraphqlQueryService:
        return GraphqlQueryService(schema_loader, solution_loader)

    def graphql_schema_loader(self) -> GraphqlSchemaLoader:
        definitions_directory = self.config['schema_definitions_directory']
        return GraphqlSchemaLoader(definitions_directory)

    def graphql_solution_loader(self) -> GraphqlSolutionLoader:
        solutions_directory = self.config['schema_solutions_directory']
        return GraphqlSolutionLoader(solutions_directory)
