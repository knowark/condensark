from typing import Dict, Any


class ExecutionCoordinator:
    def __init__(self) -> None:
        pass

    async def execute(self, query: str) -> Dict[str, Any]:
        result = {'data': query}

        return result
