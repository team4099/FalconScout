import json
import os
import uuid
from csv import reader
from datetime import datetime

import yaml
from data_validation.data_val_2023 import DataValidation2023
from flask import Flask, jsonify, render_template, request
from github import Github
from pandas import DataFrame

g = Github(os.getenv("GITHUB_KEY"))

with open("config.json", "r") as json_file:
    config = json.load(json_file)

DATA_JSON_FILE = config["data_config"]["json_file"]
DATA_CSV_FILE = config["data_config"]["csv_file"]
ERROR_JSON = config["data_config"]["error_json"]

validation_by_year = {2023: DataValidation2023}
path_to_config = "data_validation/config.yaml"

with open(path_to_config) as file:
    data_validator = validation_by_year[yaml.safe_load(file)["year"]](path_to_config)

app = Flask(__name__)

def remove_escape_characters(string_to_change: str) -> str:
    escape_characters = "".join(chr(char) for char in range(1, 32))
    translator = string_to_change.maketrans("", "", escape_characters)
    return string_to_change.translate(translator)

@app.route("/")
def home():
    with open(DATA_JSON_FILE, "r") as file:
        file_data = json.load(file)

    scanRawData = []

    for row in file_data:
        scanRawData.append(row["scanRaw"])

    with open(ERROR_JSON, "r") as file:
        errorData = json.load(file)

    return render_template(
        "home.html",
        title="FalconScoutCore",
        scanRawData=scanRawData,
        tableData=file_data[::-1],
        tableHeaderData=config["data_config"]["data_labels"],
        errorData=errorData[:20],
    )


@app.route("/process_scan", methods=["POST"])
def process_scan():
    if request.method == "POST":
        # Retrieve file data to check for
        with open(DATA_JSON_FILE, "r") as file:
            file_data = json.load(file)

        try:
            scan_info = request.get_json()
            split_scan = scan_info["scan_text"].split(
                config["data_config"]["delimiter"]
            )
            for i in range(len(split_scan)):
                try:
                    try:
                        split_scan[i] = int(split_scan[i])
                    except ValueError:
                        split_scan[i] = float(split_scan[i])
                except Exception as e:
                    print(e)

            if len(split_scan) != len(config["data_config"]["data_labels"]):
                # 110: Data points in scan are too short and do not fit data label list size
                return jsonify(
                    {"action_code": "200", "result": ["110", "scan too short"]}
                )

            data_map = dict(zip(config["data_config"]["data_labels"], split_scan))
            data_map["scanRaw"] = scan_info["scan_text"]
            data_map["uuid"] = str(uuid.uuid4())
            # Commas in values will cause the CSV to error out
            data_map["AutoGrid"] = data_map["AutoGrid"].replace(",", "|")
            data_map["TeleopGrid"] = data_map["TeleopGrid"].replace(",", "|")

            if data_map in file_data:
                # Check for if the qrcode was already scanned
                return jsonify(
                    {
                        "action_code": "200",
                        "result": ["This QRcode has already scanned before."],
                    }
                )

            cone_positions = {1, 3, 4, 6, 7, 9}
            positions_to_names = {"L": "Low", "M": "Mid", "H": "High"}

            auto_grid = data_map["AutoGrid"].split("|")
            teleop_grid = data_map["TeleopGrid"].split("|")

            auto_cones = []
            auto_cubes = []

            for game_piece in auto_grid:
                if not game_piece:
                    continue

                position = game_piece[1]

                if "cone" in game_piece:
                    auto_cones.append(positions_to_names[position])
                elif "cube" in game_piece:
                    auto_cubes.append(positions_to_names[position])
                elif int(game_piece[0]) in cone_positions:
                    auto_cones.append(positions_to_names[position])
                else:
                    auto_cubes.append(positions_to_names[position])

            data_map["AutoCones"] = auto_cones
            data_map["AutoCubes"] = auto_cubes

            teleop_cones = []
            teleop_cubes = []

            for game_piece in teleop_grid:
                if not game_piece:
                    continue

                position = game_piece[1]

                if "cone" in game_piece:
                    teleop_cones.append(positions_to_names[position])
                elif "cube" in game_piece:
                    teleop_cubes.append(positions_to_names[position])
                elif int(game_piece[0]) in cone_positions:
                    teleop_cones.append(positions_to_names[position])
                else:
                    teleop_cubes.append(positions_to_names[position])

            data_map["TeleopCones"] = teleop_cones
            data_map["TeleopCubes"] = teleop_cubes

            if data_map["Alliance"].lower() == "red":
                if auto_grid != [""]:
                    auto_grid_reversed = [
                        f"{9 - int(position[0]) + 1}{position[1:]}"
                        for position in auto_grid
                    ]
                else:
                    auto_grid_reversed = []

                if teleop_grid != [""]:
                    teleop_grid_reversed = [
                        f"{9 - int(position[0]) + 1}{position[1:]}"
                        for position in teleop_grid
                    ]
                else:
                    teleop_grid_reversed = []

                data_map["AutoGrid"] = "|".join(auto_grid_reversed)
                data_map["TeleopGrid"] = "|".join(teleop_grid_reversed)

            # Remove escape characters + commas
            data_map["MatchKey"] = data_map["MatchKey"].replace(",", "")
            data_map = {
                key: remove_escape_characters(value).replace(",", "|") if isinstance(value, str) else value
                for key, value in data_map.items()
            }

            with open(DATA_JSON_FILE, "r+") as file:
                file_data = json.load(file)
                file_data.append(data_map)

                file.seek(0)
                json.dump(file_data, file, indent=2)

            data_df = DataFrame.from_dict(file_data)
            data_df.drop(
                columns=["AutoCones", "AutoCubes", "TeleopCones", "TeleopCubes"]
            )
            data_df = data_df[config["data_config"]["data_labels"]]

            data_df["AutoNotes"] = (
                data_df["AutoNotes"]
                .astype(str)
                .apply(lambda note: note.replace(",", ""))
            )
            data_df["TeleopNotes"] = (
                data_df["TeleopNotes"]
                .astype(str)
                .apply(lambda note: note.replace(",", ""))
            )
            data_df["EndgameNotes"] = (
                data_df["EndgameNotes"]
                .astype(str)
                .apply(lambda note: note.replace(",", ""))
            )
            data_df["RatingNotes"] = (
                data_df["RatingNotes"]
                .astype(str)
                .apply(lambda note: note.replace(",", ""))
            )

            data_df.to_csv(DATA_CSV_FILE)

            return jsonify(
                {
                    "action_code": "200",
                    "result": ["100", "scan read well"],
                    "scanInfo": data_map,
                }
            )

        except FileExistsError as e:
            print(e)
            return jsonify(
                {
                    "action_code": "200",
                    "result": ["120", "python error: " + str(e)[:20]],
                }
            )


@app.route("/sync_github", methods=["POST"])
def sync_github():
    if request.method == "POST":
        try:
            with open(DATA_JSON_FILE, "r+") as file:
                file_json_data = json.load(file)

            file_csv_data = ""
            with open(DATA_CSV_FILE) as file:
                print("reading")
                csv_reader = reader(file)
                for line in csv_reader:
                    file_csv_data += ",".join(line) + "\n"

            repo = g.get_repo(config["repo_config"]["repo"])
            contents = repo.get_contents(config["repo_config"]["update_json"])
            repo.update_file(
                contents.path,
                f'updated data @ {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}',
                str(file_json_data).replace("'", '"'),
                contents.sha,
            )

            contents = repo.get_contents(config["repo_config"]["update_csv"])
            repo.update_file(
                contents.path,
                f'updated data @ {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}',
                str(file_csv_data),
                contents.sha,
            )

            return jsonify(
                {
                    "action_code": "200",
                    "result": ["100", "Github push was valid"],
                }
            )
        except TypeError as e:
            print(e, "test")
            return jsonify(
                {
                    "action_code": "200",
                    "result": ["110", "python error: " + str(e)[:20]],
                }
            )


@app.route("/validate_data", methods=["POST"])
def validate_data():
    with open(DATA_JSON_FILE) as file:
        file_data = json.load(file)
        data_validator.validate_data(file_data)

    with open(ERROR_JSON) as error_file:
        amount_of_errors = len(json.load(error_file))

    if amount_of_errors == 0:
        return jsonify(
            {
                "action_code": "200",
                "result": ["100", "All passes checked when ran with DataVal!"],
            }
        )
    else:
        return jsonify(
            {
                "action_code": "200",
                "result": [
                    "110",
                    f"{amount_of_errors} errors raised when ran with DataVal.",
                ],
            }
        )


@app.route("/get_errors", methods=["POST"])
def get_errors():
    if request.method == "POST":
        try:
            with open(ERROR_JSON, "r") as file:
                file_data = json.load(file)
            return jsonify(
                {
                    "action_code": "200",
                    "result": ["100", "Sent errors success"],
                    "errors": file_data[:20],
                }
            )
        except Exception as e:
            print(e, "test")
            return jsonify(
                {
                    "action_code": "200",
                    "result": ["110", "python error: " + str(e)[:20]],
                }
            )


@app.route("/delete_data", methods=["POST"])
def delete_data():
    data_to_remove = request.get_json()

    with open(DATA_JSON_FILE, "r+") as file:
        file_data = json.load(file)
        file_data.remove(data_to_remove)

        file.seek(0)
        json.dump(file_data, file, indent=2)
        file.truncate()

    return jsonify(
        {
            "action_code": "200",
            "result": [
                "100",
                f"Data of scout {data_to_remove['ScoutId']} in {data_to_remove['MatchKey']} removed",
            ],
        }
    )


@app.route("/delete_error", methods=["POST"])
def delete_error():
    error_to_remove = request.get_json()

    with open(ERROR_JSON, "r+") as file:
        file_data = json.load(file)
        file_data.remove(error_to_remove)

        file.seek(0)
        json.dump(file_data, file, indent=2)
        file.truncate()

    return jsonify(
        {
            "action_code": "200",
            "result": [
                "100",
                f"An error raised in {error_to_remove['match']} was successfully removed.",
            ],
        }
    )


@app.route("/change_submission", methods=["POST"])
def change_submission():
    headers = config["data_config"]["data_labels"]
    changed_submission = request.get_json()

    submission_row = changed_submission["submissionRow"]
    submission_col = changed_submission["submissionCol"]
    header_changed = headers[submission_col]
    new_value = changed_submission["changedValue"]

    with open(DATA_JSON_FILE, "r+") as file:
        file_data = json.load(file)

        old_value = file_data[~submission_row][header_changed]
        file_data[~submission_row][header_changed] = new_value

        file.seek(0)
        json.dump(file_data, file, indent=2)
        file.truncate()

    return jsonify(
        {
            "action_code": "200",
            "result": [
                "100",
                f"Data in column {header_changed!r} changed from {old_value!r} to {new_value!r}",
            ],
        }
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4099)
