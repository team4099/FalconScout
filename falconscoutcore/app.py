from flask import (
    Flask, 
    render_template,
    jsonify,
    request
)
import json
import os
from dotenv import load_dotenv
from github import Github
from datetime import datetime

g = Github(os.getenv("GITHUB_KEY"))

with open("config.json", "r") as json_file:
    config = json.load(json_file)

DATA_FILE = config["data"]

app = Flask(__name__)

@app.route("/")
def home():
    with open(DATA_FILE,'r+') as file:
        file_data = json.load(file)

    tableData = []
    scanRawData = []

    for row in file_data:
        print(row)
        scanRawData.append(row["scanRaw"])
        tableData.append(
            {
                "id": row[config["table_config"]["line_id"]],
                "scanRaw": row["scanRaw"]
            }
        )

    return render_template(
        "home.html",
        title="FalconScoutCore",
        scanRawData=scanRawData,
        tableData=tableData
    )

@app.route("/process_scan", methods=["POST"])
def process_scan():
    if request.method == "POST":
        try:
            scan_info = request.get_json()
            split_scan = scan_info["scan_text"].split(config["delimeter"])
            print(split_scan)
            if len(split_scan) != len(config["data_config"]["data_labels"]):
                # 110: Data points in scan are too short and do not fit data label list size
                return jsonify({
                    "action_code": "200",
                    "result": ["110", "scan too short"]
                })
            
            data_map = dict(zip(config["data_config"]["data_labels"], split_scan))
            data_map["scanRaw"] = scan_info["scan_text"]

            with open(DATA_FILE,'r+') as file:
                file_data = json.load(file)
                print(file_data)
                if (data_map[config["data_config"]["data_header"]] in file_data.keys()):
                    file_data[data_map[config["data_config"]["data_header"]]].append(data_map)
                else:
                    file_data[data_map[config["data_config"]["data_header"]]] = []
                    file_data[data_map[config["data_config"]["data_header"]]].append(data_map)
                file_data.append(data_map)
                file.seek(0)
                json.dump(file_data, file, indent = 4)

            return jsonify({
                "action_code": "200",
                "result": ["100", "scan read well"],
                "scanInfo": {
                    "id": data_map[config["table_config"]["line_id"]],
                    "scanRaw": scan_info
                }
            })

        except Exception as e:
            print(e)
            return jsonify({
                "action_code": "200",
                "result": ["120", "python error: " + str(e)[:20]],
            })

@app.route("/sync_github", methods=["POST"])
def sync_github():
    if request.method == "POST":
        with open(DATA_FILE,'r+') as file:
            file_data = json.load(file)

        repo = g.get_repo(config["repo"])
        contents = repo.get_contents(DATA_FILE)
        repo.update_file(contents.path, f'updated data @ {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}', str(file_data), contents.sha)
        return jsonify({
            "action_code": "200",
            "result": ["100", "push valid"],
        })
        

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0")