import os
import uuid
from json import dump, load

import cv2

with open("../data/2023new_match_data.json") as file:
    scouting_data = load(file)

with open("../config.json") as config_file:
    config = load(config_file)

os.chdir("../data/2023new_qr_codes")

detector = cv2.QRCodeDetector()


def remove_escape_characters(string_to_change: str) -> str:
    escape_characters = "".join(chr(char) for char in range(1, 32))
    translator = string_to_change.maketrans("", "", escape_characters)
    return string_to_change.translate(translator)


for idx, file in enumerate(whole_dir := os.listdir()):
    if os.path.isfile(file):
        if file.endswith("HEIC"):
            continue

        img = cv2.imread(file)
        val, *_ = detector.detectAndDecode(img)

        if not val:
            continue

        # Interpret values
        split_scan = val.split(
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
            raise ValueError("Data points wrong")

        # TODO: Use config names instead of raw names (eg self.config["auto_grid"] rather than AutoGrid)
        data_map = dict(zip(config["data_config"]["data_labels"], split_scan))
        data_map["scanRaw"] = val
        data_map["uuid"] = str(uuid.uuid4())
        # Commas in values will cause the CSV to error out
        data_map["AutoGrid"] = data_map["AutoGrid"].replace(",", "|")
        data_map["TeleopGrid"] = data_map["TeleopGrid"].replace(",", "|")
        # Change true/false to signify whether they tried to engage or not
        data_map["AutoAttemptedCharge"] = "Engage" if data_map["AutoAttemptedCharge"] else "None"
        data_map["EndgameAttemptedCharge"] = "Engage" if data_map["EndgameAttemptedCharge"] else "None"

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
            key: remove_escape_characters(value).replace(",", "|")
            if isinstance(value, str)
            else value
            for key, value in data_map.items()
        }

        scouting_data.append(data_map)

        print(f"{idx}/{len(whole_dir)} finished")

with open("../2023new_match_data.json", "w") as file:
    dump(scouting_data, file, indent=2)

