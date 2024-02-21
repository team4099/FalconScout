import json
from itertools import chain

from data_validation.base_data_val import BaseDataValidation
from data_validation.config.constants import ChargedUp
from data_validation.config.utils import (ErrorType,
                                          get_intersection_of_n_series)
from numpy import logical_or
from pandas import DataFrame, Series, concat, isna, notna


class DataValidation2024(BaseDataValidation):
    def __init__(self, path_to_config: str = "config.yaml"):
        super().__init__(path_to_config)

    def validate_data(self, scouting_data: list = None) -> None:
        """
        Runs all checks for validating data from 2024's game (Crescendo).

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
            self.tba_validate_total_trap_cycles(scouting_data)

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

        self.scored_more_than_one_without_leaving_in_auto(
            match_key=submission[self.config["match_key"]],
            team_number=submission[self.config["team_number"]],
            auto_speaker=submission[self.config["auto_speaker"]],
            auto_amp=submission[self.config["auto_amp"]],
            auto_leave=submission[self.config["auto_leave"]],
        )

        self.scored_more_than_four_without_centerline_in_auto(
            match_key=submission[self.config["match_key"]],
            team_number=submission[self.config["team_number"]],
            auto_speaker=submission[self.config["auto_speaker"]],
            auto_amp=submission[self.config["auto_amp"]],
            auto_used_centerline=submission[self.config["auto_centerline"]],
        )

        self.scored_more_than_seven_pieces_in_auto(
            match_key=submission[self.config["match_key"]],
            team_number=submission[self.config["team_number"]],
            auto_speaker=submission[self.config["auto_speaker"]],
            auto_amp=submission[self.config["auto_amp"]],
        )

        self.check_for_if_they_harmonized_without_climbing(
            match_key=submission[self.config["match_key"]],
            team_number=submission[self.config["team_number"]],
            climbed=submission[self.config["climbed"]],
            harmonized=submission[self.config["harmonized"]],
        )

        self.check_for_invalid_defense_data(
            match_key=submission[self.config["match_key"]],
            team_number=submission[self.config["team_number"]],
            defense_time=submission[self.config["defense_time"]],
            defense_skill=submission[self.config["defense_skill"]],
        )

        if self._run_with_tba:
            self.tba_validate_climb_state(
                match_key=submission[self.config["match_key"]],
                team_number=submission[self.config["team_number"]],
                alliance=submission[self.config["alliance"]],
                driver_station=submission[self.config["driver_station"]],
                parked=submission[self.config["parked"]],
                climbed=submission[self.config["climbed"]],
            )

    def tba_validate_climb_state(
        self,
        match_key: str,
        team_number: int,
        alliance: str,
        driver_station: int,
        parked: bool,
        climbed: bool,
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

        tba_climb_status = score_breakdown[f"endGameRobot{driver_station}"]

        if tba_climb_status == "Parked" and not parked:
            self.add_error(
                f"In {match_key}, {team_number} was said to have NOT PARKED despite TBA marking them as PARKED.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

        if "Stage" in tba_climb_status and not climbed:
            self.add_error(
                f"In {match_key}, {team_number} was said to have NOT CLIMBED despite TBA marking them as having CLIMBED.",
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

            actual_auto_speaker = score_breakdown["autoSpeakerNoteCount"]
            scouted_auto_speaker = submissions_by_alliance[self.config["auto_speaker"]].sum()

            actual_auto_amp  = score_breakdown["autoAmpNoteCount"]
            scouted_auto_amp = submissions_by_alliance[self.config["auto_amp"]].sum()

            scouted_auto_pieces = scouted_auto_speaker + scouted_auto_amp
            actual_auto_pieces = actual_auto_speaker + actual_auto_amp

            if (
                scouted_auto_pieces != actual_auto_pieces
                and abs(scouted_auto_pieces - actual_auto_pieces)
                >= self.TBA_AUTO_ERROR_THRESHOLD
            ):
                self.add_error(
                    f"In {match_key}, the {alliance.upper()} alliance was said to have scored"
                    f" {scouted_auto_speaker} NOTES IN THE SPEAKER and {scouted_auto_amp} NOTES IN THE AMP during AUTO "
                    f"but actually scored {actual_auto_speaker} NOTES IN THE SPEAKER and {actual_auto_amp} NOTES IN THE AMP.",
                    ErrorType.INCORRECT_DATA,
                    match_key,
                    alliance=alliance,
                )
    
    def tba_validate_total_teleop_cycles(self, scouting_data: DataFrame):
        """Validates the total teleop speaker/amp cycles for an alliance with TBA."""
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

            actual_teleop_speaker = score_breakdown["teleopSpeakerNoteCount"] + score_breakdown["teleopSpeakerNoteAmplifiedCount"]
            scouted_teleop_speaker = submissions_by_alliance[self.config["teleop_speaker"]].sum()

            actual_teleop_amp  = score_breakdown["teleopAmpNoteCount"]
            scouted_teleop_amp = submissions_by_alliance[self.config["teleop_amp"]].sum()

            scouted_teleop_pieces = scouted_teleop_speaker + scouted_teleop_amp
            actual_teleop_pieces = actual_teleop_speaker + actual_teleop_amp

            if (
                scouted_teleop_pieces != actual_teleop_pieces
                and abs(scouted_teleop_pieces - actual_teleop_pieces)
                >= self.TBA_TELEOP_ERROR_THRESHOLD
            ):
                self.add_error(
                    f"In {match_key}, the {alliance.upper()} alliance was said to have scored"
                    f" {scouted_teleop_speaker} NOTES IN THE SPEAKER and {scouted_teleop_amp} NOTES IN THE AMP during TELEOP "
                    f"but actually scored {actual_teleop_speaker} NOTES IN THE SPEAKER and {actual_teleop_amp} NOTES IN THE AMP.",
                    ErrorType.INCORRECT_DATA,
                    match_key,
                    alliance=alliance,
                )
    
    def tba_validate_total_trap_cycles(self, scouting_data: DataFrame):
        """Validates the total trap cycles for an alliance with TBA."""
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

            actual_trap_cycles = score_breakdown["trapCenterStage"] + score_breakdown["trapStageLeft"] + score_breakdown["trapStageRight"]
            scouted_trap_cycles = submissions_by_alliance[self.config["teleop_trap"]].sum()

            if actual_trap_cycles != scouted_trap_cycles:
                self.add_error(
                    f"In {match_key}, the {alliance.upper()} alliance was said to have scored"
                    f" {scouted_trap_cycles} NOTES IN THE TRAP "
                    f"but actually scored {actual_trap_cycles} NOTES IN THE TRAP.",
                    ErrorType.INCORRECT_DATA,
                    match_key,
                    alliance=alliance,
                )

    def scored_more_than_one_without_leaving_in_auto(
        self,
        match_key: str,
        team_number: int,
        auto_speaker: int,
        auto_amp: int,
        auto_leave: bool,
    ):
        """Marks an error if more than one piece was scored in auto without leaving."""
        if auto_speaker + auto_amp > 1 and not auto_leave:
            self.add_error(
                f"In {match_key}, {team_number} was said to have scored {auto_speaker + auto_amp} GAME PIECES IN AUTO WITHOUT LEAVING WHICH IS IMPOSSIBLE.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

    def scored_more_than_four_without_centerline_in_auto(
        self,
        match_key: str,
        team_number: int,
        auto_speaker: int,
        auto_amp: int,
        auto_used_centerline: bool,
    ):
        """Marks an error if more than four pieces were scored in auto without using the centerline notes."""
        if auto_speaker + auto_amp > 4 and not auto_used_centerline:
            self.add_error(
                f"In {match_key}, {team_number} was said to have scored {auto_speaker + auto_amp} GAME PIECES IN AUTO WITHOUT USING THE CENTERLINE NOTES WHICH IS IMPOSSIBLE.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

    def scored_more_than_seven_pieces_in_auto(
        self, match_key: str, team_number: int, auto_speaker: int, auto_amp: int
    ):
        """Marks an error if more than nine pieces were scored in auto (impossible)."""
        if auto_speaker + auto_amp > 9 and not auto_leave:
            self.add_error(
                f"In {match_key}, {team_number} was said to have scored {auto_speaker + auto_amp} GAME PIECES IN AUTO WHICH IS IMPOSSIBLE.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

    def check_for_if_they_harmonized_without_climbing(
        self, match_key: str, team_number: int, climbed: bool, harmonized: bool
    ):
        if harmonized and not climbed:
            self.add_error(
                f"In {match_key}, {team_number} was said to have HARMONIZED WITHOUT CLIMBING WHICH IS IMPOSSIBLE.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

    def check_for_invalid_defense_data(
        self, match_key: str, team_number: int, defense_time: str, defense_skill: str
    ):
        """Checks for missing data if the scouter forgot to mark down either the defense time or the defense skill."""
        if defense_time and "Never" not in defense_time and not defense_skill:
            self.add_error(
                f"In {match_key}, {team_number} was said to have spent time DEFENDING but the scouter forgot to mark down their DEFENSE SKILL.",
                ErrorType.MISSING_DATA,
                match_key,
                team_number,
            )
        elif (not defense_time or "Never" in defense_time) and defense_skill:
            self.add_error(
                f"In {match_key}, {team_number} had a DEFENSE SKILL marked down but the scouter forgot to mark down how long they DEFENDED FOR.",
                ErrorType.MISSING_DATA,
                match_key,
                team_number,
            )
