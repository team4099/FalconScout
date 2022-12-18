from flask import (
    Flask, 
    render_template,
    jsonify,
    request
)
import json
import requests

with open("config.json", "r") as json_file:
    config = json.load(json_file)

DATA_FILE = config["data"]

app = Flask(__name__)

@app.route("/")
def home():
    return render_template(
        "home.html",
        title="FalconScoutCore"
    )

@app.route("/process_scan", methods=["POST"])
def process_scan():
    if request.method == "POST":
        scan_info = request.get_json()
        print(scan_info["scan_text"])

        return jsonify({"action_code": "200"})

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0")