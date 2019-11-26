import json
from typing import List, Dict, Any
from .normalizer import camel_to_snake


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
    if not domains:
        return []

    or_list = []
    for item in domains[:-1]:
        or_list.append(symbol)
        or_list.append(item)
    or_list.append(domains[-1])

    return or_list
