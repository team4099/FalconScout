import json

import falcon_alliance
import yaml
from utils import ErrorType, valid_match_key


class BaseDataValidation:
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

        self.path_to_output_file = self.config.get("path_to_output") or "output.json"
        self.path_to_data_file = (
            self.config.get("path_to_data")
            or f"../data/{self.config['year']}{self.config['event_code']}_match_data.json"
        )

        # Retrieves match schedule
        try:
            with open(
                self.config.get("path_to_match_schedule")
                or "../data/match_schedule.json"
            ) as file:
                self.match_schedule = json.load(file)
        except FileNotFoundError:  # We want to ignore if it doesn't exist because get_match_schedule() will create it.
            pass

        # Setting up FalconAlliance (our connection to TBA) and retrieving match schedule if it doesn't exist
        self.api_client = falcon_alliance.ApiClient(
            api_key="6lcmneN5bBDYpC47FolBxp2RZa4AbQCVpmKMSKw9x9btKt7da5yMzVamJYk0XDBm"  # for testing purposes
        )

        self._event_key = str(self.config["year"]) + self.config["event_code"]
        self._run_tba_checks = self.config.get("run_tba_checks")
        self.get_match_schedule()

    def check_submission_with_match_schedule(self, submission: dict) -> None:
        """
        Includes all checks relating match key and team number for a single submission.
        Checks key format and ensures it exist in schedule.
        Checks team number against schedule.
        Checks for correct DriverStation when scouting.

        :param submission: Representing a single submission in dictionary format.
        :return: None
        """
        match_key = str(submission["match_key"]).strip().lower()
        full_match_key = f"{self._event_key}_{match_key}"

        # Check if match key format is valid.
        if not valid_match_key(match_key):
            self.add_error(
                f"In {submission['match_key']}, {submission['team_number']} INVALID MATCH KEY"
            )
            return

        # Check if match key exists in schedule.
        if full_match_key not in self.match_schedule.keys():
            self.add_error(
                f"In {submission['match_key']}, {submission['team_number']} MATCH KEY NOT FOUND in schedule"
            )
            return

        # Check if the robot was in the match.
        team_number = submission["team_number"]
        alliance = submission["alliance"]
        if (
            f"frc{team_number}"
            not in self.match_schedule[full_match_key][alliance.lower()]
        ):
            self.add_error(
                f"frc{int(team_number)} was NOT IN MATCH {submission['match_key']}, on the {alliance} alliance"
            )
        else:
            # check for correct driver station
            scouted_driver_station = submission["driver_station"]
            scheduled_driver_station = (
                self.match_schedule[full_match_key][alliance.lower()].index(
                    f"frc{team_number}"
                )
                + 1
            )
            if scouted_driver_station != scheduled_driver_station:
                self.add_error(
                    f"In {submission['match_key']}, frc{team_number} INCONSISTENT DRIVER STATION with schedule"
                )

    def check_for_invalid_defense_data(self, submission: dict) -> None:
        """
        Checks if scouter gave defense or counter defense rating but stated that the robot didn't play defense/counter defense.
        Checks if scouter stated that robot played defense or counter defense but didn't give a corresponding rating.
        Checks if total defense played + counter defense played > 100% hence impossible.

        :param submission: Representing a single submission in dictionary format.
        :return: None
        """  # noqa
        defense_pct = submission["defense_pct"]
        defense_rating = submission["defense_rating"]
        counter_pct = submission["counter_defense_pct"]
        counter_rating = submission["counter_defense_rating"]

        # Check for 0% defense pct but given rating.
        if defense_pct == 0 and defense_rating != 0:
            self.add_error(
                f"In {submission['match_key']}, {submission['team_number']} rated for defense but NO DEFENSE PCT"
            )

        # Check for missing defense rating.
        if defense_rating == 0 and defense_pct != 0:
            self.add_error(
                f"In {submission['match_key']}, {submission['team_number']} MISSING DEFENSE RATING"
            )

        # Check for 0% counter defense pct but given rating.
        if counter_pct == 0 and counter_rating != 0:
            self.add_error(
                f"In {submission['match_key']}, {submission['team_number']} "
                f"rated for counter defense but NO COUNTER DEFENSE PCT"
            )

        # Check for missing counter defense rating.
        if counter_rating == 0 and counter_pct != 0:
            self.add_error(
                f"In {submission['match_key']}, {submission['team_number']} MISSING COUNTER DEFENSE RATING"
            )

        # Inconsistent defense + counter defense pct.
        if (defense_pct + counter_pct) > 1:
            self.add_error(
                f"In {submission['match_key']}, {submission['team_number']} DEFENSE AND COUNTER DEFENSE PCT TOO HIGH"
            )

    def add_error(
        self, error_message: str, error_type: ErrorType = ErrorType.ERROR
    ) -> None:
        """
        Adds an error to the dictionary containing all errors raised with data validation.

        :param error_type: Represents the error type (eg WARNING, CRITICAL, etc.). Value by default is ErrorType.ERROR.
        :param error_message: Message containing information about the error.
        :return:
        """
        self.errors.append({"error_type": error_type._name_, "message": error_message})

    def output_errors(self) -> None:
        """
        Outputs errors within the _errors attribute (a dictionary) to a JSON file.
        The path to the JSON file is mentioned with the path_to_output_file attribute.

        :return: None
        """
        with open(self.path_to_output_file, "w") as file:
            json.dump(self.errors, file)

    def get_match_schedule(self):
        """Retrieves match schedule if match schedule wasn't already passed in."""
        with self.api_client:
            self._run_tba_checks = (
                self._event_key not in self.api_client.status().down_events
            )

            # Sets match schedule and tba_match_data attributes, with tba_match_data being raw data.
            if self._run_tba_checks:
                match_schedule = falcon_alliance.Event(self._event_key).matches(
                    simple=True
                )

                for match in match_schedule:
                    self.tba_match_data[match.key] = match

                    self.match_schedule[match.key] = {
                        "red": match.alliances["red"].team_keys,
                        "blue": match.alliances["blue"].team_keys,
                    }

        # Writes match schedule to the corresponding JSON
        with open("../data/match_schedule.json", "w") as file:
            json.dump(self.match_schedule, file, indent=4)
