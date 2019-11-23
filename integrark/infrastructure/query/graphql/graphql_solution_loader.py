import sys
from pathlib import Path
from types import ModuleType
from typing import List, Tuple, Dict, Any
from importlib.util import spec_from_file_location, module_from_spec
from graphql import GraphQLSchema, build_schema
from .solution import Solution
from .dataloader import DataLoader


class GraphqlSolutionLoader:
    def __init__(self, directory: str) -> None:
        self.path = directory
        self.extension = 'py'

    def load(self) -> Tuple[List[Solution], Dict[str, DataLoader]]:
        package = self._load_package(Path(self.path))
        solutions = self._load_solutions(package) or []
        dataloaders = self._load_dataloaders_factory(package)
        return (sorted(solutions, key=lambda s: s.type), dataloaders)

    def _load_package(self, path: Path) -> ModuleType:
        package_init = path / '__init__.py'
        if not package_init.exists():
            return None

        spec = spec_from_file_location(
            path.stem, str(package_init.absolute()))
        package = module_from_spec(spec)
        sys.modules[spec.name] = package
        spec.loader.exec_module(package)

        return package

    def _load_solutions(self, package: ModuleType) -> List[Solution]:
        return [
            solution_class() for solution_class in
            getattr(package, 'SOLUTIONS', [])]

    def _load_dataloaders_factory(
            self, package: ModuleType) -> Dict[str, DataLoader]:
        dataloader_classes = getattr(package, 'DATALOADERS', [])
        return lambda context: {
            dataloader_class.__name__: dataloader_class(context)
            for dataloader_class in dataloader_classes}
