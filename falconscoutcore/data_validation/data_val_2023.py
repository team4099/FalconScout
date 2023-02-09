import json

from data_validation.base_data_val import BaseDataValidation
from data_validation.config.constants import ChargedUp
from data_validation.config.utils import ErrorType
from pandas import DataFrame, Series, isna, notna


class DataValidation2023(BaseDataValidation):
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

        self.auto_charge_station_checks(scouting_data)
        self.check_if_engaged_but_not_docked(scouting_data)
        self.check_for_inconsistent_engaged(scouting_data)
        self.check_if_engaged_for_only_one_robot(scouting_data)

        # Validates individual submissions
        for _, submission in scouting_data.iterrows():
            if not submission[self.config["team_number"]]:
                self.add_error(
                    f"NO TEAM NUMBER for match {submission[self.config['match_key']]}",
                    error_type=ErrorType.CRITICAL,
                )
                continue

            self.validate_submission(submission)

        self.output_errors()

    def validate_submission(self, submission: Series) -> None:
        """
        Runs all checks validating a single submission from 2022's game (Rapid React).

        :param submission: Series object containing a single submission of scouting data.
        :return:
        """
        self.validate_auto_attempted_game_pieces(
            match_key=submission[self.config["match_key"]],
            team_number=submission[self.config["team_number"]],
            preloaded=submission[self.config["preloaded"]],
            auto_cones=submission[self.config["auto_cones"]],
            auto_cubes=submission[self.config["auto_cubes"]],
            auto_misses=submission[self.config["auto_misses"]],
        )

        self.check_for_invalid_defense_data(
            match_key=submission[self.config["match_key"]],
            team_number=submission[self.config["team_number"]],
            defense_pct=submission[self.config["defense_pct"]],
            counter_defense_pct=submission[self.config["counter_defense_pct"]],
            defense_rating=submission[self.config["defense_rating"]],
            counter_defense_rating=submission[self.config["counter_defense_rating"]],
        )

        self.validate_attempted_game_pieces(
            match_key=submission[self.config["match_key"]],
            team_number=submission[self.config["team_number"]],
            auto_cones=submission[self.config["auto_cones"]],
            teleop_cones=submission[self.config["teleop_cones"]],
            auto_cubes=submission[self.config["auto_cubes"]],
            teleop_cubes=submission[self.config["teleop_cubes"]],
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

    def validate_auto_attempted_game_pieces(
        self,
        match_key: str,
        team_number: int,
        preloaded: bool,
        auto_cones: list,
        auto_cubes: list,
        auto_misses: list,
    ) -> None:
        """
        Checks if the amount of game pieces the robot attempted to score in auto is "reasonable".

        :param match_key: Key of match that was scouted.
        :param team_number: Number of team that was scouted (eg 4099).
        :param preloaded: Whether or not the robot was preloaded with a game piece.
        :param auto_cones: List containing the type of node where the cone was placed onto in auto.
        :param auto_cubes: List containing the type of node where the cube was placed onto in auto.
        :param auto_misses: List containing the type of node and the type of game piece that the robot missed in auto.
        :return:
        """
        # Checks the # of attempted cones + cubes placed in auto
        pieces_attempted_in_auto = len(auto_cones) + len(auto_cubes) + len(auto_misses)

        # Checks if either the number of pieces attempted > 4 despite no preloaded or if it's > 5
        if (
            not preloaded and pieces_attempted_in_auto > 4
        ) or pieces_attempted_in_auto > 5:
            self.add_error(
                (
                    f"In {match_key}, {team_number} {pieces_attempted_in_auto} CONES AND CUBES BEING"
                    f" ATTEMPTED IN AUTO IS IMPOSSIBLE"
                ),
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

    def validate_attempted_game_pieces(
        self,
        match_key: str,
        team_number: int,
        auto_cones: list,
        teleop_cones: list,
        auto_cubes: list,
        teleop_cubes: list,
    ) -> None:
        """
        Checks if the amount of cones scored in auto + teleop < 21 (12 cone nodes + 9 hybrid nodes).
        Checks if the amount of cubes scored in auto + teleop < 15 (6 cube nodes + 9 hybrid nodes).
        Checks if the amount of cones + cubes scored thru the game < 27 (12 cone nodes + 6 cube nodes + 9 hybrid nodes).

        :param match_key: Key of match that was scouted.
        :param team_number: Number of team that was scouted (eg 4099).
        :param auto_cones: List containing the type of node where the cone was placed onto in auto.
        :param teleop_cones: List containing the type of node where the cone was placed onto in teleop.
        :param auto_cubes: List containing the type of node where the cube was placed onto in auto.
        :param teleop_cubes: List containing the type of node where the cube was placed onto in teleop.
        :return:
        """
        # Makes sure that the # of cones scored is <= 21
        if (cones_scored := len(auto_cones) + len(teleop_cones)) > 21:
            self.add_error(
                f"In {match_key}, {team_number} SCORING {cones_scored} CONES IS IMPOSSIBLE",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

        # Makes sure that the # of cubes scored is <= 15
        if (cubes_scored := len(auto_cubes) + len(teleop_cubes)) > 15:
            self.add_error(
                f"In {match_key}, {team_number} SCORING {cubes_scored} CUBES IS IMPOSSIBLE",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

        # Makes sure that the # of cubes and cones scored is <= 27
        if (total_scored := cones_scored + cubes_scored) > 27:
            self.add_error(
                f"In {match_key}, {team_number} SCORING {total_scored} CUBES AND CONES IS IMPOSSIBLE",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

    def auto_charge_station_checks(self, scouting_data: DataFrame) -> None:
        """
        Checks if either more than one robot is ticked off as docked/engaged
        or if a robot was marked as engaged but not docked.

        :param scouting_data: A Pandas dataframe containing the scouting submissions.
        :return:
        """
        for (match_key, alliance), submissions_by_alliance in scouting_data.groupby(
            ["match_key", "alliance"]
        ):
            # Ensure that only one robot was marked off as docked/engaged
            if (
                len(
                    submissions_by_alliance[
                        submissions_by_alliance[self.config["auto_docked"]] == True
                    ]
                )
                > 1
                or len(
                    submissions_by_alliance[
                        submissions_by_alliance[self.config["auto_engaged"]] == True
                    ]
                )
                > 1
            ):
                self.add_error(
                    (
                        f"In {match_key}, THE {alliance.upper()} ALLIANCE MARKED MORE THAN "
                        f"ONE ROBOT AS DOCKED/ENGAGED IN AUTO"
                    ),
                    ErrorType.INCORRECT_DATA,
                    match_key,
                )

            # Check for any robots marked as engaged but not docked
            for _, submission in submissions_by_alliance.iterrows():
                if (
                    submission[self.config["auto_docked"]] == False
                    and submission[self.config["auto_engaged"]] == True
                ):
                    self.add_error(
                        (
                            f"In {match_key}, {submission[self.config['team_number']]} WAS MARKED"
                            f" AS ENGAGED DESPITE NOT DOCKING IN AUTO"
                        ),
                        ErrorType.INCORRECT_DATA,
                        match_key,
                        submission[self.config["team_number"]],
                    )

    def check_if_engaged_but_not_docked(self, scouting_data: DataFrame) -> None:
        """
        Checks if a robot was marked as engaged but not docked in the endgame.

        :param scouting_data: A Pandas dataframe containing the scouting submissions.
        :return:
        """
        for (match_key, alliance), submissions_by_alliance in scouting_data.groupby(
            ["match_key", "alliance"]
        ):
            for _, submission in submissions_by_alliance.iterrows():
                if (
                    submission[self.config["docked"]] == False
                    and submission[self.config["engaged"]] == True
                ):
                    self.add_error(
                        f"In {match_key}, {submission['team_number']} WAS MARKED AS ENGAGED DESPITE NOT DOCKING",
                        ErrorType.INCORRECT_DATA,
                        match_key,
                        submission[self.config["team_number"]],
                    )

    def check_if_engaged_for_only_one_robot(self, scouting_data: DataFrame) -> None:
        """
        Checks if a robot was marked as engaged in Endgame even though only one robot was marked as docked (impossible).

        :param scouting_data: A Pandas dataframe containing the scouting submissions.
        :return:
        """
        for (match_key, alliance), submissions_by_alliance in scouting_data.groupby(
            ["match_key", "alliance"]
        ):
            robots_docked = len(
                submissions_by_alliance[
                    submissions_by_alliance[self.config["docked"]] == True
                ]
            )
            robots_engaged = len(
                submissions_by_alliance[
                    submissions_by_alliance[self.config["engaged"]] == True
                ]
            )
            if robots_engaged == 1 and robots_docked == 1:
                self.add_error(
                    (
                        f"In {match_key}, THE {alliance.upper()} ALLIANCE HAS ONLY ONE ROBOT MARKED AS DOCKED/ENGAGED"
                        " WHICH IS IMPOSSIBLE IN ENDGAME"
                    ),
                    ErrorType.INCORRECT_DATA,
                    match_key,
                )

    def check_for_inconsistent_engaged(self, scouting_data: DataFrame) -> None:
        """
        Checks if two or more robots were marked as docked but one was marked as engaged whilst the other wasn't.

        :param scouting_data: A Pandas dataframe containing the scouting submissions.
        :return:
        """
        for (match_key, alliance), submissions_by_alliance in scouting_data.groupby(
            ["match_key", "alliance"]
        ):
            robots_docked = len(
                submissions_by_alliance[
                    submissions_by_alliance[self.config["docked"]] == True
                ]
            )
            robots_engaged = len(
                submissions_by_alliance[
                    submissions_by_alliance[self.config["engaged"]] == True
                ]
            )

            if (
                robots_docked > 0
                and robots_engaged > 0
                and robots_docked != robots_engaged
            ):
                self.add_error(
                    f"In {match_key}, THE {alliance.upper()} ALLIANCE HAS SOME ROBOTS MARKED AS ENGAGED AND OTHERS NOT",
                    ErrorType.INCORRECT_DATA,
                    match_key,
                )

    # TODO: Implement the statistical outliers check.
    def check_for_statistical_outliers(self) -> None:
        """Needs to be implemented later."""
        pass
