import json

from base_data_val import BaseDataValidation
from utils import *


class DataValidation2022(BaseDataValidation):
    def __init__(self, path_to_config: str = "config.yaml"):
        super().__init__(path_to_config)

    def validate_data(self) -> None:
        """Runs all checks for validating data from 2022's game (Rapid React)."""
        with open(self.path_to_data_file) as file:
            scouting_data = sorted(json.load(file), key=lambda data: data["match_key"])

        self.check_team_numbers_for_each_match(scouting_data)

        for submission in scouting_data:
            if not submission["team_number"]:
                self.add_error(
                    f"NO TEAM NUMBER for match {submission['match_key']}",
                    error_type=ErrorType.CRITICAL,
                )
                continue

            self.validate_submission(submission)

        self.output_errors()

    def validate_submission(self, submission: dict) -> None:
        """
        Runs all checks validating a single submission from 2022's game (Rapid React).

        :param submission: Dictionary containing data scouted.
        :return:
        """
        # Validates match schedule
        self.check_submission_with_match_schedule(submission)
