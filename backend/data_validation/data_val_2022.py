import collections
import json
from operator import itemgetter

from base_data_val import BaseDataValidation
from utils import *


class DataValidation2022(BaseDataValidation):
    def __init__(self, path_to_config: str = "config.yaml"):
        super().__init__(path_to_config)

        self.shooting_difference_auto = self.config.get("auto_shooting_difference", 5)
        self.shooting_difference_teleop = self.config.get(
            "teleop_shooting_difference", 10
        )

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

        if self._run_tba_checks:
            self.check_shooting_total_with_tba(scouting_data)

        self.output_errors()

    def validate_submission(self, submission: dict) -> None:
        """
        Runs all checks validating a single submission from 2022's game (Rapid React).

        :param submission: Dictionary containing data scouted.
        :return:
        """
        # Validates match schedule
        self.check_submission_with_match_schedule(submission)

        # Data-specific checks
        self.check_for_higher_than_six_ball_auto(submission)
        self.check_for_auto_shots_but_no_taxi(submission)
        self.check_for_missing_shooting_zones(submission)
        self.check_for_invalid_climb_data(submission)
        self.check_for_invalid_defense_data(
            match_key=submission["match_key"],
            team_number=submission["team_number"],
            defense_pct=submission["defense_pct"],
            counter_defense_pct=submission["counter_defense_pct"],
            defense_rating=submission["defense_rating"],
            counter_defense_rating=submission["counter_defense_rating"],
        )

        # TBA-related checks
        if self._run_tba_checks:
            self.check_submission_with_tba(submission)

    def check_for_higher_than_six_ball_auto(self, submission: dict) -> None:
        """
        Checks if a robot shot more than six balls during autonomous.

        :param submission: A dictionary containing scouted data for a robot.
        :return:
        """
        balls_shot_in_auto = (
            submission["auto_lower_hub"]
            + submission["auto_upper_hub"]
            + submission["auto_misses"]
        )

        if balls_shot_in_auto > 6:
            self.add_error(
                f"In {submission['match_key']}, {submission['team_number']} "
                f"shot {int(balls_shot_in_auto)} balls in Autonomous.",
                ErrorType.WARNING,
            )

    def check_for_auto_shots_but_no_taxi(self, submission: dict) -> None:
        """
        Checks if robot shot at least 2 balls in auto but didn't taxi.

        :param submission: Dictionary containing data scouted.
        :return:
        """
        balls_shot_in_auto = (
            submission["auto_lower_hub"]
            + submission["auto_upper_hub"]
            + submission["auto_misses"]
        )
        taxied = submission["taxied"]

        if balls_shot_in_auto >= 2 and not taxied:
            self.add_error(
                f"In {submission['match_key']}, {submission['team_number']} shot"
                f" {int(balls_shot_in_auto)} balls in Autonomous but DIDN'T TAXI.",
                ErrorType.WARNING,
            )

    def check_for_missing_shooting_zones(self, submission: dict) -> None:
        """
        Checks if robot shot balls in autonomous or teleoperated periods but scouter didn't select any shooting zones.

        :param submission: Dictionary containing data scouted.
        :return:
        """
        # Checks auto shooting zones
        balls_shot_in_auto = (
            submission["auto_lower_hub"]
            + submission["auto_upper_hub"]
            + submission["auto_misses"]
        )
        if balls_shot_in_auto and not submission["auto_shooting_zones"]:
            self.add_error(
                f"In {submission['match_key']}, {submission['team_number']} MISSING AUTO SHOOTING ZONES"
            )

        # Checks teleop shooting zones
        balls_shot_in_teleop = (
            submission["teleop_lower_hub"]
            + submission["teleop_upper_hub"]
            + submission["teleop_misses"]
        )
        if balls_shot_in_teleop and not submission["teleop_shooting_zones"]:
            self.add_error(
                f"In {submission['match_key']}, {submission['team_number']} MISSING TELEOP SHOOTING ZONES"
            )

    def check_for_invalid_climb_data(self, submission: dict) -> None:
        """
        Checks if the final and attempted climb are inconsistent, i.e. final climb traversal but robot didn't attempt traversal.
        Checks if robot climbed but no climb time was given.

        :param submission: Dictionary containing data scouted.
        :return:
        """  # noqa
        final_climb_type = submission["final_climb_type"]

        if not final_climb_type:
            final_climb_type = "No Climb"
        if final_climb_type != "No Climb":
            # Check if attempted climb for corresponding final climb type is false
            attempted_climb = submission[f"attempted_{final_climb_type.lower()}"]

            if not attempted_climb:
                self.add_error(
                    f"In {submission['match_key']}, {submission['team_number']}"
                    f" MISSING ATTEMPTED {final_climb_type.upper()}"
                )

            # Check if climb time is missing
            climb_time = submission["climb_time"]
            if not climb_time:
                self.add_error(
                    f"In {submission['match_key']}, {submission['team_number']} MISSING CLIMB TIME"
                )

    def check_submission_with_tba(self, submission: dict) -> None:
        """
        Validates taxi state and final climb with TBA data.
        :param submission: Dictionary containing data scouted.
        :return:
        """

        submission_key = submission["match_key"].strip().lower()
        full_match_key = f"{self._event_key}_{submission_key}"

        score_info = self.tba_match_data[full_match_key].score_breakdown

        if score_info:
            alliance = submission["alliance"].lower()
            driver_station = submission["driver_station"]

            tba_taxi = score_info[alliance][f"taxiRobot{driver_station}"]
            tba_climb = score_info[alliance][f"endgameRobot{driver_station}"]

            submission_taxi = submission["taxied"]
            submission_climb = submission["final_climb_type"]
            if submission_climb == "No Climb":
                submission_climb = "None"

            # Check for inconsistent taxi
            if (tba_taxi == "No" and submission_taxi) or (
                tba_taxi == "Yes" and not submission_taxi
            ):
                self.add_error(
                    f"In {submission['match_key']}, {submission['team_number']} INCORRECT TAXI according to TBA"
                )

            # Check for inconsistent climb type
            if tba_climb != submission_climb:
                self.add_error(
                    f"In {submission['match_key']}, {submission['team_number']} "
                    f"INCORRECT ClIMB TYPE according to TBA, should be {tba_climb}"
                )

    def check_shooting_total_with_tba(self, scouting_data: list) -> None:
        """
        Compares shooting total with TBA data with total from scouted data by match.
        :param scouting_data: List containing submissions, each submission being a dictionary containing scouted data.
        :return:
        """

        data_by_match = collections.defaultdict(lambda: collections.defaultdict(list))

        for data in scouting_data:
            data_by_match[data["match_key"]][data["alliance"].lower()].append(data)

        for match_key, alliance_data in data_by_match.items():
            full_match_key = f"{self._event_key}_{match_key}"

            if full_match_key in self.tba_match_data.keys():
                for alliance, submissions in alliance_data.items():
                    score_info = self.tba_match_data[full_match_key]["score_breakdown"][
                        alliance
                    ]

                    # Check total auto lower hub
                    auto_lower_scouting_total = sum(
                        map(itemgetter("auto_lower_hub"), submissions)
                    )
                    auto_lower_tba_total = (
                        score_info["autoCargoLowerNear"]
                        + score_info["autoCargoLowerFar"]
                        + score_info["autoCargoLowerRed"]
                        + score_info["autoCargoLowerBlue"]
                    )
                    auto_lower_difference = abs(
                        auto_lower_tba_total - auto_lower_scouting_total
                    )

                    if auto_lower_difference >= self.shooting_difference_auto:
                        self.add_error(
                            f"In {match_key}, {alliance} alliance, INCORRECT AUTO LOWER TOTAL according to TBA, "
                            f"Scouts: {auto_lower_scouting_total}, TBA: {auto_lower_tba_total}"
                        )

                    # Check total auto upper hub
                    auto_upper_scouting_total = sum(
                        map(itemgetter("auto_upper_hub"), submissions)
                    )
                    auto_upper_tba_total = (
                        score_info["autoCargoUpperNear"]
                        + score_info["autoCargoUpperFar"]
                        + score_info["autoCargoUpperRed"]
                        + score_info["autoCargoUpperBlue"]
                    )
                    auto_upper_difference = abs(
                        auto_upper_tba_total - auto_upper_scouting_total
                    )

                    if auto_upper_difference >= self.shooting_difference_auto:
                        self.add_error(
                            f"In {match_key}, {alliance} alliance, INCORRECT AUTO UPPER TOTAL according to TBA, "
                            f"Scouts: {auto_upper_scouting_total}, TBA: {auto_upper_tba_total}"
                        )

                    # Check total teleop lower hub
                    teleop_lower_scouting_total = sum(
                        map(itemgetter("teleop_lower_hub"), submissions)
                    )
                    teleop_lower_tba_total = (
                        score_info["teleopCargoLowerNear"]
                        + score_info["teleopCargoLowerFar"]
                        + score_info["teleopCargoLowerRed"]
                        + score_info["teleopCargoLowerBlue"]
                    )
                    teleop_lower_difference = abs(
                        teleop_lower_tba_total - teleop_lower_scouting_total
                    )

                    if teleop_lower_difference >= self.shooting_difference_teleop:
                        self.add_error(
                            f"In {match_key}, {alliance} alliance, INCORRECT TELEOP LOWER TOTAL according to TBA, "
                            f"Scouts: {teleop_lower_scouting_total}, TBA: {teleop_lower_tba_total}"
                        )

                    # Check total teleop upper hub
                    teleop_upper_scouting_total = sum(
                        map(itemgetter("teleop_upper_hub"), submissions)
                    )
                    teleop_upper_tba_total = (
                        score_info["teleopCargoUpperNear"]
                        + score_info["teleopCargoUpperFar"]
                        + score_info["teleopCargoUpperRed"]
                        + score_info["teleopCargoUpperBlue"]
                    )
                    teleop_upper_difference = abs(
                        teleop_upper_tba_total - teleop_upper_scouting_total
                    )

                    if teleop_upper_difference >= self.shooting_difference_teleop:
                        self.add_error(
                            f"In {match_key}, {alliance} alliance, INCORRECT TELEOP UPPER TOTAL according to TBA, "
                            f"Scouts: {teleop_upper_scouting_total}, TBA: {teleop_upper_tba_total}"
                        )
