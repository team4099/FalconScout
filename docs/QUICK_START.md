# FalconScout (Kinda) Quick Start

## Download FalconScout

Go to your preferred folder and clone the repository.

```
git clone https://github.com/team4099/FalconScout.git
```

## Setting up FalconScoutCore

### Running the app

Enter the repository and the FalconScoutCore folder

```
cd FalconScout/falconscoutcore
```

Set up a virtual environment by typing the following commands. *Note:* that the following applies if you have Python 3.10 installed. If you don't visit the [Python Downloads Page](https://www.python.org/downloads/) and download Python 3.10. If you would like to use another version of Python, run the same command with the version replaced.

**Macos**

```
python3.10 -m venv venv
source venv/bin/activate
```

**Windows**
```
python -m venv venv
.\venv\Scripts\activate
```

Now, install the dependencies.
```
pip install -r requirements.txt
```

Now, setup your `.env` file. So in the falconscoutcore folder, rename the file called `.env.example` to `.env`.

Inside the file add the token from [here](https://github.com/settings/tokens) to the spot where it says `<YOUR_KEY_HERE>`
```
GITHUB_KEY=<YOUR_KEY_HERE>
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
        "delimiter": ",",
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
 - `delimiter` dictates how core will split qr code data from the scouting app. This value should stay the same between both forms (e.g. `, ; |`). Since
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

By doing this, you have setup your core app and can run this to record data. You can take a look at the [data val explanation](./CONFIGURING_DATAVALIDATION.md) page to look at exactly how data validation works.

## Running Scouting App

Enter the repository and the ScoutingApp folder

```
cd FalconScout/scoutingapp
```

Install the necessary packages via npm using our `packages.json` file
```
npm install
```

Run the app to verify you have everything setup
```
npm run dev
```

Build the app to deploy to [netlify](https://app.netlify.com/drop). Running this command will generate a `dist` folder.
```
npm run build
```

### Setting up config files
The config file setup for FalconScout is just one file and you'll love it.

Assuming you are already in the scoutingapp folder, open the file at the following location
```
src/config/structure.json
```

`structure.json` is a list of pages which your scouting app will contain. The file will contain a predefined structure with every component available. You can view the possible components [here](https://sunny-kitten-b34948.netlify.app/#/AllComponents). Structure of a file follows like this

```
[
    {
        {
        "name": "Match Scouting",
        "description": "Gather data on robots during matches. Data used for quantitative metrics in alliance selection.",
        "components": [
            {
                "type": "GenericHeaderOne",
                "text": "Match Scouting",
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
                "text": "Team Number",
                "placeholder": [
                    "4099"
                ],
                "id": "teamnumber"
            },
            {
                "type": "DarkButton",
                "text": "Submit",
                "id": "result"
            }
        ],
        "export": {
            "delimiter": ";"
            "order": ["scoutid", "teamnumber"]
        }
    }
]
```

For each page you have 4 parts. `name`, `description`, `components`, `export`.
 - `name` is the name of the page which shows up on the home page as well as the form and is used for the link
 - `description` is the description of the page which shows up on the home page
 - `export` is the way for you to generate a qrcode
    - `delimiter` is how you set the delimiter for separating the values in the qrcode.

    - `order` is a list of ids from components in order to write the order of data in the qr code. This order should be the same as the one in the core `config.json`

 - `component` is a list of components with a set structure shown below.
    - The `type` is one of 12 components that can be used in the scouting app. Type `String`
    - The `text` is the title which appears on top of the component and should be used as the description of your component to the scout. Type `String`
    - The `placeholder` is a list which should contain placeholders for things like text boxes or anything that should contain predefined or example values. It will be indicated in the component description if its needed. Type `Array<String>`
    - The `options` is a list of options needed for elements which may have dropdowns or checkboxes. Type `Array<String>`
    - The `id` is a string which is used in the system for storing the value of the element and using it in the export and qrcode generation

    - Here is the info on each one with the type listed. **To see each component, please go [here](https://sunny-kitten-b34948.netlify.app/#/AllComponents)**
        - `DarkButton` is the button generally used for submitting. **When used for submitting, the id must be set to `result`**. No placeholders or options

        - `DropdownTextInput` is used for selection an option and providing a text input inline. This could be used for selecting your match type by setting your options as qm, qf, sf, f and your placeholder as match number. Can take placeholders (1) and options (many)
        - `GenericTextArea` is used for getting inputs in a paragraph form. Similar to text area in google forms. Can take a placeholder (only 1) but no options
        - `GenericTextInput` is used for getting inputs in a single line form. Similar to text input in google forms. Can take a placeholder (only 1) but no options
        - `IncrementNumberInput` is used to get a number and add or subtract to it. It can be used in Rapid React for getting the ball count. It can take a placeholder for the initial value but no options.
        - `SliderInput` is used to get a value on a regular html slider from values a to b. The values are set via two options. Options are used and not placeholders
        - `GenericCheckboxSelect` is used for getting multiple values selected. Checkbox like google forms. Can be used for zones in 2022. Takes options in a list and no placeholders
        - `GenericDropdownSelect` is a dropdown which can be used to select one of many options in a list. Options can be given in a list and no placeholders taken.
        - `GenericRadioSelect` are for selecting an option in a list like the dropdown select but in the ui format of a radio which takes a single value. Takes a list of options and no placeholders
        - `GenericToggle` is a phone setting-like toggle used for getting a `True` or `False` value from the user. Takes no placeholders or options.
        - `GenericHeaderOne` is a big text header for displaying text for the user. Takes no placeholder or options
        - `GenericHeaderTwo` is a small text header for displaying text for the user. Takes no placeholder or options
```
{
    "type": "DarkButton",
    "text": "Submit",
    "placeholder: [
        "team4099",
        "team6328"
    ],
    "options: [
        "4414",
        "254",
        "6328",
        "4099"
    ],
    id: "submit"
}
```

By doing this, your scouting app should be setup. You can take a look at the [example forms](./EXAMPLE_FORMS.md) page to look at forms we have made for you to help your setup.
