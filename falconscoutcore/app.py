import json
import os
import uuid
from csv import reader, writer
from datetime import datetime

import yaml
from data_validation.data_val_2022 import DataValidation2022
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from github import Github

g = Github(os.getenv("GITHUB_KEY"))

with open("config.json", "r") as json_file:
    config = json.load(json_file)

DATA_JSON_FILE = config["data_config"]["json_file"]
DATA_CSV_FILE = config["data_config"]["csv_file"]

validation_by_year = {2022: DataValidation2022}
path_to_config = "config.yaml"

with open(path_to_config) as file:
    data_validator = validation_by_year[yaml.safe_load(file)["year"]](path_to_config)

app = Flask(__name__)


@app.route("/")
def home():
    with open(DATA_JSON_FILE, "r") as file:
        file_data = json.load(file)

    data_validator.validate_data(file_data)

    tableData = []
    scanRawData = []

    for row in file_data:
        scanRawData.append(row["scanRaw"])

    with open("data/errors.json", "r") as file:
        errorData = json.load(file)

    print(errorData[-20:])

    return render_template(
        "home.html",
        title="FalconScoutCore",
        scanRawData=scanRawData,
        tableData=file_data[::-1],
        tableHeaderData=config["data_config"]["data_labels"],
        errorData=errorData[-20:],
    )


@app.route("/process_scan", methods=["POST"])
def process_scan():
    if request.method == "POST":
        try:
            scan_info = request.get_json()
            split_scan = scan_info["scan_text"].split(config["data_config"]["delimiter"])
            for i in range(len(split_scan)):
                try:
                    try:
                        split_scan[i] = int(split_scan[i])
                    except ValueError:
                        split_scan[i] = float(split_scan[i])
                except:
                    pass
            print(split_scan)
            if len(split_scan) != len(config["data_config"]["data_labels"]):
                # 110: Data points in scan are too short and do not fit data label list size
                return jsonify(
                    {"action_code": "200", "result": ["110", "scan too short"]}
                )

            data_map = dict(zip(config["data_config"]["data_labels"], split_scan))
            data_map["scanRaw"] = scan_info["scan_text"]
            data_map["uuid"] = str(uuid.uuid4())

            with open(DATA_JSON_FILE, "r+") as file:
                file_data = json.load(file)
                file_data.append(data_map)
                file.seek(0)
                json.dump(file_data, file, indent=4)

            with open(DATA_CSV_FILE, "a") as file:
                new_data_map = data_map
                new_data_map.pop("scanRaw")
                writer_file = writer(file)
                writer_file.writerow(new_data_map.values())
                file.close()

            data_validator.validate_data(scouting_data=[data_map])

            return jsonify(
                {
                    "action_code": "200",
                    "result": ["100", "scan read well"],
                    "scanInfo": data_map
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
                str(file_json_data),
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


@app.route("/get_errors", methods=["POST"])
def get_errors():
    if request.method == "POST":
        try:
            with open("data/errors.json", "r") as file:
                file_data = json.load(file)
            return jsonify(
                {
                    "action_code": "200",
                    "result": ["100", "Sent errors success"],
                    "errors": file_data[-20:],
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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4099)
