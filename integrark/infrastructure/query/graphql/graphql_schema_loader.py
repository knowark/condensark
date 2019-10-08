from pathlib import Path
from typing import List
from graphql import GraphQLSchema, build_schema


class GraphqlSchemaLoader:
    def __init__(self, directory: str) -> None:
        self.directory = directory
        self.extensions = ['gql', 'graphql']

    def load(self) -> GraphQLSchema:
        graphql_files: List[Path] = []
        for extension in self.extensions:
            graphql_files.extend(Path(self.directory).glob(
                f"**/*.{extension}"))

        content = self._join_graphql_files(graphql_files)
        schema = build_schema(content)

        return schema

    def _join_graphql_files(self, graphql_files: List[Path]) -> str:
        joined_content = ""

        for graphql_file in graphql_files:
            joined_content += graphql_file.read_text()
            joined_content += '\n'

        return joined_content
