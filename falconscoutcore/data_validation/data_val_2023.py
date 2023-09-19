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
        scouting_data = self.average_out_data(scouting_data)

        # Write averaged out data back to file
        with open(self.path_to_data_file, "w") as file:
            json.dump(scouting_data.to_dict("records"), file, indent=2)

        self.check_team_numbers_for_each_match(scouting_data)

        if not scouting_data.empty:
            self.auto_charge_station_checks(scouting_data)
            self.check_for_inconsistent_engaged(scouting_data)

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
        # self.check_team_info_with_match_schedule(
        #     match_key=submission[self.config["match_key"]],
        #     team_number=submission[self.config["team_number"]],
        #     alliance=submission[self.config["alliance"]],
        #     driver_station=submission[self.config["driver_station"]],
        # )

        self.check_team_info_with_match_schedule(
            match_key=submission[self.config["match_key"]],
            team_number=submission[self.config["team_number"]],
            alliance=submission[self.config["alliance"]],
            driver_station=submission[self.config["driver_station"]],
        )

        self.validate_auto_attempted_game_pieces(
            match_key=submission[self.config["match_key"]],
            team_number=submission[self.config["team_number"]],
            preloaded=submission[self.config["preloaded"]],
            auto_cones=submission[self.config["auto_cones"]],
            auto_cubes=submission[self.config["auto_cubes"]],
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
            auto_cones=submission[self.config["auto_cones"]],
            teleop_cones=submission[self.config["teleop_cones"]],
            auto_cubes=submission[self.config["auto_cubes"]],
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

    def average_out_data(self, scouting_data: DataFrame) -> DataFrame:
        """
        Averages out data if n-scouts scouted a single robot in order to get more accurate data.

        :return: A dataframe containing the averaged-out dataframe.
        """
        columns_to_use = [
            column for column in scouting_data.columns if column != "uuid"
        ]
        averaged_scouting_data = DataFrame(columns=columns_to_use)

        for (match_key, alliance), submissions_by_alliance in scouting_data.groupby(
            [self.config["match_key"], self.config["alliance"]]
        ):
            attempted_triple_balance = int(
                (submissions_by_alliance["EndgameAttemptedCharge"] == "Engage").sum()
                >= 3
            )
            successful_triple_balance = int(
                (submissions_by_alliance["EndgameFinalCharge"] == "Engage").sum() >= 3
            )

            for team_number, submissions_by_team in submissions_by_alliance.groupby(
                self.config["team_number"]
            ):
                # Map "Disabled", "Tippy" and "Mobile" from strings to booleans
                json_boolean_to_int = {
                    "true": 1,
                    "false": 0,
                    0: 0,
                    1: 1,
                    0.5: 0.5,
                }  # TODO: support dual scouting condensation after doing it once

                submissions_by_team[self.config["disabled"]] = submissions_by_team[
                    self.config["disabled"]
                ].map(json_boolean_to_int)
                submissions_by_team[self.config["tippy"]] = submissions_by_team[
                    self.config["tippy"]
                ].map(json_boolean_to_int)
                submissions_by_team[self.config["mobile"]] = submissions_by_team[
                    self.config["mobile"]
                ].map(json_boolean_to_int)

                if len(submissions_by_team) == 1:
                    submissions_by_team[self.config["attempted_triple_balance"]] = int(
                        attempted_triple_balance
                    )
                    submissions_by_team[self.config["successful_triple_balance"]] = int(
                        successful_triple_balance
                    )

                    averaged_scouting_data = concat(
                        [averaged_scouting_data, submissions_by_team]
                    )
                else:
                    n_scouts = len(submissions_by_team)

                    # Convert auto grid and teleop grids to a list
                    submissions_by_team[self.config["auto_grid"]] = [
                        grid_submission.split("|")
                        for grid_submission in submissions_by_team[
                            self.config["auto_grid"]
                        ]
                    ]
                    submissions_by_team[self.config["teleop_grid"]] = [
                        grid_submission.split("|")
                        for grid_submission in submissions_by_team[
                            self.config["teleop_grid"]
                        ]
                    ]

                    # Auto grid intersection
                    (
                        auto_grid_intersected,
                        auto_same_length,
                        auto_same_values,
                    ) = get_intersection_of_n_series(
                        submissions_by_team[self.config["auto_grid"]]
                    )
                    if auto_same_length and not auto_same_values:
                        auto_grid_intersected = submissions_by_team[
                            self.config["auto_grid"]
                        ].iloc[0]
                        # self.add_error(
                        #     f"In {match_key}, {n_scouts} SCOUTS scouting {team_number} have"
                        #     f" DIFFERENT positions for the GAME PIECES scored during AUTONOMOUS.",
                        #     ErrorType.INCORRECT_DATA,
                        #     match_key,
                        #     team_number,
                        # )
                    elif not (auto_same_length or auto_same_values):
                        auto_grid_intersected = submissions_by_team[
                            self.config["auto_grid"]
                        ].iloc[0]
                        total_differences = len(
                            {
                                *chain.from_iterable(
                                    [*submissions_by_team[self.config["auto_grid"]]]
                                )
                            }
                        ) - len(
                            min(submissions_by_team[self.config["auto_grid"]], key=len)
                        )

                        self.add_error(
                            f"In {match_key}, {n_scouts} SCOUTS scouting {team_number} have"
                            f"a DIFFERENCE of {total_differences} GAME PIECES scored during AUTONOMOUS.",
                            ErrorType.RESCOUT_MATCH
                            if total_differences >= 2
                            else ErrorType.INCORRECT_DATA,
                            match_key,
                            team_number,
                        )
                    else:
                        auto_grid_intersected = auto_grid_intersected[0]

                    # Teleop grid intersection
                    (
                        teleop_grid_intersected,
                        teleop_same_length,
                        teleop_same_values,
                    ) = get_intersection_of_n_series(
                        submissions_by_team[self.config["teleop_grid"]]
                    )

                    if teleop_same_length and not teleop_same_values:
                        teleop_grid_intersected = submissions_by_team[
                            self.config["teleop_grid"]
                        ].iloc[0]
                        # self.add_error(
                        #     f"In {match_key}, {n_scouts} SCOUTS scouting {team_number} have"
                        #     f" DIFFERENT positions for the GAME PIECES scored during TELEOP.",
                        #     ErrorType.INCORRECT_DATA,
                        #     match_key,
                        #     team_number,
                        # )
                    elif not (teleop_same_length or teleop_same_values):
                        teleop_grid_intersected = submissions_by_team[
                            self.config["teleop_grid"]
                        ].iloc[0]
                        total_differences = len(
                            {
                                *chain.from_iterable(
                                    [*submissions_by_team[self.config["teleop_grid"]]]
                                )
                            }
                        ) - len(
                            min(
                                submissions_by_team[self.config["teleop_grid"]], key=len
                            )
                        )

                        self.add_error(
                            f"In {match_key}, {n_scouts} SCOUTS scouting {team_number} have"
                            f"a DIFFERENCE of {total_differences} GAME PIECES scored during TELEOP.",
                            ErrorType.RESCOUT_MATCH
                            if total_differences >= 2
                            else ErrorType.INCORRECT_DATA,
                            match_key,
                            team_number,
                        )
                    else:
                        teleop_grid_intersected = teleop_grid_intersected[0]

                    # Auto attempted and actual charge station states
                    auto_attempted_charges = submissions_by_team[
                        self.config["auto_attempted_charge"]
                    ]
                    if auto_attempted_charges.nunique() == 1:
                        auto_attempted_charge = auto_attempted_charges.iloc[0]
                    else:
                        different_charges = set(auto_attempted_charges)
                        auto_attempted_charge = (
                            "Engage" if "Engage" in different_charges else "None"
                        )

                    auto_final_charges = submissions_by_team[
                        self.config["auto_charging_state"]
                    ]
                    if auto_final_charges.nunique() == 1:
                        auto_final_charge = auto_final_charges.iloc[0]
                    else:
                        different_charges = set(auto_final_charges)
                        if "Engage" in different_charges:
                            auto_final_charge = "Engage"
                        elif "Docked" in different_charges:
                            auto_final_charge = "Docked"
                        else:
                            auto_final_charge = "None"

                    # Endgame attempted and actual charge station states
                    endgame_attempted_charges = submissions_by_team[
                        self.config["endgame_attempted_charge"]
                    ]
                    if endgame_attempted_charges.nunique():
                        endgame_attempted_charge = endgame_attempted_charges.iloc[0]
                    else:
                        different_charges = set(endgame_attempted_charges)
                        endgame_attempted_charge = (
                            "Dock|Engage"
                            if "Dock|Engage" in different_charges
                            else "None"
                        )

                    endgame_final_charges = submissions_by_team[
                        self.config["endgame_charging_state"]
                    ]
                    if endgame_final_charges.nunique() == 1:
                        endgame_final_charge = endgame_final_charges.iloc[0]
                    else:
                        different_charges = set(endgame_final_charges)
                        if "Engage" in different_charges:
                            endgame_final_charge = "Engage"
                        elif "Docked" in different_charges:
                            endgame_final_charge = "Docked"
                        elif "Parked" in different_charges:
                            endgame_final_charge = "Parked"
                        else:
                            endgame_final_charge = "None"

                    # create lists for auto cones, auto cubes, teleop cones and teleop cubes
                    cone_positions = {1, 3, 4, 6, 7, 9}
                    positions_to_names = {"H": "High", "M": "Mid", "L": "Low"}

                    auto_cones = []
                    auto_cubes = []
                    teleop_cones = []
                    teleop_cubes = []

                    for game_piece in auto_grid_intersected:
                        if not game_piece:
                            continue

                        position, height = game_piece[:2]

                        if height == "L":
                            if "cone" in game_piece:
                                auto_cones.append("Low")
                            elif "cube" in game_piece:
                                auto_cubes.append("Low")
                            continue

                        if int(position) in cone_positions:
                            auto_cones.append(positions_to_names[height])
                        else:
                            auto_cubes.append(positions_to_names[height])

                    for game_piece in teleop_grid_intersected:
                        if not game_piece:
                            continue

                        position, height = game_piece[:2]

                        if height == "L":
                            if "cone" in game_piece:
                                teleop_cones.append("Low")
                            elif "cube" in game_piece:
                                teleop_cubes.append("Low")
                            continue

                        if int(position) in cone_positions:
                            teleop_cones.append(positions_to_names[height])
                        else:
                            teleop_cubes.append(positions_to_names[height])

                    averaged_scouting_data = concat(
                        [
                            averaged_scouting_data,
                            DataFrame.from_dict(
                                [
                                    {
                                        self.config["scout_id"]: " and ".join(
                                            submissions_by_team[self.config["scout_id"]]
                                        ).strip(),
                                        self.config["match_key"]: match_key,
                                        self.config["alliance"]: alliance,
                                        self.config[
                                            "driver_station"
                                        ]: submissions_by_team[
                                            self.config["driver_station"]
                                        ].iloc[
                                            0
                                        ],
                                        self.config["team_number"]: team_number,
                                        self.config["preloaded"]: submissions_by_team[
                                            self.config["preloaded"]
                                        ].iloc[0],
                                        self.config["auto_grid"]: "|".join(
                                            auto_grid_intersected
                                        ),
                                        self.config["auto_missed"]: submissions_by_team[
                                            self.config["auto_missed"]
                                        ].mean(),
                                        self.config["mobile"]: submissions_by_team[
                                            self.config["mobile"]
                                        ].iloc[0],
                                        self.config[
                                            "auto_attempted_charge"
                                        ]: auto_attempted_charge,
                                        self.config[
                                            "auto_charging_state"
                                        ]: auto_final_charge,
                                        self.config["auto_notes"]: " | ".join(
                                            submissions_by_team[
                                                self.config["auto_notes"]
                                            ]
                                        ),
                                        self.config["teleop_grid"]: "|".join(
                                            teleop_grid_intersected
                                        ),
                                        self.config[
                                            "teleop_missed"
                                        ]: submissions_by_team[
                                            self.config["teleop_missed"]
                                        ].mean(),
                                        self.config["teleop_notes"]: " | ".join(
                                            submissions_by_team[
                                                self.config["teleop_notes"]
                                            ]
                                        ),
                                        self.config[
                                            "endgame_attempted_charge"
                                        ]: endgame_attempted_charge,
                                        self.config[
                                            "endgame_charging_state"
                                        ]: endgame_final_charge,
                                        self.config["endgame_notes"]: " | ".join(
                                            submissions_by_team[
                                                self.config["endgame_notes"]
                                            ]
                                        ),
                                        self.config["disabled"]: (
                                            int(
                                                submissions_by_team[
                                                    self.config["disabled"]
                                                ].iloc[0]
                                            )
                                            if submissions_by_team[
                                                self.config["disabled"]
                                            ].nunique()
                                            == 1
                                            else 1
                                        ),
                                        self.config["tippy"]: submissions_by_team[
                                            self.config["tippy"]
                                        ]
                                        .astype(int)
                                        .mean(),
                                        self.config["defense_pct"]: submissions_by_team[
                                            self.config["defense_pct"]
                                        ].mean(),
                                        self.config[
                                            "defense_rating"
                                        ]: submissions_by_team[
                                            self.config["defense_rating"]
                                        ].mean(),
                                        self.config[
                                            "driver_rating"
                                        ]: submissions_by_team[
                                            self.config["driver_rating"]
                                        ].mean(),
                                        self.config["rating_notes"]: " | ".join(
                                            submissions_by_team[
                                                self.config["rating_notes"]
                                            ]
                                        ),
                                        self.config["auto_cones"]: auto_cones,
                                        self.config["auto_cubes"]: auto_cubes,
                                        self.config["teleop_cones"]: teleop_cones,
                                        self.config["teleop_cubes"]: teleop_cubes,
                                        "scanRaw": submissions_by_team["scanRaw"].iloc[
                                            0
                                        ],
                                        "uuid": submissions_by_team["uuid"].iloc[0],
                                        self.config["attempted_triple_balance"]: int(
                                            attempted_triple_balance
                                        ),
                                        self.config["successful_triple_balance"]: int(
                                            successful_triple_balance
                                        ),
                                    }
                                ]
                            ),
                        ]
                    )

        return averaged_scouting_data

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

    def tba_validate_endgame_charge_station_state(
        self,
        match_key: str,
        team_number: int,
        alliance: str,
        driver_station: int,
        endgame_charging_state: str,
    ) -> None:
        """
        Validates the state of any robots during endgame if they were said to have docked/engaged with TBA.

        :param match_key: Key of match that was scouted.
        :param team_number: Number of team that was scouted (eg 4099).
        :param alliance: The name of the alliance the team scouted was on.
        :param driver_station: The corresponding driver station of the team scouted (eg 1 for Red 1).
        :param endgame_charging_state: The state the robot is in at the end of Teleop in regards to the Charge Station.
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
            score_breakdown[f"endGameChargeStationRobot{driver_station or 1}"]
            == "Docked"
        )
        is_level = score_breakdown["endGameBridgeState"] == "Level"

        docked_state = on_charge_station and not is_level
        engaged_state = on_charge_station and is_level

        # Using XOR (^) here because we want to check for only when the two states are differing.
        if (endgame_charging_state == "Dock") ^ docked_state and not engaged_state:
            self.add_error(
                f"In {match_key}, {team_number} has an incorrect DOCKED state during ENDGAME based on TBA data.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )
        if (endgame_charging_state == "Engage") ^ engaged_state and not docked_state:
            self.add_error(
                f"In {match_key}, {team_number} has an incorrect ENGAGED state during ENDGAME based on TBA data.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

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
        preloaded: bool,
        auto_cones: list,
        auto_cubes: list,
    ) -> None:
        """
        Checks if the amount of game pieces the robot attempted to score in auto is "reasonable".

        :param match_key: Key of match that was scouted.
        :param team_number: Number of team that was scouted (eg 4099).
        :param preloaded: Whether or not the robot was preloaded with a game piece.
        :param auto_cones: List containing the type of node where the cone was placed onto in auto.
        :param auto_cubes: List containing the type of node where the cube was placed onto in auto.
        :return:
        """
        # Checks the # of attempted cones + cubes placed in auto
        pieces_attempted_in_auto = len(auto_cones) + len(auto_cubes)

        # Checks if either the number of pieces attempted > 4 despite no preloaded or if it's > 5
        if (
            not preloaded and pieces_attempted_in_auto > 2
        ) or pieces_attempted_in_auto > 3:
            self.add_error(
                (
                    f"In {match_key}, {team_number} SCORING {pieces_attempted_in_auto} CONES AND CUBES"
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
            [self.config["match_key"], self.config["alliance"]]
        ):
            # Ensure that only one robot was marked off as docked/engaged
            if (
                len(
                    submissions_by_alliance[
                        submissions_by_alliance[self.config["auto_charging_state"]]
                        == "Docked"
                    ]
                )
                > 1
                or len(
                    submissions_by_alliance[
                        submissions_by_alliance[self.config["auto_charging_state"]]
                        == "Engaged"
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

    def check_if_engaged_but_not_docked(self, scouting_data: DataFrame) -> None:
        """
        Checks if a robot was marked as engaged but not docked in the endgame.

        :param scouting_data: A Pandas dataframe containing the scouting submissions.
        :return:
        """
        for (match_key, alliance), submissions_by_alliance in scouting_data.groupby(
            [self.config["match_key"], self.config["alliance"]]
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

    def check_for_inconsistent_engaged(self, scouting_data: DataFrame) -> None:
        """
        Checks if two or more robots were marked as docked but one was marked as engaged whilst the other wasn't.

        :param scouting_data: A Pandas dataframe containing the scouting submissions.
        :return:
        """
        for (match_key, alliance), submissions_by_alliance in scouting_data.groupby(
            [self.config["match_key"], self.config["alliance"]]
        ):
            robots_docked = len(
                submissions_by_alliance[
                    submissions_by_alliance[self.config["endgame_charging_state"]]
                    == "Docked"
                ]
            )
            robots_engaged = len(
                submissions_by_alliance[
                    submissions_by_alliance[self.config["endgame_charging_state"]]
                    == "Engaged"
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
