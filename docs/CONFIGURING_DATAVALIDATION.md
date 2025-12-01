# DataValidation 📔

Datavalidation is a system which scans scouting data as its collected and flags possible data entry errors. The scouting admin is then alerted to these possible errors. This system is written in `python` and is run after scouting data for each match is collected.


## Configuring Validation

To configure datavalidation you only need to edit a couple fields in the `config.yaml` file. This file cand be found under `/backend/data_validation` directory.

Example:
```
year: 2025
event_code: "bob"
```

### Required Configuration Fields

 - `year`
    - specifies the year the competition is taking place(i.e. 2026)
 -  `event_code`
    - a string, written in all lowercase letters, which corresponds to the given event and can be found on TBA (i.e. 'iri', 'cmptx')

Additionally, a json file must exist in the `backend/data` directory in the format `{year}{event_code}_match_data.json` where {year} and {event_code} are replaced by the values specified in the `config.yaml` file.

### Optional Configuration Fields
 - `run_with_tba`
    - determines whether match schedule will be retrieved from tba or from file, also determines if checks based on TBA (The Blue Alliance) data will run
    - default: `true`

### Match Schedule Configuration
A couple of the checks in the datavalidation software rely on having access to an accurate match schedule. These checks are important since they ensure that the data collected corresponds to the correct team number. 

By default, the software will attempt to retrieve the match schedule using TBA's api. However, at smaller competitions its possible that TBA may not have a copy of match schedule ready in time for the competition. In that case the scouting admin is able to edit a copy of the match schedule by hand.

To do this the `run_with_tba` configuration field must be specified as `false` in the `config.yaml` file. The `../data/match_schedule.json` file, which currently contains the match schedule from `2024ash`, can then be edited.

### Making DataValidation Optional
 
## Code Structure 
Datavalidation uses inheritance to provide teams with some level of base functionality and allow them to add their own data checks
- `BaseDataValidation` Class
    - At the heart of the DataValidation software is a class called `BaseDataValidation`. This class contains basic checks which are essential to validating data from any scouting app(i.e. match schedule checks, defense checks).
    - It also includes two important abstract methods `validate_data` and `validate_submission`, these two methods must be implimented in any child class and are where other checks are called from.
- `DataValidation2025` Child Class
    - Inherits `BaseDataValidation`
        ```
        class DataValidation2025(BaseDataValidation):
            def __init__(self, path_to_config: str = "config yaml"):
                super().__init__(path_to_config)
        ```
    - Contains checks on data for a  specific years game
    - `validate_data` method
        - takes in all scouting data
        - runs checks with require data from multiple matches(i.e. statistical outliers)
        - runs `validate_submission` on each data submission
    - `validate_submission` method
        - takes in a single submission as parameter, a submission refers to the set of data collected by one scout during one match
        - calls all methods which check data from one submisison

### Writing Custom Checks
 - Each check is a method of the `DatValidation2025` class and should take in the data fields it uses as parameters
   - it is recommended to include the `match_key` and `team_number` as parameters of any check since they can be used as identifiers in the error message
 - Example data check function signature:
    ```
    def scored_more_than_eight_in_auto(
            self,
            match_key: str,
            team_number: int,
            auto_coral: int,
            auto_algae: int,
    ):
    ```
 - Teams may then implement whatever logic they like in the function body
 - To flag an error you must call the `add_error` method which takes two arguments the `error_message` and the `error_type`
    - The `error_message` is simply a string which describes the error
    - The `error_type` takes in a value from a predefined enum which is used to categorize the error
        - Here are the possible `error_type` values
            ```
            class ErrorType(Enum):
                DEBUG = 0
                INFO = 1
                WARNING = 2
                INCORRECT_DATA = 3
                EXTRA_DATA = 4
                MISSING_DATA = 5
                CRITICAL = 6
                RESCOUT_MATCH = 7
            ```
    - Example call to `add_error`
        ```
         if auto_coral + auto_algae > 8:
            self.add_error(
                f"In {match_key}, {team_number} was said to have scored {auto_coral} CORAL GAME PIECES AND {auto_algae} ALGAE GAME PIECES IN AUTO WHICH IS IMPOSSIBLE.",
                ErrorType.INCORRECT_DATA,
                match_key,
                team_number,
            )
        ```
 - Lastly to run the check the function must be called in either `validate_submission` or `validate_data` and pass in the required data arguments
 - Example data check function call
    ```
     def validate_submission(self, submission: Series) -> None:
        self.scored_more_than_eight_in_auto(
            match_key=submission[self.config["match_key"]],
            team_number=submission[self.config["team_number"]],
            auto_coral=submission[self.config["auto_coral_l1"]] + submission[self.config["auto_coral_l2"]]+submission[self.config["auto_coral_l3"]]+submission[self.config["auto_coral_l4"]],
            auto_algae=submission[self.config["auto_processor"]]+submission[self.config["auto_barge"]],
        )
    ```