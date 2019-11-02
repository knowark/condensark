from typing import List, Any
import json


def parse_domain(filter: str) -> List[Any]:
    domain = json.loads(filter)

    return domain
