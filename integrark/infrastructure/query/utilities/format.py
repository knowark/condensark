import re

# Adapted from:
# https://github.com/okunishinishi/python-stringcase


def camel_to_snake(value: str) -> str:
    value = re.sub(r"[\-\.\s]", '_', str(value))
    return (value[0].lower() +
            re.sub(r"[A-Z]",
                   lambda matched: '_' + matched.group(0).lower(), value[1:]))


def snake_to_camel(value: str) -> str:
    value = re.sub(r"^[\-_\.]", '', str(value))
    return (value[0].lower() +
            re.sub(r"[\-_\.\s]([A-Za-z])",
                   lambda matched: matched.group(1).upper(), value[1:]))
