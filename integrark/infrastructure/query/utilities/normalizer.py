import re
from typing import Sequence, Dict, Union, Any

DATA_TYPE = Union[Sequence[Dict[str, Any]], Dict[str, Any]]


def normalize(data: DATA_TYPE, format='camel') -> DATA_TYPE:
    if isinstance(data, (list, tuple)):
        return [normalize(item, format) for item in data]

    format_function = snake_to_camel if format == 'camel' else camel_to_snake

    normalized_data = {}
    for key, value in data.items():
        if not isinstance(value, (str, int, float, bool)):
            value = normalize(value, format)
        normalized_data[format_function(key)] = value

    return normalized_data


def camel_to_snake(word: str) -> str:
    chain = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', word)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', chain).lower()


def snake_to_camel(value: str) -> str:
    title_case = value.title().replace("_", "")
    return title_case[0].lower() + title_case[1:]
