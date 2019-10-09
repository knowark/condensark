from pathlib import Path
from typing import List, Any, Dict
from importlib.util import spec_from_file_location, module_from_spec
from graphql import GraphQLSchema, build_schema
from .solution import Solution


class GraphqlSolutionLoader:
    def __init__(self, directory: str, config: Dict[str, Any] = None) -> None:
        self.path = directory
        self.config = config or {}
        self.extension = 'py'

    def load(self, config: Dict['str', Any]) -> List[Solution]:
        solutions = []
        for solution_file in Path(self.path).rglob(f'*.{self.extension}'):
            solution = self._load_solution_file(config, solution_file)
            if solution:
                solutions.append(solution)

        return sorted(solutions, key=lambda s: s.type)

    def _load_solution_file(
            self, config: Dict['str', Any], path: Path) -> Solution:
        spec = spec_from_file_location(path.stem, str(path))
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        Solution = getattr(module, 'Solution', None)
        if not Solution:
            return None

        return Solution(config)
