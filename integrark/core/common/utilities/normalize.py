import re
import json
from typing import Sequence, Dict, Union, Any
from .format import snake_to_camel, camel_to_snake
from .parse_domain import parse_domain

DATA_TYPE = Union[
    Sequence[Dict[str, Any]], Dict[str, Any], str, int, float, bool]


def normalize(data: DATA_TYPE, format='camel') -> DATA_TYPE:
    if isinstance(data, (str, int, float, bool, type(None))):
        return data

    if isinstance(data, (list, tuple)):
        return [normalize(item, format) for item in data]

    format_function = snake_to_camel if format == 'camel' else camel_to_snake

    normalized_data = {}
    for key, value in data.items():
        if not isinstance(value, (str, int, float, bool)):
            value = normalize(value, format)
        normalized_data[format_function(key)] = value

    return normalized_data


def normalize_domain(filter: str, alias: Dict[str, str] = None,
                     snake=True) -> str:
    return json.dumps(parse_domain(filter, alias, snake))
