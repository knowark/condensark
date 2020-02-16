from typing import Dict, Callable, Any


class Location:
    path = ''

    def route(self, context: Dict[str, Any]) -> Any:
        return f"REST Proxy. Context: {context}"
