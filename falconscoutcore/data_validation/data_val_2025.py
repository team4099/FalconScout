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

    def validate_data(self, scouting_data: list = None) -> None:
        """
        Runs all checks for validating data from 2025's game (Reefscape).

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

        if self._run_with_tba:
            self.tba_validate_total_auto_cycles(scouting_data)
            self.tba_validate_total_teleop_cycles(scouting_data)

        if not scouting_data.empty:
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

            # if self._run_with_tba:
            #     self.tba_validate_auto_game_pieces_scored(scouting_data)
            #     self.tba_validate_teleop_game_pieces_scored(scouting_data)

            self.output_errors()

    def validate_submission(self, submission: Series) -> None:
        self.scored_more_than_one_without_leaving_in_auto(
            match_key=submission[self.config["match_key"]],
            team_number=submission[self.config["team_number"]],
            auto_coral=submission[self.config["auto_coral_l1"]] + submission[self.config["auto_coral_l2"]]+submission[self.config["auto_coral_l3"]]+submission[self.config["auto_coral_l4"]],
            auto_algae=submission[self.config["auto_processor"]]+submission[self.config["auto_barge"]],
            auto_leave=submission[self.config["auto_leave"]],
        )
        self.scored_more_than_eight_in_auto(
            match_key=submission[self.config["match_key"]],
            team_number=submission[self.config["team_number"]],
            auto_coral=submission[self.config["auto_coral_l1"]] + submission[self.config["auto_coral_l2"]]+submission[self.config["auto_coral_l3"]]+submission[self.config["auto_coral_l4"]],
            auto_algae=submission[self.config["auto_processor"]]+submission[self.config["auto_barge"]],
        )

        self.scored_more_than_twelve_coral_on_level(
            match_key=submission[self.config["match_key"]],
            team_number=submission[self.config["team_number"]],
            coral_l2=submission[self.config["teleop_coral_l2"]] + submission[self.config["auto_coral_l2"]],
            coral_l3=submission[self.config["teleop_coral_l3"]] + submission[self.config["auto_coral_l3"]],
            coral_l4=submission[self.config["teleop_coral_l4"]] + submission[self.config["auto_coral_l4"]],
        )

        self.scored_more_than_fifteen_algae(
            match_key=submission[self.config["match_key"]],
            team_number=submission[self.config["team_number"]],
            algae=submission[self.config["auto_processor"]] + submission[self.config["auto_barge"]] + submission[self.config["teleop_algae_processor"]] + submission[self.config["teleop_algae_barge"]],
        )

        if self._run_with_tba:
            self.tba_validate_climbing_state(
                match_key=submission[self.config["match_key"]],
                team_number=submission[self.config["team_number"]],
                alliance=submission[self.config["alliance"]],
                driver_station=submission[self.config["driver_station"]],
                parked=submission[self.config["endgame_parked"]],
                climb_level=submission[self.config["endgame_climb_status"]],
            )

    def scored_more_than_one_without_leaving_in_auto(
            self,
            match_key: str,
            team_number: int,
            auto_coral: int,
            auto_algae: int,
            auto_leave: bool,
    ):
        """Marks an error if more than one piece was scored in auto without leaving."""
        if (auto_coral != 0 or auto_algae > 1) and not auto_leave:
            self.add_error(
                f"In {match_key}, {team_number} was said to have scored {auto_coral} CORAL GAME PIECES AND {auto_algae} ALGAE GAME PIECES IN AUTO WITHOUT LEAVING WHICH IS IMPOSSIBLE.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

    def scored_more_than_eight_in_auto(
            self,
            match_key: str,
            team_number: int,
            auto_coral: int,
            auto_algae: int,
    ):
        """Marks an error if more than one piece was scored in auto without leaving."""
        if auto_coral + auto_algae > 8:
            self.add_error(
                f"In {match_key}, {team_number} was said to have scored {auto_coral} CORAL GAME PIECES AND {auto_algae} ALGAE GAME PIECES IN AUTO WHICH IS IMPOSSIBLE.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

    def tba_validate_total_auto_cycles(self, scouting_data: DataFrame):
        """Validates the total auto speaker/amp cycles for an alliance with TBA."""
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

            # TODO: Find the TBA keys for these stats
            actual_auto_coral = score_breakdown[""]
            scouted_auto_coral_l1 = submissions_by_alliance[self.config["auto_coral_l1"]].sum()
            scouted_auto_coral_l2 = submissions_by_alliance[self.config["auto_coral_l2"]].sum()
            scouted_auto_coral_l3 = submissions_by_alliance[self.config["auto_coral_l3"]].sum()
            scouted_auto_coral_l4 = submissions_by_alliance[self.config["auto_coral_l4"]].sum()
            scouted_auto_coral = scouted_auto_coral_l1 + scouted_auto_coral_l2 + scouted_auto_coral_l3 + scouted_auto_coral_l4

            actual_auto_algae = score_breakdown[""]
            scouted_auto_algae_processor = submissions_by_alliance[self.config["auto_processor"]].sum()
            scouted_auto_algae_barge = submissions_by_alliance[self.config["auto_barge"]].sum()
            scouted_auto_algae = scouted_auto_algae_barge + scouted_auto_algae_processor

            scouted_auto_pieces = scouted_auto_coral + scouted_auto_algae
            actual_auto_pieces = actual_auto_coral + actual_auto_algae

            if (
                    scouted_auto_pieces != actual_auto_pieces
                    and abs(scouted_auto_pieces - actual_auto_pieces)
                    >= self.TBA_AUTO_ERROR_THRESHOLD
            ):
                self.add_error(
                    f"In {match_key}, the {alliance.upper()} alliance was said to have scored"
                    f" {scouted_auto_coral} CORAL IN THE REEF and {scouted_auto_algae} ALGAE IN THE NET & PROCESSOR during AUTO "
                    f"but actually scored {actual_auto_coral} CORAL IN THE REEF and {actual_auto_algae} ALGAE IN THE NET & PROCESSOR.",
                    ErrorType.INCORRECT_DATA,
                    match_key,
                    alliance=alliance,
                )

    def scored_more_than_twelve_coral_on_level(
            self, match_key: str, team_number: int, coral_l2: int, coral_l3: int, coral_l4: int,
    ):
        """Marks an error if more than twelve coral were scored on any level l2-l4 (impossible)."""
        if coral_l2 > 12:
            self.add_error(
                f"In {match_key}, {team_number} was said to have scored {coral_l2} CORAL ON LEVEL 2 WHICH IS IMPOSSIBLE.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )
        if coral_l3 > 12:
            self.add_error(
                f"In {match_key}, {team_number} was said to have scored {coral_l3} CORAL ON LEVEL 3 WHICH IS IMPOSSIBLE.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )
        if coral_l4 > 12:
            self.add_error(
                f"In {match_key}, {team_number} was said to have scored {coral_l4} CORAL ON LEVEL 4 WHICH IS IMPOSSIBLE.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

    def scored_more_than_fifteen_algae(
               self, match_key: str, team_number: int, algae: int,
    ):
        if algae > 15:
            self.add_error(
                f"In {match_key}, {team_number} was said to have scored {algae} ALGAE WHICH IS IMPOSSIBLE.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

    def tba_validate_total_teleop_cycles(self, scouting_data: DataFrame):
        """Validates the total teleop coral/algae cycles for an alliance with TBA."""
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

            # TODO: Find the TBA keys for these stats
            actual_teleop_coral = score_breakdown[""]
            scouted_teleop_coral_l1 = submissions_by_alliance[self.config["teleop_coral_l1"]].sum()
            scouted_teleop_coral_l2 = submissions_by_alliance[self.config["teleop_coral_l2"]].sum()
            scouted_teleop_coral_l3 = submissions_by_alliance[self.config["teleop_coral_l3"]].sum()
            scouted_teleop_coral_l4 = submissions_by_alliance[self.config["teleop_coral_l4"]].sum()
            scouted_teleop_coral = scouted_teleop_coral_l1 + scouted_teleop_coral_l2 + scouted_teleop_coral_l3 + scouted_teleop_coral_l4

            actual_teleop_algae = score_breakdown[""]
            scouted_teleop_algae_barge = submissions_by_alliance[self.config["teleop_algae_barge"]].sum()
            scouted_teleop_algae_processor = submissions_by_alliance[self.config["teleop_algae_processor"]].sum()
            scouted_teleop_algae = scouted_teleop_algae_processor + scouted_teleop_algae_barge

            scouted_teleop_pieces = scouted_teleop_coral + scouted_teleop_algae
            actual_teleop_pieces = actual_teleop_coral + actual_teleop_algae

            if (
                    scouted_teleop_pieces != actual_teleop_pieces
                    and abs(scouted_teleop_pieces - actual_teleop_pieces)
                    >= self.TBA_TELEOP_ERROR_THRESHOLD
            ):
                self.add_error(
                    f"In {match_key}, the {alliance.upper()} alliance was said to have scored"
                    f" {scouted_teleop_coral} CORAL and {scouted_teleop_algae} ALGAE during TELEOP "
                    f"but actually scored {scouted_teleop_coral} CORAL and {actual_teleop_algae} ALGAE.",
                    ErrorType.INCORRECT_DATA,
                    match_key,
                    alliance=alliance,
                )

    def tba_validata_climb_state(
            self,
            match_key: str,
            team_number: int,
            alliance: int,
            driver_station: int,
            parked: bool,
            climb_level: str
        ) -> None:
        """Validates the final climb state of the robot using TBA data."""
        try:
            score_breakdown = self.match_data[
                f"{self._event_key}_{match_key}"
            ].score_breakdown[alliance.lower()]
        except KeyError as e:
            raise KeyError(
                "No matches to retrieve data from OR invalid match key, check scouting data."
            ) from e

        # TODO: Find the TBA Key for this stat
        tba_climb_status = score_breakdown[""]

        if tba_climb_status == "Parked" and not parked:
            self.add_error(
                f"In {match_key}, {team_number} was said to have NOT PARKED despite TBA marking them as PARKED.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

        if tba_climb_status != climb_level and not parked:
            self.add_error(
                f"In {match_key}, {team_number} was said to have a climbing status of {climb_level.upper()} despite TBA marking them as {tba_climb_status.upper()}.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )
