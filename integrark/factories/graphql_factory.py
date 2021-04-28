from ..application.services import QueryService
from ..core import Config, IntegrationImporter
from ..core.query import GraphqlQueryService
from ..core.query.graphql import GraphqlSchemaLoader
from .rest_factory import RestFactory


class GraphqlFactory(RestFactory):
    def __init__(self, config: Config) -> None:
        self.config = config

    def query_service(
            self, integration_importer: IntegrationImporter) -> QueryService:
        definitions_directory = self.config['definitions_directory']
        schema_loader = GraphqlSchemaLoader(definitions_directory)
        return GraphqlQueryService(schema_loader, integration_importer)
