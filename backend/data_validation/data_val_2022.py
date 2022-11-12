import json

from base_data_val import BaseDataValidation
from pandas import DataFrame, Series, isna, notna
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

        # TODO: Add TBA-related checks (see Notion docs for which checks to add.)
        if self._run_tba_checks:
            self.check_submission_with_tba(
                match_key=submission["match_key"],
                team_number=submission["team_number"],
                alliance=submission["alliance"],
                driver_station=submission["driver_station"],
                taxied=submission["taxied"],
                final_climb_type=submission["final_climb_type"],
            )

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

    def check_submission_with_tba(
        self,
        match_key: str,
        team_number: int,
        alliance: str,
        driver_station: int,
        taxied: float,
        final_climb_type: str,
    ) -> None:

        """
        Validates taxi state and final climb status for scouted robot with TBA data.

        :param match_key: Key of match that was scouted.
        :param team_number: Number of team that was scouted (eg 4099).
        :param alliance: Either "Red" or "Blue"; represents the alliance the scouted team was on.
        :param driver_station: Number representing which order in the alliance a team is (eg 1 for Red 1)
        :param taxied: Represents whether a team taxied or not during Autonomous.
        :param final_climb_type: Represents the rung the scouted team got to in endgame, if any.
        :return: None
        """

        submission_key = match_key.strip().lower()
        full_match_key = f"{self._event_key}_{submission_key}"
        score_info = self.tba_match_data[full_match_key]["score_breakdown"]

        if score_info:
            tba_taxi = score_info[alliance.lower()][f"taxiRobot{driver_station}"]
            tba_climb = score_info[alliance.lower()][f"endgameRobot{driver_station}"]

            # check for inconsistent taxi
            if (tba_taxi == "No" and (notna(taxied) or taxied)) or (
                tba_taxi == "Yes" and (isna(taxied) or not taxied)
            ):
                self.add_error(
                    f"In {match_key}, {team_number} INCORRECT TAXI according to TBA",
                    error_type=ErrorType.INCORRECT_DATA,
                )

            # check for inconsistent climb type
            if tba_climb != final_climb_type.replace("No Climb", "None"):
                self.add_error(
                    f"In {match_key}, {team_number} INCORRECT ClIMB TYPE according to TBA, should be {tba_climb}",
                    error_type=ErrorType.INCORRECT_DATA,
                )

    def check_for_invalid_defense_data(
        self,
        match_key: str,
        team_number: int,
        defense_pct: float,
        defense_rating: float,
        counter_defense_pct: float,
        counter_defense_rating: float,
    ) -> None:
        """
        Checks if scouter gave defense or counter defense rating but stated that the robot didn't play defense/counter defense.
        Checks if scouter stated that robot played defense or counter defense but didn't give a corresponding rating.
        Checks if total defense played + counter defense played > 100% hence impossible.

        :param match_key: Key of match that was scouted.
        :param team_number: Number of team that was scouted (eg 4099).
        :param defense_pct: Decimal representing how much the scouted team played defense out of 1 (eg 0.75)
        :param defense_rating: Representing how well the scouted team played defense on a scale of 1 to 5.
        :param counter_defense_pct: Decimal representing how much the scouted team played counter defense out of 1 (eg 0.75)
        :param counter_defense_rating: Representing how well the scouted team played counter defense on a scale of 1 to 5.
        :return: None
        """  # noqa
        # Check for missing defense pct.
        if notna(defense_rating) and isna(defense_pct):
            self.add_error(
                f"In {match_key}, {team_number} rated for defense but NO DEFENSE PCT",
                error_type=ErrorType.MISSING_DATA,
            )

        # Check for missing defense rating.
        if isna(defense_rating) and notna(defense_pct):
            self.add_error(
                f"In {match_key}, {team_number} MISSING DEFENSE RATING",
                error_type=ErrorType.MISSING_DATA,
            )

        # Check for 0% counter defense pct but given rating.
        if notna(counter_defense_rating) and isna(counter_defense_pct):
            self.add_error(
                f"In {match_key}, {team_number} "
                f"rated for counter defense but NO COUNTER DEFENSE PCT",
                error_type=ErrorType.MISSING_DATA,
            )

        # Check for missing counter defense rating.
        if notna(counter_defense_pct) and isna(counter_defense_rating):
            self.add_error(
                f"In {match_key}, {team_number} MISSING COUNTER DEFENSE RATING",
                error_type=ErrorType.MISSING_DATA,
            )

        # Inconsistent defense + counter defense pct.
        if (
            notna(defense_pct)
            and notna(counter_defense_pct)
            and (defense_pct + counter_defense_pct) > 1
        ):
            self.add_error(
                f"In {match_key}, {team_number} DEFENSE AND COUNTER DEFENSE PCT TOO HIGH",
                error_type=ErrorType.INCORRECT_DATA,
            )
