import sys
from pathlib import Path
from typing import List, Any, Dict
from importlib.util import spec_from_file_location, module_from_spec
from graphql import GraphQLSchema, build_schema
from .solution import Solution


class GraphqlSolutionLoader:
    def __init__(self, directory: str) -> None:
        self.path = directory
        self.extension = 'py'

    def load(self) -> List[Solution]:
        solutions = self._load_solutions_from_package(Path(self.path)) or []
        return sorted(solutions, key=lambda s: s.type)

    def _load_solutions_from_package(self, path: Path) -> List[Solution]:
        package_init = path / '__init__.py'
        if not package_init.exists():
            return None

        spec = spec_from_file_location(
            path.stem, str(package_init.absolute()))
        package = module_from_spec(spec)
        sys.modules[spec.name] = package
        spec.loader.exec_module(package)

        return [solution_class() for solution_class in
                getattr(package, 'SOLUTIONS', [])]
