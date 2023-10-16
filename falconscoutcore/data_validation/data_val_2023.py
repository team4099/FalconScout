import json
from itertools import chain

from data_validation.base_data_val import BaseDataValidation
from data_validation.config.constants import ChargedUp
from data_validation.config.utils import (ErrorType,
                                          get_intersection_of_n_series)
from numpy import logical_or
from pandas import DataFrame, Series, concat, isna, notna


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

        # Write averaged out data back to file
        with open(self.path_to_data_file, "w") as file:
            json.dump(scouting_data.to_dict("records"), file, indent=2)

        self.check_team_numbers_for_each_match(scouting_data)

        if not scouting_data.empty:
            self.auto_charge_station_checks(scouting_data)

            # Validates individual submissions
            for _, submission in scouting_data.iterrows():
                if not submission[self.config["team_number"]]:
                    self.add_error(
                        f"NO TEAM NUMBER for match {submission[self.config['match_key']]}",
                        ErrorType.CRITICAL,
                        submission[self.config["match_key"]],
                    )
                    continue

                self.validate_submission(submission)

            if self._run_with_tba:
                self.tba_validate_auto_game_pieces_scored(scouting_data)
                self.tba_validate_teleop_game_pieces_scored(scouting_data)

            self.output_errors()

    def validate_submission(self, submission: Series) -> None:
        """
        Runs all checks validating a single submission from 2022's game (Rapid React).

        :param submission: Series object containing a single submission of scouting data.
        :return:
        """
        auto_pieces = (
            submission[self.config["auto_high"]]
            + submission[self.config["auto_mid"]]
            + submission[self.config["auto_low"]]
        )

        if self.match_schedule:
            self.check_team_info_with_match_schedule(
                match_key=submission[self.config["match_key"]],
                team_number=submission[self.config["team_number"]],
                alliance=submission[self.config["alliance"]],
                driver_station=submission[self.config["driver_station"]],
            )

        self.validate_auto_attempted_game_pieces(
            match_key=submission[self.config["match_key"]],
            team_number=submission[self.config["team_number"]],
            auto_pieces=auto_pieces
        )

        # self.check_for_invalid_defense_data(
        #     match_key=submission[self.config["match_key"]],
        #     team_number=submission[self.config["team_number"]],
        #     defense_pct=submission[self.config["defense_pct"]],
        #     counter_defense_pct=submission[self.config["counter_defense_pct"]],
        #     defense_rating=submission[self.config["defense_rating"]],
        #     counter_defense_rating=submission[self.config["counter_defense_rating"]],
        # )

        self.validate_attempted_game_pieces(
            match_key=submission[self.config["match_key"]],
            team_number=submission[self.config["team_number"]],
            auto_pieces=auto_pieces,
            teleop_cones=submission[self.config["teleop_cones"]],
            teleop_cubes=submission[self.config["teleop_cubes"]],
        )

        if self._run_with_tba:
            self.tba_validate_auto_charge_station_state(
                match_key=submission[self.config["match_key"]],
                team_number=submission[self.config["team_number"]],
                alliance=submission[self.config["alliance"]],
                driver_station=submission[self.config["driver_station"]],
                auto_charging_state=submission[self.config["auto_charging_state"]],
            )
            self.tba_validate_endgame_charge_station_state(
                match_key=submission[self.config["match_key"]],
                team_number=submission[self.config["team_number"]],
                alliance=submission[self.config["alliance"]],
                driver_station=submission[self.config["driver_station"]],
                endgame_charging_state=submission[
                    self.config["endgame_charging_state"]
                ],
            )

    # TBA checks
    def tba_validate_auto_charge_station_state(
        self,
        match_key: str,
        team_number: int,
        alliance: str,
        driver_station: int,
        auto_charging_state: str,
    ) -> None:
        """
        Validates the state of any robots during autonomous if they were said to have docked/engaged with TBA data.

        :param match_key: Key of match that was scouted.
        :param team_number: Number of team that was scouted (eg 4099).
        :param alliance: The name of the alliance the team scouted was on.
        :param driver_station: The corresponding driver station of the team scouted (eg 1 for Red 1).
        :param auto_charging_state: The state the robot is in at the end of Autonomous in regards to the Charge Station.
        :return:
        """
        try:
            score_breakdown = self.match_data[
                f"{self._event_key}_{match_key}"
            ].score_breakdown[alliance.lower()]
        except KeyError as e:
            raise KeyError(
                "No matches to retrieve data from OR invalid match key, check scouting data."
            ) from e

        on_charge_station = (
            score_breakdown[f"autoChargeStationRobot{driver_station or 1}"] == "Docked"
        )
        is_level = score_breakdown["autoBridgeState"] == "Level"

        docked_state = on_charge_station and not is_level
        engaged_state = on_charge_station and is_level

        # Using XOR (^) here because we want to check for only when the two states are differing.
        if (auto_charging_state == "Dock") ^ docked_state and not engaged_state:
            self.add_error(
                f"In {match_key}, {team_number} has an incorrect DOCKED state during AUTO based on TBA data.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )
        if (auto_charging_state == "Engage") ^ engaged_state and not docked_state:
            self.add_error(
                f"In {match_key}, {team_number} has an incorrect ENGAGED state during AUTO based on TBA data.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

    # TODO: Won't work with the current implementation so fix if needed, but doesn't matter
    def tba_validate_auto_game_pieces_scored(
        self,
        scouting_data: DataFrame,
    ) -> None:
        """
        Validates if the amount of game pieces that were said to have been scored during autonomous are correct w/ TBA.

        :param scouting_data: A Pandas dataframe containing all the submissions 2023new_qr_codes wise.
        :return:
        """
        for (match_key, alliance), submissions_by_alliance in scouting_data.groupby(
            [self.config["match_key"], self.config["alliance"]]
        ):
            try:
                score_breakdown = self.match_data[
                    f"{self._event_key}_{match_key}"
                ].score_breakdown[alliance.lower()]
            except KeyError as e:
                raise KeyError(
                    "No matches to retrieve data from OR invalid match key, check scouting data."
                ) from e

            actual_auto_cones = sum(
                [
                    nodes.count("Cone")
                    for nodes in score_breakdown["autoCommunity"].values()
                ]
            )
            scouted_auto_cones = len(
                sum(submissions_by_alliance[self.config["auto_cones"]], start=[])
            )

            actual_auto_cubes = sum(
                [
                    nodes.count("Cube")
                    for nodes in score_breakdown["autoCommunity"].values()
                ]
            )
            scouted_auto_cubes = len(
                sum(submissions_by_alliance[self.config["auto_cubes"]], start=[])
            )

            scouted_auto_pieces = scouted_auto_cones + scouted_auto_cubes
            actual_auto_pieces = actual_auto_cones + actual_auto_cubes

            if (
                scouted_auto_pieces != actual_auto_pieces
                and abs(scouted_auto_pieces - actual_auto_pieces)
                >= self.TBA_GRID_AUTO_ERROR_THRESHOLD
            ):
                self.add_error(
                    f"In {match_key}, the {alliance.upper()} alliance was said to have scored"
                    f" {scouted_auto_cones} CONES and {scouted_auto_cubes} CUBES during AUTO "
                    f"but actually scored {actual_auto_cones} CONES and {actual_auto_cubes} CUBES.",
                    ErrorType.INCORRECT_DATA,
                    match_key,
                    alliance=alliance,
                )

    def tba_validate_teleop_game_pieces_scored(
        self,
        scouting_data: DataFrame,
    ) -> None:
        """
        Validates if the amount of game pieces that were said to have been scored during teleop are correct w/ TBA.

        :param scouting_data: A Pandas dataframe containing all the submissions 2023new_qr_codes wise.
        :return:
        """
        for (match_key, alliance), submissions_by_alliance in scouting_data.groupby(
            [self.config["match_key"], self.config["alliance"]]
        ):
            try:
                score_breakdown = self.match_data[
                    f"{self._event_key}_{match_key}"
                ].score_breakdown[alliance.lower()]
            except KeyError as e:
                raise KeyError(
                    "No matches to retrieve data from OR invalid match key, check scouting data."
                ) from e

            actual_teleop_cones = sum(
                [
                    nodes.count("Cone")
                    for nodes in score_breakdown["teleopCommunity"].values()
                ]
            )
            scouted_teleop_cones = len(
                sum(submissions_by_alliance[self.config["teleop_cones"]], start=[])
            )

            actual_teleop_cubes = sum(
                [
                    nodes.count("Cube")
                    for nodes in score_breakdown["teleopCommunity"].values()
                ]
            )
            scouted_teleop_cubes = len(
                sum(submissions_by_alliance[self.config["teleop_cubes"]], start=[])
            )

            scouted_teleop_pieces = scouted_teleop_cones + scouted_teleop_cubes
            actual_teleop_pieces = actual_teleop_cones + actual_teleop_cubes

            if (
                scouted_teleop_pieces != actual_teleop_pieces
                and abs(scouted_teleop_pieces - actual_teleop_pieces)
                >= self.TBA_GRID_TELEOP_ERROR_THRESHOLD
            ):
                self.add_error(
                    f"In {match_key}, the {alliance.upper()} alliance was said to have scored"
                    f" {scouted_teleop_cones} CONES and {scouted_teleop_cubes} CUBES during TELEOP "
                    f"but actually scored {actual_teleop_cones} CONES and {actual_teleop_cubes} CUBES.",
                    ErrorType.INCORRECT_DATA,
                    match_key,
                    alliance=alliance,
                )

    # Non-TBA checks
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
            float(defense_rating) and not float(defense_pct)
        ):
            self.add_error(
                f"In {match_key}, {team_number} rated for defense but NO DEFENSE PCT",
                ErrorType.MISSING_DATA,
                match_key,
                team_number,
            )

        # Check for missing defense rating.
        if (isna(defense_rating) and notna(defense_pct)) or (
            float(defense_pct) and not float(defense_rating)
        ):
            self.add_error(
                f"In {match_key}, {team_number} MISSING DEFENSE RATING",
                ErrorType.MISSING_DATA,
                match_key,
                team_number,
            )

        # Check for 0% counter defense pct but given rating.
        if (notna(counter_defense_rating) and isna(counter_defense_pct)) or (
            float(counter_defense_rating) and not float(counter_defense_pct)
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
            float(counter_defense_pct) and not float(counter_defense_rating)
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
            and (float(defense_pct) + float(counter_defense_pct)) > 100
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
        auto_pieces: int
    ) -> None:
        """
        Checks if the amount of game pieces the robot attempted to score in auto is "reasonable".

        :param match_key: Key of match that was scouted.
        :param team_number: Number of team that was scouted (eg 4099).
        :param auto_pieces: Number of pieces scored during autonomous
        :return:
        """
        if auto_pieces > 3:
            self.add_error(
                (
                    f"In {match_key}, {team_number} SCORING {auto_pieces} CONES AND CUBES"
                    f" IN AUTO IS IMPOSSIBLE"
                ),
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

    def validate_attempted_game_pieces(
        self,
        match_key: str,
        team_number: int,
        auto_pieces: int,
        teleop_cones: list,
        teleop_cubes: list,
    ) -> None:
        """
        Checks if the amount of cones scored in auto + teleop < 21 (12 cone nodes + 9 hybrid nodes).
        Checks if the amount of cubes scored in auto + teleop < 15 (6 cube nodes + 9 hybrid nodes).
        Checks if the amount of cones + cubes scored thru the game < 27 (12 cone nodes + 6 cube nodes + 9 hybrid nodes).

        :param match_key: Key of match that was scouted.
        :param team_number: Number of team that was scouted (eg 4099).
        :param auto_pieces: Number of pieces scored during autonomous.
        :param teleop_cones: List containing the type of node where the cone was placed onto in teleop.
        :param teleop_cubes: List containing the type of node where the cube was placed onto in teleop.
        :return:
        """
        # Makes sure that the # of cubes and cones scored is <= 27
        if (total_scored := auto_pieces + len(teleop_cones) + len(teleop_cubes)) > 27:
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
            [self.config["match_key"], self.config["alliance"]]
        ):
            # Ensure that only one robot was marked off as docked/engaged
            if (
                len(
                    submissions_by_alliance[
                        submissions_by_alliance[self.config["auto_charging_state"]]
                        == "true"
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
