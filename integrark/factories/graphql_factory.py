from ..core import Config, IntegrationImporter
from ..core.query import GraphqlQueryService
from ..core.query.graphql import GraphqlSchemaLoader
from .rest_factory import RestFactory


class GraphqlFactory(RestFactory):
    def __init__(self, config: Config) -> None:
        self.config = config

    def graphql_query_service(
            self, schema_loader: GraphqlSchemaLoader,
            integration_importer: IntegrationImporter) -> GraphqlQueryService:
        return GraphqlQueryService(schema_loader, integration_importer)

    def graphql_schema_loader(self) -> GraphqlSchemaLoader:
        definitions_directory = self.config['definitions_directory']
        return GraphqlSchemaLoader(definitions_directory)
