import json
from itertools import chain

from falconscoutcore.data_validation.base_data_val import BaseDataValidation
from falconscoutcore.data_validation.config.constants import ChargedUp
from falconscoutcore.data_validation.config.utils import (ErrorType, get_intersection_of_n_series)
from numpy import logical_or
from pandas import DataFrame, Series, concat, isna, notna


class DataValidation2025(BaseDataValidation):
    def __init__(self, path_to_config: str = "config.yaml"):
        super().__init__(path_to_config)
