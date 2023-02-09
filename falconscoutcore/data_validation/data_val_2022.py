import json

from data_validation.base_data_val import BaseDataValidation
from data_validation.config.constants import RapidReact
from data_validation.config.utils import ErrorType
from numpy import percentile
from pandas import DataFrame, Series, isna, notna


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
                    json.load(file), key=lambda data: data[self.config["match_key"]]
                )

        # Converts JSON to DataFrame
        scouting_data = DataFrame.from_dict(scouting_data)

        self.check_team_numbers_for_each_match(scouting_data)

        # Validates individual submissions
        for _, submission in scouting_data.iterrows():
            if not submission[self.config["team_number"]]:
                self.add_error(
                    f"NO TEAM NUMBER for match {submission[self.config['match_key']]}",
                    error_type=ErrorType.CRITICAL,
                )
                continue

            self.validate_submission(submission)

        # TODO: Add check relying on TBA to cross-check shooting totals with TBA's reported shooting totals.
        if self._run_with_tba:
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
        try:
            self.check_for_missing_shooting_zones(
                match_key=submission[self.config["match_key"]],
                team_number=submission[self.config["team_number"]],
                auto_lower_hub=submission[self.config["auto_lower_hub"]],
                auto_upper_hub=submission[self.config["auto_upper_hub"]],
                auto_misses=submission[self.config["auto_misses"]],
                auto_shooting_zones=submission[self.config["auto_shooting_zones"]],
                teleop_lower_hub=submission[self.config["teleop_lower_hub"]],
                teleop_upper_hub=submission[self.config["teleop_upper_hub"]],
                teleop_misses=submission[self.config["teleop_misses"]],
                teleop_shooting_zones=submission[self.config["teleop_shooting_zones"]],
            )
        except Exception as e:
            print(e)

        try:
            self.check_for_invalid_defense_data(
                match_key=submission[self.config["match_key"]],
                team_number=submission[self.config["team_number"]],
                defense_pct=submission[self.config["defense_pct"]],
                counter_defense_pct=submission[self.config["counter_defense_pct"]],
                defense_rating=submission[self.config["defense_rating"]],
                counter_defense_rating=submission[
                    self.config["counter_defense_rating"]
                ],
            )
        except Exception as e:
            print(e)

        try:
            self.check_team_info_with_match_schedule(
                match_key=submission[self.config["match_key"]],
                team_number=submission[self.config["team_number"]],
                alliance=submission[self.config["alliance"]],
                driver_station=submission[self.config["driver_station"]],
            )
        except Exception as e:
            print(e)

        try:
            self.check_for_auto_great_than_6(
                match_key=submission[self.config["match_key"]],
                team_number=submission[self.config["team_number"]],
                auto_lower_hub=submission[self.config["auto_lower_hub"]],
                auto_upper_hub=submission[self.config["auto_upper_hub"]],
                auto_misses=submission[self.config["auto_misses"]],
            )
        except Exception as e:
            print(e)

        try:
            self.check_for_auto_cargo_when_taxi(
                match_key=submission[self.config["match_key"]],
                team_number=submission[self.config["team_number"]],
                auto_lower_hub=submission[self.config["auto_lower_hub"]],
                auto_upper_hub=submission[self.config["auto_upper_hub"]],
                auto_misses=submission[self.config["auto_misses"]],
                taxi=submission[self.config["taxied"]],
            )
        except Exception as e:
            print(e)

        # TODO: Add TBA-related checks (see Notion docs for which checks to add.)
        if self._run_with_tba:
            try:
                self.check_submission_with_tba(
                    match_key=submission[self.config["match_key"]],
                    team_number=submission[self.config["team_number"]],
                    alliance=submission[self.config["alliance"]],
                    driver_station=submission[self.config["driver_station"]],
                    taxied=submission[self.config["taxied"]],
                    final_climb_type=submission[self.config["final_climb_type"]],
                )
            except Exception as e:
                print(e)

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
                ErrorType.MISSING_DATA,
                match_key,
                team_number,
            )

        # Checks teleop shooting zones
        balls_shot_in_teleop = teleop_lower_hub + teleop_upper_hub + teleop_misses
        if balls_shot_in_teleop and not teleop_shooting_zones:
            self.add_error(
                f"In {match_key}, {team_number} MISSING TELEOP SHOOTING ZONES",
                ErrorType.MISSING_DATA,
                match_key,
                team_number,
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
                    ErrorType.INCORRECT_DATA,
                    match_key,
                    team_number,
                )

            # check for inconsistent climb type
            if tba_climb != final_climb_type.replace("No Climb", "None"):
                self.add_error(
                    f"In {match_key}, {team_number} INCORRECT ClIMB TYPE according to TBA, should be {tba_climb}",
                    ErrorType.INCORRECT_DATA,
                    match_key,
                    team_number,
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
        if (notna(defense_rating) and isna(defense_pct)) or (
            defense_rating and not defense_pct
        ):
            self.add_error(
                f"In {match_key}, {team_number} rated for defense but NO DEFENSE PCT",
                ErrorType.MISSING_DATA,
                match_key,
                team_number,
            )

        # Check for missing defense rating.
        if (isna(defense_rating) and notna(defense_pct)) or (
            defense_pct and not defense_rating
        ):
            self.add_error(
                f"In {match_key}, {team_number} MISSING DEFENSE RATING",
                ErrorType.MISSING_DATA,
                match_key,
                team_number,
            )

        # Check for 0% counter defense pct but given rating.
        if (notna(counter_defense_rating) and isna(counter_defense_pct)) or (
            counter_defense_rating and not counter_defense_pct
        ):
            self.add_error(
                f"In {match_key}, {team_number} "
                f"rated for counter defense but NO COUNTER DEFENSE PCT",
                ErrorType.MISSING_DATA,
                match_key,
                team_number,
            )

        # Check for missing counter defense rating.
        if (notna(counter_defense_pct) and isna(counter_defense_rating)) or (
            counter_defense_pct and not counter_defense_rating
        ):
            self.add_error(
                f"In {match_key}, {team_number} MISSING COUNTER DEFENSE RATING",
                ErrorType.MISSING_DATA,
                match_key,
                team_number,
            )

        # Inconsistent defense + counter defense pct.
        if (
            notna(defense_pct)
            and notna(counter_defense_pct)
            and (defense_pct + counter_defense_pct) > 1
        ):
            self.add_error(
                f"In {match_key}, {team_number} DEFENSE AND COUNTER DEFENSE PCT TOO HIGH",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

    def check_for_auto_cargo_when_taxi(
        self,
        match_key: str,
        team_number: int,
        auto_upper_hub: int,
        auto_lower_hub: int,
        auto_misses: int,
        taxi: bool,
    ) -> None:
        """
        Checks if a team both taxied and shot more than 2 balls. This configuration is almost always impossible.

        :param match_key: Key of match that was scouted.
        :param team_number: Number of team that was scouted (eg 4099).
        :param auto_lower_hub: Number of balls shot into the lower hub during Autonomous.
        :param auto_upper_hub: Number of balls shot into the upper hub during Autonomous.
        :param auto_misses: Number of balls missed when shooting during Autonomous.
        :param taxi: Whether the team taxied.

        :return:
        """
        # Check if 2 or more balls were shot in auto and still taxied
        if (auto_upper_hub + auto_lower_hub + auto_misses) >= 2 and not (taxi):
            self.add_error(
                f"In {match_key}, frc{team_number} SHOT 2 OR MORE BALLS WITHOUT TAXING",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number
                # Marked as incorrect although it is technically possible.
                # Most times it will not be possible
            )

    def check_for_statistical_outliers(
        self,
        auto_check: bool = True,
        teleop_check: bool = True,
        endgame_check: bool = True,
    ) -> None:
        """
        Checking for statistical outliers in the 2022 Rapid React game.

        :param auto_check: Runs outlier checks specifically and strictly against the autonomous portion of the game.
        :param teleop_check: Runs outlier checks specifically and strictly against the teloperated portion of the game.
        :param endgame_check: Runs outlier checks specifically and strictly against the endgame portion of the game.

        :return:
        """
        self.check_for_auto_outliers()

    def check_for_auto_outliers(self) -> None:
        """
        Check and mark any statistical outliers across all teams' auto data.

        :return:
        """
        for team in self.teams:
            team_data_entries = self.df.loc[self.df["team_number"] == team]

            auto_cargo_match_team_data = list(
                zip(
                    team_data_entries["match_key"],
                    team_data_entries["auto_lower_hub"],
                    team_data_entries["auto_upper_hub"],
                    team_data_entries["taxied"],
                )
            )

            auto_points_match_team_data = list(
                map(
                    lambda team_datum: (
                        team_datum[0],
                        team_datum[1] * RapidReact.AUTO_LOWER_HUB_POINT_VALUE
                        + team_datum[2] * RapidReact.AUTO_UPPER_HUB_POINT_VALUE
                        + team_datum[3] * RapidReact.AUTO_TAXI_POINT_VALUE,
                    ),
                    auto_cargo_match_team_data,
                )
            )

            min_IQR_threshold = percentile(
                [datum[1] for datum in auto_points_match_team_data], 25
            )
            max_IQR_threshold = percentile(
                [datum[1] for datum in auto_points_match_team_data], 75
            )

            min_outliers = list(
                filter(
                    lambda match_data: match_data[1] < min_IQR_threshold,
                    auto_points_match_team_data,
                )
            )
            max_outliers = list(
                filter(
                    lambda match_data: match_data[1] > max_IQR_threshold,
                    auto_points_match_team_data,
                )
            )

            for outlier in min_outliers:
                # Logging all min outliers as info
                self.add_error(
                    f"In {outlier[0]}, frc{team} HAD AN AUTONOMOUS SCORE OUTLIER (<Q1) OF {outlier[1]} POINTS",
                    ErrorType.INFO,
                    outlier[0],
                    team,
                )

            for outlier in max_outliers:
                # Logging all max outliers as info
                self.add_error(
                    f"In {outlier[0]}, frc{team} HAD AN AUTONOMOUS SCORE OUTLIER (>Q3) {outlier[1]} POINTS",
                    ErrorType.INFO,
                    outlier[0],
                    team,
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
                f"In {match_key}, {team_number} UNLIKELY AUTO SHOT COUNT",
                ErrorType.WARNING,
                match_key,
                team_number,
            )
