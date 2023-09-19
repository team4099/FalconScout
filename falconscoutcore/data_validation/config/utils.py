import re
from enum import Enum
from functools import reduce

from pandas import DataFrame, Series, isna


class ErrorType(Enum):
    """Enum class for the different error types that can occur with the data validation."""

    RESCOUT_MATCH = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    EXTRA_DATA = 4
    INCORRECT_DATA = 5
    MISSING_DATA = 6
    CRITICAL = 7


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


def get_intersection_of_n_series(*args: Series) -> tuple[list, bool, bool]:
    intersected_result = list(reduce(lambda x, y: set(x).intersection(set(y)), args))
    return (
        intersected_result,
        len({len(scouting_datum) for scouting_datum in args}) == 1,
        (DataFrame(*args).astype(str).nunique() == 1).all(),
    )
