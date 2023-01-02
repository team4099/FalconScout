# FalconScout (Kinda) Quick Start

## Download FalconScout

Go to your preferred folder and clone the repository.

```
git clone https://github.com/team4099/FalconScout.git
```

## Setting up FalconScoutCore

### Running the app

Then enter the repository and the FalconScoutCore folder

```
cd FalconScout/falconscoutcore
```

Set up a virtual environment by typing the following commands. *Note:* that the following applies if you have Python 3.10 installed. If you don't visit the [Python Downloads Page](https://www.python.org/downloads/) and download Python 3.10. If you would like to use another version of Python, run the same command with the version replaced.
```
python3.10 -m venv venv
source venv/bin/activate
```

Now, install the dependencies.
```
pip install -r requirements.txt
```

Now, setup your `.env` file. So in the falconscoutcore folder, create a file called `.env`.

Inside the file add the following and get your token [here](https://github.com/settings/tokens).
```
GITHUB_KEY=YOUR KEY HERE
```

Simply run the app by doing
```
python app.py
```

You should be good to go! The output will tell you what it's running on (usually on `localhost:4099`)

### Setting up the Config Files

One of the goals in FalconScout is creating a system where a team can write no code to setup a scouting app. To do this, we implemented a system of json and yaml files in core. In this section you will walkthrough how to edit these files to configure your app.

**JSON setup**

You have two parts to the JSON (`data_config`, `repo_config`)

```
{
    "data_config": {
        "delimeter": ",",
        "data_labels": [
            "scout_id",
            "match_key",
            ...
            "teleop_notes",
            "misc_notes"
        ],
        "json_file": "./data/2022iri_match_data.json",
        "csv_file": "./data/2022iri_match_data.csv"
    },
    "repo_config": {
        "repo": "team4099/falcontrack",
        "update_csv": "data.csv",
        "update_json": "data.json"
    }
}
```

In `data_config`, you have 4 parameters.
 - `delimeter` dictates how core will split qr code data from the scouting app. This value should stay the same between both forms (e.g. `, ; |`). Since
 - `data_labels` are the order of keys in the qr code. So the list you provide in the json wll be the names in order of the values in a qr code. In this example, the first value read in a qr code will be the `scout_id` and the second to last is `teleop_notes `.
 - `json_file` is the location of the file which data will be written to in a json format
 - `csv_file` is the location of the file which data will be written to in a csv format. **We recommend you DO NOT use csv in your data collection since data can contain commas and mess up collumn collection**

In `repo config`, you have 3 parameters.
 - `repo` gives github what code repository will be written to. Your tokens must have access to wherever you are writing to. You can have a user repository of `Oboy-1/LunaSim` or an organization repository of `Team4099/FalconAlliance` and as long as you and your token have write permissions to the organization and the repository, it should work.
 - `update_csv` is the file path of the csv file on the repository that will be updated when github is synced
 - `update_json` is the file path of the json file on the repository that will be updated when github is synced

**YAML Setup**
The Yaml is used to setup our data validation system we provide to check your data using code we've written to identify possible errors like scouting the same robot twice, not scouting, high error data, missing data values, and more. We write a base validation class and a year specific one and plan to release a validation class for 2023.

```
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
...
taxied: "taxied"
final_climb_type: "final_climb_type"

# general game parameters
alliance: "alliance"
driver_station: "driver_station"
...
defense_rating: "defense_rating"
counter_defense_rating: "counter_defense_rating"
```

The first 3 parameters in the example `year`, `event_code`, `run_with_tba` are used to setup the year specific and general checks to be run. Setting `year` to 2023 will run the 2023 checks if they exist. Setting `event` to iri will cause TBA to grab the iri 2022 schedule and use it for data validation. This will only happen if you choose to use the `run_with_tba` parameter (use only if you have internet connection).

The rest of the parameters may change yearly but are used to translate the data you collect to the `4099 data val syntax` for that and past year checks. Internally, we use wording like `auto_lower_hub` but if you don't use that same wording, then you can just change your name for it in the yaml file by changing the key. Example ...
```
taxied: "taxi"
```

The values used in the value pair should be the same values in your `data_labels` in your `config.json`. 

If you do not collect that data, place the value as `not_col`.

By doing this, you have setup your core app and can run this to record data.

## Running Scouting App

