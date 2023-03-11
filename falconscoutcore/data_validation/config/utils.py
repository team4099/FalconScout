import re
from enum import Enum

from pandas import isna


class ErrorType(Enum):
    """Enum class for the different error types that can occur with the data validation."""

    DEBUG = 1
    INFO = 2
    WARNING = 3
    EXTRA_DATA = 4
    INCORRECT_DATA = 5
    MISSING_DATA = 6
    CRITICAL = 7
    RESCOUT_MATCH = 8


def valid_match_key(key: str) -> bool:
    """
    Checks if the match key is valid.

    :param key: Match key as a string (eg 'qm1')
    :return: Boolean representing whether or not a match key is valid.
    """
    if isna(key):
        return False

    # Check if match key is valid via regex
    match_key_format = re.compile(
        r"(qm[1-9][0-9]{0,3})|(qf[1-4]m[1-3])|(sf[1-2]m[1-3])|(f[1]m[1-3])"
    )
    return bool(re.fullmatch(match_key_format, key))
