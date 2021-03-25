import sys
import inspect
from pathlib import Path
from types import ModuleType
from typing import List, Tuple, Dict, Callable, Any
from importlib.util import spec_from_file_location, module_from_spec
from graphql import GraphQLSchema, build_schema
from .solution import Solution
from .location import Location
from .dataloader import DataLoader


class IntegrationImporter:
    def __init__(self, directory: str) -> None:
        self.path = directory
        self.extension = 'py'
        self.solutions: List[Solution] = []
        self.locations: List[Location] = []
        self.dataloaders_factory: Callable[
            [Any], Dict[str, DataLoader]] = lambda context: {}

    def load(self) -> None:
        package = self._load_package(Path(self.path))
        self.solutions = sorted(
            (self._load_solutions(package) or []), key=lambda s: s.type)
        self.locations = sorted(
            (self._load_locations(package) or []), key=lambda l: l.path)
        self.dataloaders_factory = self._load_dataloaders_factory(package)

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
            inspect.isclass(solution) and solution() or solution
            for solution in getattr(package, 'SOLUTIONS', [])]

    def _load_locations(self, package: ModuleType) -> List[Location]:
        return [
            inspect.isclass(location) and location() or location
            for location in getattr(package, 'LOCATIONS', [])]

    def _load_dataloaders_factory(
            self, package: ModuleType) -> Callable[[Any], Dict[str, Any]]:
        dataloader_classes = getattr(package, 'DATALOADERS', [])
        return lambda context: {
            dataloader_class.__name__: dataloader_class(context)
            for dataloader_class in dataloader_classes}
