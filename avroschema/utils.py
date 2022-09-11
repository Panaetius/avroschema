"""Avro utilities."""

import re

NAME_REGEX = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def validate_name(name: str) -> bool:
    """Validate an avro name."""
    if not NAME_REGEX.match(name):
        return False

    return True
