from abc import ABC, abstractmethod
from collections import defaultdict
from itertools import chain
from json import dump, load
from typing import List

import falcon_alliance
import pandas as pd
import yaml
from data_validation.config.utils import ErrorType
from pandas import DataFrame, Series, notna, read_json


class BaseDataValidation(ABC):
    """
    Base class that validates the data passed in.

    Implements base checks explained below (e.g. checking if the scout scouted the right driver station.)
    """

    TBA_AUTO_ERROR_THRESHOLD = 1
    TBA_TELEOP_ERROR_THRESHOLD = 2

    RESCOUTING_ERROR_THRESHOLD = 20

    def __init__(self, path_to_config: str = "config.yaml"):
        # Basic attributes
        self.tba_match_data = {}
        self.errors = []
        self.match_schedule = {}

        # Config attributes
        with open(path_to_config) as file:
            self.config = yaml.safe_load(file)

        self.path_to_output_file = self.config.get("path_to_output", "data/errors.json")
        self.path_to_data_file = self.config.get(
            "path_to_data",
            f"data/{self.config['year']}{self.config['event_code']}_match_data.json",
        )
        self.path_to_scouting_rotations = self.config.get("path_to_scouting_rotations")

        self.df = read_json(self.path_to_data_file)

        self._event_key = str(self.config["year"]) + self.config["event_code"]
        # Determines both if were using tba for match schedule and whether we're running tba checks
        self._run_with_tba = self.config.get("run_with_tba", False)

        # Setting up FalconAlliance (our connection to TBA) and retrieving match schedule
        self.api_client = falcon_alliance.ApiClient(
            api_key="6lcmneN5bBDYpC47FolBxp2RZa4AbQCVpmKMSKw9x9btKt7da5yMzVamJYk0XDBm"  # for testing purposes
        )

        # Retrieve match data from event so far
        self.match_data = self.get_match_data()

        if self._run_with_tba:
            with self.api_client:
                # make sure tba isn't down
                self._run_with_tba = (
                    self._event_key not in self.api_client.status().down_events
                )

                if self._run_with_tba:
                    self.get_match_schedule_tba()

        if not self._run_with_tba:
            self.get_match_schedule_file()

        if self.path_to_scouting_rotations:
            with open(f"data/{self._event_key}_scouting_rotations.json") as file:
                self.scouting_rotations = load(file)
        else:
            self.scouting_rotations = []

    def get_match_data(self) -> dict:
        if self._run_with_tba:
            with self.api_client:
                event_matches = falcon_alliance.Event(self._event_key).matches()
                return {match.key: match for match in event_matches}
        else:
            return {}

    @abstractmethod
    def validate_data(self, scouting_data: list = None) -> None:
        """
        Runs all checks validating a single submission from 2022's game (Rapid React).

        :param scouting_data: Optional parameter containing scouting data mostly for testing purposes.
        :return:
        """
        pass

    @abstractmethod
    def validate_submission(self, submission: Series) -> None:
        """
        Runs all checks validating a single submission.

        :param submission: Series object containing a single submission of scouting data.
        :return:
        """
        pass

    def check_team_info_with_match_schedule(
        self,
        match_key: str,
        team_number: int,
        alliance: str,
        driver_station: int,
    ) -> None:
        """
        Checks if the team scouted was in the match on given alliance
        Checks if the team driverstation doesn't correspond to team scouted

        :param match_key: Key of match that was scouted.
        :param team_number: Number of team that was scouted (eg 4099).
        :param alliance: string either "Red' or 'Blue' of which alliance was scouted
        :param driver_station: int representing which driver station(1-3) was  scouted.
        """
        match_schedule_key = self._event_key + "_" + match_key
        teams_on_alliance = self.match_schedule[match_schedule_key][alliance]
        teams_on_alliance = [int(team.lstrip("frc")) for team in teams_on_alliance]

        if team_number not in teams_on_alliance:
            self.add_error(
                f"In {match_key}, {team_number} was NOT IN MATCH on the {alliance} alliance",
                ErrorType.MISSING_DATA,
                match_key,
                team_number,
            )

        elif (team_number) != teams_on_alliance[driver_station - 1]:
            self.add_error(
                f"In {match_key}, {team_number} INCONSISTENT DRIVER STATION with schedule",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )

        self.teams = self.get_teams()

    def check_team_numbers_for_each_match(self, scouting_data: pd.DataFrame) -> None:
        """
        Checks if a team was scouted/not double scouted.

        :param scouting_data: List containing data from each scout.
        :return: None
        """  # noqa
        data_by_match_key = defaultdict(lambda: defaultdict(list))

        for _, submission in scouting_data.iterrows():
            if notna(submission[self.config["match_key"]]):
                data_by_match_key[submission[self.config["match_key"]].strip().lower()][
                    submission[self.config["alliance"]].lower()
                ].append(submission)

        for match_key, match_data in data_by_match_key.items():
            for alliance in ("red", "blue"):
                try:
                    teams = self.match_schedule[f"{self._event_key}_{match_key}"][
                        alliance
                    ]
                except KeyError as e:
                    print(e)
                    continue

                team_numbers = [
                    f"frc{submission[self.config['team_number']]}"
                    for submission in match_data[alliance]
                ]

                if len(match_data[alliance]) < 3:
                    for driver_station, team in enumerate(teams):
                        if team not in team_numbers:
                            scout_responsible = (
                                self.scouting_rotations[match_key][driver_station]
                                if self.scouting_rotations
                                else ""
                            )
                            self.add_error(
                                f"In {match_key}, {team} was NOT SCOUTED",
                                ErrorType.MISSING_DATA,
                                match_key,
                                int(team.strip("frc")),
                                scout_id=scout_responsible,
                            )

    def remove_duplicate_errors(self) -> None:
        """Edits self.errors to remove any duplicate errors found."""
        self.errors = [
            dict(error)
            for error in set([tuple(error.items()) for error in self.errors])
        ]

    def add_error(
        self,
        error_message: str,
        error_type: ErrorType,
        match_key: str,
        team_id: int = 9999,
        scout_id: str = "N/A",
        alliance: str = "N/A",
    ) -> None:
        """
        Adds an error to the dictionary containing all errors raised with data validation.

        :param error_type: Represents the error type (eg WARNING, CRITICAL, etc.). Value by default is ErrorType.ERROR.
        :param error_message: Message containing information about the error.
        :param match_key: The key of the match where the error is being raised from.
        :param team_id: The team number where the error is being raised from.
        :param scout_id: The scout responsible for the error being raised.
        :param alliance: The alliance where the error is being raised from.
        :return:
        """
        # Explicit conversions to string and integers because of NumPy types that might be passed in.
        self.errors.append(
            {
                "error_type": error_type.name.replace("_", " "),
                "error_number": error_type.value,
                "message": error_message,
                "match": str(match_key),
                "scout_id": scout_id,
                "team_id": int(team_id),
                "alliance": alliance,
            }
        )

    def output_errors(self) -> None:
        """
        Outputs errors within the _errors attribute (a dictionary) to a JSON file.
        The path to the JSON file is mentioned with the path_to_output_file attribute.

        :return: None
        """
        self.remove_duplicate_errors()

        # Add rescouting flag for matches with a 10 or more cumulative "error amount" (enum value).
        error_dataframe = DataFrame.from_dict(self.errors)

        if not error_dataframe.empty:
            for match_key, error_amount in (
                error_dataframe[error_dataframe["error_type"] != "RESCOUT MATCH"]
                .groupby("match")["error_number"]
                .sum()
                .items()
            ):
                if error_amount >= self.RESCOUTING_ERROR_THRESHOLD:
                    self.add_error(
                        f"In {match_key}, a cumulative amount of {error_amount} gathered "
                        f"from ERRORS were found, this match should be RESCOUTED.",
                        ErrorType.RESCOUT_MATCH,
                        match_key,
                    )

        self.remove_duplicate_errors()

        with open(self.path_to_output_file, "w") as file:
            dump(
                sorted(
                    self.errors,
                    key=lambda error: int(
                        error["match"]
                        .replace("qm", "")
                        .replace("sf", "")
                        .replace("f", "")
                    ),
                    reverse=True,
                ),
                file,
                indent=4,
            )

    def get_match_schedule_tba(self) -> None:
        """
        Retrieves match schedule from tba

        :return: None
        """

        # Sets match schedule and tba_match_data attributes, with tba_match_data being raw data.
        match_schedule = falcon_alliance.Event(self._event_key).matches()

        for match in match_schedule:
            self.tba_match_data[match.key] = match
            self.match_schedule[match.key] = {
                "red": match.alliances["red"].team_keys,
                "blue": match.alliances["blue"].team_keys,
            }

    def get_match_schedule_file(self) -> None:
        """
        Retrieves match_schedule from data/match_schedule.json unless different file was set in conifg

        :return: None
        """

        try:
            with open(
                self.config.get("path_to_match_schedule", "data/match_schedule.json")
            ) as file:
                self.match_schedule = load(file)
        except FileNotFoundError:  # We want to ignore if it doesn't exist because get_match_schedule() will create it.
            pass

        # Writes match schedule to the corresponding JSON
        with open("data/match_schedule.json", "w") as file:
            dump(self.match_schedule, file, indent=2)

    def get_teams(self) -> List[int]:
        """
        Gets list of all teams from match schedule

        :return List of all team numbers
        """

        schedule_df = read_json("data/match_schedule.json")

        # Retrieve all alliances across all matches
        all_alliances = schedule_df.loc["red"] + schedule_df.loc["blue"]

        # Flatten alliance lists into one large list (with no repeating teams) and strip "frc"
        all_team_identifiers = list(set(chain(*all_alliances)))
        all_teams = list(map(lambda x: int(x[3:]), all_team_identifiers))

        return all_teams
