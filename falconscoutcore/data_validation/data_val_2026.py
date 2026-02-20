import json
from itertools import chain

from data_validation.base_data_val import BaseDataValidation
from data_validation.config.utils import (ErrorType, get_intersection_of_n_series)
from numpy import logical_or
from pandas import DataFrame, Series, concat, isna, notna


class DataValidation2026(BaseDataValidation):
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
        
        self.scored_more_than_eighty_in_auto(
            match_key=submission[self.config["match_key"]],
            team_number=submission[self.config["team_number"]],
            auto_points=submission[self.config["auto_singular_count"]]+submission[self.config["auto_batch_count"]]*["MAGANZINE PLACEHOLDER"] #TODO
        )

       

        if self._run_with_tba:
            self.tba_validate_climb_state(
                match_key=submission[self.config["match_key"]],
                team_number=submission[self.config["team_number"]],
                alliance=submission[self.config["alliance"]],
                driver_station=submission[self.config["driver_station"]],
                climb_level=submission[self.config["teleop_climb"]],
            )

   

    def scored_more_than_eighty_in_auto(
            self,
            match_key: str,
            team_number: int,
            auto_points: int,
    ):
        """Marks an error if more than 80 points were scored in auto."""
        if auto_points > 80:
            self.add_error(
                f"In {match_key}, {team_number} was said to have scored {auto_points} AUTO POINTS WHICH IS IMPOSSIBLE.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

    def tba_validate_climb_state(
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

        tba_climb_status = score_breakdown[f"endGameRobot{driver_station}"]

        

        if tba_climb_status != climb_level.replace(" ", "") and not parked:
            self.add_error(
                f"In {match_key}, {team_number} was said to have a climbing status of {climb_level.upper()} despite TBA marking them as {tba_climb_status.upper()}.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )
