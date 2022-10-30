import re
from enum import Enum

__all__ = ["ErrorType", "iqr_outlier", "valid_match_key", "z_score_outlier"]
Z_THRESHOLD = 1.96


class ErrorType(Enum):
    """Enum class for the different error types that can occur with data validation."""
    DEBUG = "green",
    INFO = "white",
    WARNING = "bold_yellow",
    ERROR = "bold_red",
    CRITICAL = "bold_purple"


def z_score_outlier(value: int, mean: float, std: float) -> bool:
    """
    Calculates a z-score for a team's datapoint and checks if it's an outlier within the team's data itself.

    :param value: A team's datapoint (value for year-specific data for a team).
    :param mean: The mean of a team's dataset.
    :param std: The standard deviation of a team's dataset.
    :return: A boolean representing whether or not the datapoint of a team is an outlier within the team's dataset.
    """
    return abs(value - mean) / std > Z_THRESHOLD


def iqr_outlier(value: int, q1: int, q3: int) -> bool:
    """
    Calculates whether or not a team's datapoint is an outlier via if it's within the IQR of the team's dataset.

    :param value: A team's datapoint (value for year-specific data for a team).
    :param q1: An integer representing the start of quartile 1.
    :param q3: An integer representing the start of quartile 3.
    :return: A boolean representing whether or not the datapoint of a team is an outlier within the team's dataset.
    """
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return value < lower_bound or value > upper_bound


def valid_match_key(key: str) -> bool:
    """
    Checks if the match key is valid.

    :param key: Match key as a string (eg 'qm1')
    :return: Boolean representing whether or not a match key is valid.
    """
    # Check if match key is valid via regex
    match_key_format = re.compile(r"(qm[1-9][0-9]{0,3})|(qf[1-4]m[1-3])|(sf[1-2]m[1-3])|(f[1]m[1-3])")
    return bool(re.fullmatch(match_key_format, key))
