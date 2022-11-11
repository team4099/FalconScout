import json
from typing import Hashable

from base_data_val import BaseDataValidation
from pandas import DataFrame, Series
from utils import ErrorType


class DataValidation2022(BaseDataValidation):
    def __init__(self, path_to_config: str = "config.yaml"):
        super().__init__(path_to_config)

    def validate_data(self, scouting_data: list = None) -> None:
        """
        Runs all checks for validating data from 2022's game (Rapid React).

        :param scouting_data: Optional parameter containing scouting data mostly for testing purposes.
        :return:
        """
        # Loads in scouting data if not passed in.
        if scouting_data is None:
            with open(self.path_to_data_file) as file:
                scouting_data = sorted(
                    json.load(file), key=lambda data: data["match_key"]
                )

        # Converts JSON to DataFrame
        scouting_data = DataFrame.from_dict(scouting_data)

        # TODO: Add check to make sure that teams aren't double scouted or have been scouted (check Notion doc.)
        ...

        # Validates individual submissions
        for _, submission in scouting_data.iterrows():
            if not submission["team_number"]:
                self.add_error(
                    f"NO TEAM NUMBER for match {submission['match_key']}",
                    error_type=ErrorType.CRITICAL,
                )
                continue

            self.validate_submission(submission)

        # TODO: Add check relying on TBA to cross-check shooting totals with TBA's reported shooting totals.
        if self._run_tba_checks:
            ...

        self.output_errors()

    def validate_submission(self, submission: Series) -> None:
        """
        Runs all checks validating a single submission from 2022's game (Rapid React).

        :param submission: Series object containing a single submission of scouting data.
        :return:
        """
        # TODO: Add check to validate match schedule (see Notion doc for more information.)
        ...

        # TODO: Add more data-specific checks (see Notion doc for which checks to add.)
        self.check_for_missing_shooting_zones(
            match_key=submission["match_key"],
            team_number=submission["team_number"],
            auto_lower_hub=submission["auto_lower_hub"],
            auto_upper_hub=submission["auto_upper_hub"],
            auto_misses=submission["auto_misses"],
            auto_shooting_zones=submission["auto_shooting_zones"],
            teleop_lower_hub=submission["teleop_lower_hub"],
            teleop_upper_hub=submission["teleop_upper_hub"],
            teleop_misses=submission["teleop_misses"],
            teleop_shooting_zones=submission["teleop_shooting_zones"],
        )

        self.check_for_invalid_defense_data(
            match_key=submission["match_key"],
            team_number=submission["team_number"],
            defense_pct=submission["defense_pct"],
            counter_defense_pct=submission["counter_defense_pct"],
            defense_rating=submission["defense_rating"],
            counter_defense_rating=submission["counter_defense_rating"],
        )

        self.check_for_auto_great_than_6(
            match_key=submission["match_key"],
            team_number=submission["team_number"],
            auto_lower_hub=submission["auto_lower_hub"],
            auto_upper_hub=submission["auto_upper_hub"],
            auto_misses=submission["auto_misses"],
        )

        # TODO: Add TBA-related checks (see Notion docs for which checks to add.)
        ...

    def check_for_missing_shooting_zones(
        self,
        match_key: str,
        team_number: int,
        auto_lower_hub: int,
        auto_upper_hub: int,
        auto_misses: int,
        auto_shooting_zones: str,
        teleop_lower_hub: int,
        teleop_upper_hub: int,
        teleop_misses: int,
        teleop_shooting_zones: str,
    ) -> None:
        """
        Checks if robot shot balls in autonomous or teleoperated periods but scouter didn't select any shooting zones.

        :param match_key: Key of match that was scouted.
        :param team_number: Number of team that was scouted (eg 4099).
        :param auto_lower_hub: Number of balls shot into the lower hub during Autonomous.
        :param auto_upper_hub: Number of balls shot into the upper hub during Autonomous.
        :param auto_misses: Number of balls missed when shooting during Autonomous.
        :param auto_shooting_zones: Different zones where the scouted robot shot in during Autonomous.
        :param teleop_lower_hub: Number of balls shot into the lower hub during Teleop.
        :param teleop_upper_hub: Number of balls shot into the upper hub during Teleop.
        :param teleop_misses: Number of balls missed when shooting during Teleop.
        :param teleop_shooting_zones: Different zones where the scouted robot shot in during Teleop.
        :return:
        """
        # Checks auto shooting zones
        balls_shot_in_auto = auto_lower_hub + auto_upper_hub + auto_misses
        if balls_shot_in_auto and not auto_shooting_zones:
            self.add_error(
                f"In {match_key}, {team_number} MISSING AUTO SHOOTING ZONES",
                error_type=ErrorType.MISSING_DATA,
            )

        # Checks teleop shooting zones
        balls_shot_in_teleop = teleop_lower_hub + teleop_upper_hub + teleop_misses
        if balls_shot_in_teleop and not teleop_shooting_zones:
            self.add_error(
                f"In {match_key}, {team_number} MISSING TELEOP SHOOTING ZONES",
                error_type=ErrorType.MISSING_DATA,
            )

    def check_for_auto_great_than_6(
            self,
            match_key: str,
            team_number: int,
            auto_lower_hub: int,
            auto_upper_hub: int,
            auto_misses: int,
    ) -> None:
        """
        Checks if robot shot balls in autonomous and scouter states robot shot more than 6 cargo.

        :param match_key: Key of match that was scouted.
        :param team_number: Number of team that was scouted (eg 4099).
        :param auto_lower_hub: Number of balls shot into the lower hub during Autonomous.
        :param auto_upper_hub: Number of balls shot into the upper hub during Autonomous.
        :param auto_misses: Number of balls missed when shooting during Autonomous.
        :return:
        """
        # Checks auto ball shot count
        balls_shot_in_auto = auto_lower_hub + auto_upper_hub + auto_misses
        if balls_shot_in_auto > 6:
            self.add_error(
                f"In {match_key}, {team_number} INCORRECT AUTO SHOT COUNT",
                error_type=ErrorType.INCORRECT_DATA,
            )