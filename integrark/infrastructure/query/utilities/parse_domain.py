import re
import json
from typing import List, Dict, Any


def parse_domain(filter: str, alias: Dict[str, str] = None,
                 snake=True) -> List[Any]:
    domain = json.loads(filter)

    for item in domain:
        if isinstance(item, list) and len(item):
            word = item[0]
            if snake:
                word = camel_to_snake(word)
            if alias:
                word = alias.get(item[0]) or word
            item[0] = word

    return domain


def join_domains(domains: List[List[Any]], symbol='|') -> List[Any]:
    or_list = [symbol for item in range(len(domains) - 1)]
    return or_list + domains


def camel_to_snake(word: str) -> str:
    chain = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', word)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', chain).lower()
