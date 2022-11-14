from abc import ABC, abstractmethod
from json import dump, load
from pandas import DataFrame, Series


import falcon_alliance
import yaml
from pandas import isna, notna
from utils import ErrorType


class BaseDataValidation(ABC):
    """
    Base class that validates the data passed in.

    Implements base checks explained below (e.g. checking if the scout scouted the right driver station.)
    """

    def __init__(self, path_to_config: str = "config.yaml"):
        # Basic attributes
        self.tba_match_data = {}
        self.errors = []
        self.match_schedule = {}

        # Config attributes
        with open(path_to_config) as file:
            self.config = yaml.safe_load(file)

        self.path_to_output_file = self.config.get("path_to_output", "errors.json")
        self.path_to_data_file = self.config.get(
            "path_to_data",
            f"../data/{self.config['year']}{self.config['event_code']}_match_data.json",
        )

        self._event_key = str(self.config["year"]) + self.config["event_code"]
        # determines both if were using tba for match shedule and whether we're running tba checks
        self._run_with_tba = self.config.get("run_with_tba", True)

        # Setting up FalconAlliance (our connection to TBA) and retrieving match schedule
        self.api_client = falcon_alliance.ApiClient(
            api_key="6lcmneN5bBDYpC47FolBxp2RZa4AbQCVpmKMSKw9x9btKt7da5yMzVamJYk0XDBm"  # for testing purposes
        )

        with self.api_client:
            # make sure tba isn't down
            self._run_with_tba = (
                self._event_key not in self.api_client.status().down_events
            )

            if self._run_with_tba:
                self.get_match_schedule_tba()
            else:
                self.get_match_schedule_file()

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
        driver_station: int
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
        teams_on_alliance = list(map(
            lambda team: int(team.lstrip("frc")),
            teams_on_alliance
        ))

        if team_number not in teams_on_alliance:
            self.add_error(
                f"In {match_key}, {team_number} was NOT IN MATCH on the {alliance} alliance",
                error_type=ErrorType.INCORRECT_DATA,
            )

        elif (team_number) != teams_on_alliance[driver_station-1]:
            self.add_error(
                f"In {match_key}, {team_number} INCONSISTENT DRIVER STATION with schedule",
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
        # Check for 0% defense pct but given rating.
        if notna(defense_rating) and isna(defense_pct):
            self.add_error(
                f"In {match_key}, {team_number} rated for defense but NO DEFENSE PCT",
                error_type=ErrorType.MISSING_DATA,
            )

        # Check for missing defense rating.
        if isna(defense_rating) and notna(defense_rating):
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

    def add_error(self, error_message: str, error_type: ErrorType) -> None:
        """
        Adds an error to the dictionary containing all errors raised with data validation.

        :param error_type: Represents the error type (eg WARNING, CRITICAL, etc.). Value by default is ErrorType.ERROR.
        :param error_message: Message containing information about the error.
        :return:
        """
        self.errors.append(
            {
                "error_type": error_type._name_.replace("_", " "),
                "message": error_message,
            }
        )

    def output_errors(self) -> None:
        """
        Outputs errors within the _errors attribute (a dictionary) to a JSON file.
        The path to the JSON file is mentioned with the path_to_output_file attribute.

        :return: None
        """
        with open(self.path_to_output_file, "w") as file:
            dump(self.errors, file, indent=4)

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
                "Red": match.alliances["red"].team_keys,
                "Blue": match.alliances["blue"].team_keys,
            }

    def get_match_schedule_file(self) -> None:
        """
        Retrieves match_schedule from data/match_schedule.json unless different file was set in conifg

        :return: None
        """

        try:
            with open(
                self.config.get("path_to_match_schedule", "../data/match_schedule.json")
            ) as file:
                self.match_schedule = load(file)
        except FileNotFoundError:  # We want to ignore if it doesn't exist because get_match_schedule() will create it.
            pass

        # Writes match schedule to the corresponding JSON
        with open("../data/match_schedule.json", "w") as file:
            dump(self.match_schedule, file, indent=4)
