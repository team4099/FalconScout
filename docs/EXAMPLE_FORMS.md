# Example Scouting App Forms

These examples are already in the app right now but we have them here as well for documentation sake

## Core
```
--------------- config.json ---------------
{
    "data_config": {
        "delimiter": ",",
        "data_labels": [
            "scout_id",
            "match_key",
            "team_number",
            "alliance",
            "driver_station",
            "preloaded_cargo",
            "auto_lower_hub",
            "auto_upper_hub",
            "auto_misses",
            "taxied",
            "auto_shooting_zones",
            "teleop_lower_hub",
            "teleop_upper_hub",
            "teleop_misses",
            "teleop_shooting_zones",
            "attempted_low",
            "attempted_mid",
            "attempted_high",
            "attempted_traversal",
            "climb_time",
            "final_climb_type",
            "defense_pct",
            "defense_rating",
            "counter_defense_pct",
            "counter_defense_rating",
            "driver_rating",
            "auto_notes",
            "teleop_notes",
            "misc_notes"
        ],
        "json_file": "./data/2022iri_match_data.json",
        "csv_file": "./data/2022iri_match_data.csv"
    },
    "repo_config": {
        "repo": "AlphaPranav9102/storage",
        "update_csv": "data.csv",
        "update_json": "data.json"
    }
}

--------------- config.yaml ---------------
# core setup features
year: 2022
event_code: "iri"
run_with_tba: True

# required translation
match_key: "match_key"
team_number: "team_number"

# optional parameters - if it is needed for a data check and is
# not listed, the check will not run

# Rapid React 2022: hyper-specific parameters
auto_lower_hub: "auto_lower_hub"
auto_upper_hub: "auto_upper_hub"
auto_misses: "auto_misses"
auto_shooting_zones: "auto_shooting_zones"
teleop_lower_hub: "teleop_lower_hub"
teleop_upper_hub: "teleop_upper_hub"
teleop_misses: "teleop_misses"
teleop_shooting_zones: "teleop_shooting_zones"
taxied: "taxied"
final_climb_type: "final_climb_type"

# general game parameters
alliance: "alliance"
driver_station: "driver_station"
defense_pct: "defense_pct"
counter_defense_pct: "counter_defense_pct"
defense_rating: "defense_rating"
counter_defense_rating: "counter_defense_rating"
```

## Scouting App
### Pit Scouting
```
{
    "name": "Pit Scouting",
    "description": "Gather qualitative data on robots in pits.",
    "components": [
        {
            "type": "GenericHeaderOne",
            "text": "Pit Scouting",
            "id": "titleheader"
        },
        {
            "type": "GenericTextInput",
            "text": "Scout Name",
            "placeholder": [
                "Pranav"
            ],
            "id": "scoutid"
        },
        {
            "type": "GenericTextInput",
            "text": "Team Name",
            "placeholder": [
                "The Falcons"
            ],
            "id": "teamname"
        },
        {
            "type": "GenericTextInput",
            "text": "Team Number",
            "placeholder": [
                "4099"
            ],
            "id": "teamnumber"
        },
        {
            "type": "Spacing"
        },
        {
            "type": "GenericHeaderTwo",
            "text": "Controls",
            "id": "controlsheader"
        },
        {
            "type": "GenericTextInput",
            "text": "How many backup batteries",
            "placeholder": [
                "4"
            ],
            "id": "batterycount"
        },
        {
            "type": "GenericCheckboxSelect",
            "text": "Autos",
            "options": [
                "1 ball",
                "2 ball",
                "3 ball",
                "4 ball",
                "5 ball",
                "6 ball",
                "1 ball steal",
                "2 ball stall",
                "gremlin auto",
                "counter auto"
            ],
            "id": "autoselect"
        },
        {
            "type": "GenericRadioSelect",
            "text": "Language",
            "options": [
                "C++",
                "Java",
                "Labview",
                "Kotlin",
                "Python"
            ],
            "id": "languageselect"
        },
        {
            "type": "Spacing"
        },
        {
            "type": "GenericHeaderTwo",
            "text": "Mech",
            "id": "mechheader"
        },
        {
            "type": "GenericRadioSelect",
            "text": "Drivetrain",
            "options": [
                "swerve",
                "tank",
                "rhino",
                "mecanum",
                "omni"
            ],
            "id": "drivetrainselect"
        },
        {
            "type": "GenericRadioSelect",
            "text": "Intake Method",
            "options": [
                "single intake from ground",
                "double intake from ground",
                "terminal intake"
            ],
            "id": "intakeselect"
        },
        {
            "type": "GenericCheckboxSelect",
            "text": "Max Cargo Storage",
            "options": [
                "1",
                "2",
                "3"
            ],
            "id": "cargoselect"
        },
        {
            "type": "Spacing"
        },
        {
            "type": "GenericHeaderTwo",
            "text": "Strategy",
            "id": "strategyheader"
        },
        {
            "type": "GenericCheckboxSelect",
            "text": "Which hub",
            "options": [
                "Upper Hub",
                "Lower Hub"
            ],
            "id": "hubselect"
        },
        {
            "type": "GenericCheckboxSelect",
            "text": "Shooting zones",
            "options": [
                "tarmac",
                "fender",
                "terminal",
                "launchpad",
                "elsewhere"
            ],
            "id": "zoneselect"
        },
        {
            "type": "GenericRadioSelect",
            "text": "Max Climb level",
            "options": [
                "low",
                "mid",
                "high",
                "traversal",
                "no climb"
            ],
            "id": "climbselect"
        },
        {
            "type": "SliderInput",
            "text": "Climb time",
            "options": [
                "0",
                "15"
            ],
            "id": "climbtime"
        },
        {
            "type": "GenericTextArea",
            "text": "Other notes",
            "placeholder": [
                "4099 robot bad"
            ],
            "id": "robotnotes"
        },
        {
            "type": "DarkButton",
            "text": "Submit",
            "id": "result"
        }
    ],
    "export": {
        "order": ["scoutid", "teamname", "robotnotes"],
        "delimiter": ";"

    }
}
```

### 2018 Scouting App
Missing some components that may be build in the 2023 season.
```
{
    "name": "2018 Scouting Page",
    "description": "Collect general data for each match",
    "components": [
        {
            "type": "GenericHeaderOne",
            "text": "2018 Scouting Page"
        },
        {
            "type": "GenericTextInput",
            "text": "Scout Name",
            "placeholder": [
                "pranav"
            ],
            "id": "scoutid"
        },
        {
            "type": "DropdownTextInput",
            "text": "Match Key",
            "id": "matchkey",
            "options": ["qm", "qf", "sf", "f"],
            "placeholder": ["match id"]
        },
        {
            "type": "GenericRadioSelect",
            "text": "Alliance",
            "id": "alliance",
            "options": ["red", "blue"]
        },
        {
            "type": "GenericTextInput",
            "text": "Team Number",
            "placeholder": [
                "4099"
            ],
            "id": "teamnumber"
        },
        {
            "type": "GenericHeaderTwo",
            "text": "Auto"
        },
        {
            "type": "GenericToggle",
            "text": "Preloaded Cargo?",
            "id": "preloadedcargo"
        },
        {   
            "type": "GenericToggle",
            "text": "Line Crossed?",
            "id": "linecrossed"
        },
        {
            "type": "IncrementNumberInput",
            "text": "Switch Blocks",
            "id": "switchauto",
            "placeholder": ["0"]
        },
        {
            "type": "IncrementNumberInput",
            "text": "Scale Blocks",
            "id": "scaleauto",
            "placeholder": ["0"]
        },
        {
            "type": "GenericTextArea",
            "text": "Auto Notes",
            "placeholder": ["Notes"],
            "id": "autonotes"

        },
        {
            "type": "GenericHeaderTwo",
            "text": "Tele Ops"
        },
        {
            "type": "IncrementNumberInput",
            "text": "Switch Blocks",
            "id": "switchteleop",
            "placeholder": ["0"]
        },
        {
            "type": "IncrementNumberInput",
            "text": "Opposing Alliance Switch Blocks",
            "id": "oppswitch",
            "placeholder": ["0"]
        },
        {
            "type": "IncrementNumberInput",
            "text": "Exchange Port",
            "id": "exchangeportteleop",
            "placeholder": ["0"]
        },
        {
            "type": "GenericHeaderTwo",
            "text": "Endgame"
        },
        {
            "type": "GenericRadioSelect",
            "text": "Attemped Climb",
            "id": "attempedClimb",
            "options": ["none", "park","carried", "climb"]
        },
        {
            "type": "GenericRadioSelect",
            "text": "Final Climb",
            "id": "finalClimb",
            "options": ["none", "park", "levitate", "carried", "climb"]
        },
        {
            "type": "GenericToggle",
            "text": "Carried another Robot?",
            "id": "carryanotherrobot"
        },
        {
            "type": "GenericTextArea",
            "text": "Endgame Notes",
            "placeholder": ["Notes"],
            "id": "endgamenotes"
        },
        {
            "type": "GenericHeaderTwo",
            "text": "Misc.",
            "id": "mischeader"
        },
        {
            "type": "SliderInput",
            "text": "Driver Rating",
            "options": [
                "0",
                "5"
            ],
            "id": "driverrating"
        },
        {
            "type": "SliderInput",
            "text": "Defense Time",
            "options": [
                "0",
                "5"
            ],
            "id": "defensetime"
        },
        {
            "type": "SliderInput",
            "text": "Defense Rating",
            "options": [
                "0",
                "5"
            ],
            "id": "defenserating"
        },
        {
            "type": "SliderInput",
            "text": "Counter Defense Time",
            "options": [
                "0",
                "5"
            ],
            "id": "counterdefensetime"
        },
        {
            "type": "SliderInput",
            "text": "Counter Defense Rating",
            "options": [
                "0",
                "5"
            ],
            "id": "counterdefenserating"
        },
        {
            "type": "DarkButton",
            "text": "Submit",
            "id": "result"
        }
    ],
    "export": {
        "order": ["scoutid", "alliance"],
        "delimiter": ";"
    }
}
```

### All Components
Every components setup with all possible values
```
{
    "name": "All Components",
    "description": "Every component for view and testing",
    "components": [
        {
            "type": "GenericHeaderOne",
            "text": "All Component Test"
        },
        {
            "type": "Spacing"
        },
        {
            "type": "GenericHeaderTwo",
            "text": "Headers"
        },
        {
            "type": "GenericHeaderOne",
            "text": "GenericHeaderOne"
        },
        {
            "type": "GenericHeaderTwo",
            "text": "GenericHeaderTwo"
        },
        {
            "type": "Spacing"
        },
        {
            "type": "GenericHeaderTwo",
            "text": "Selects"
        },
        {
            "type": "GenericCheckboxSelect",
            "text": "GenericCheckBoxSelect",
            "options": [
                "Option 1",
                "Option 2",
                "Option 3",
                "Option 4",
                "Option 5"
            ],
            "id": "GenericCheckboxSelect"
        },
        {
            "type": "GenericDropdown",
            "text": "GenericDropdown",
            "options": [
                "Option 1",
                "Option 2",
                "Option 3",
                "Option 4",
                "Option 5"
            ],
            "id": "GenericDropdown"
        },
        {
            "type": "GenericRadioSelect",
            "text": "GenericRadioSelect",
            "options": [
                "Option 1",
                "Option 2",
                "Option 3",
                "Option 4",
                "Option 5"
            ],
            "id": "GenericRadioSelect"
        },
        {
            "type": "GenericToggle",
            "text": "GenericToggle",
            "id": "GenericToggle"
        },
        {
            "type": "Spacing"
        },
        {
            "type": "GenericHeaderTwo",
            "text": "Inputs"
        },
        {
            "type": "DropdownTextInput",
            "text": "DropdownTextInput",
            "options": [
                "Option 1",
                "Option 2",
                "Option 3",
                "Option 4",
                "Option 5"
            ],
            "placeholder": ["type"],
            "id": "DropdownTextInput"
        },
        {
            "type": "GenericTextInput",
            "text": "GenericTextInput",
            "placeholder": ["Wowerz"],
            "id": "GenericTextInput"
        },
        {
            "type": "GenericTextArea",
            "text": "GenericTextArea",
            "placeholder": ["Wowerz"],
            "id": "GenericTextArea"
        },
        {
            "type": "IncrementNumberInput",
            "text": "IncrementNumberInput",
            "placeholder": ["0"],
            "id": "IncrementNumberInput"
        },
        {
            "type": "SliderInput",
            "text": "SliderInput",
            "options": [
                "0", 
                "20"
            ],
            "id": "SliderInput"
        },
        {
            "type": "Spacing"
        },
        {
            "type": "GenericHeaderTwo",
            "text": "Buttons"
        },
        {
            "type": "DarkButton",
            "text": "Normal DarkButton",
            "id": "DarkButton"
        },
        {
            "type": "DarkButton",
            "text": "Submit DarkButton",
            "id": "result"
        }
    ],
    "export": {
        "order": [
            "GenericCheckboxSelect", 
            "GenericDropdown", 
            "GenericRadioSelect",
            "GenericToggle",
            "DropdownTextInput",
            "GenericTextInput",
            "GenericTextArea",
            "IncrementNumberInput",
            "SliderInput"
        ],
        "delimiter": "  "

    }
}
```