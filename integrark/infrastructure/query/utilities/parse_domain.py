from typing import List, Dict, Any
import json


def parse_domain(filter: str, alias: Dict[str, str] = None) -> List[Any]:
    domain = json.loads(filter)
    if alias:
        for item in domain:
            if isinstance(item, list) and len(item):
                item[0] = alias.get(item[0]) or item[0]

    return domain
