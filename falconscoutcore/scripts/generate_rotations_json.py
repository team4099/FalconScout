from json import dump

import pandas as pd

scouting_rotations = pd.read_csv("../data/2023new_scouting_rotations.csv")
rotation_json = {}

for _, row in scouting_rotations.iterrows():
    if row.empty:
        continue
    rotation_json[f"qm{row['Quals Match']}"] = {
        "red": [
            f"{row['red1 A']} and {row['red1 B']}",
            f"{row['red2 A']} and {row['red2 B']}",
            f"{row['red3 A']} and {row['red3 B']}",
        ],
        "blue": [
            f"{row['blue1 A']} and {row['blue1 B']}",
            f"{row['blue2 A']} and {row['blue2 B']}",
            f"{row['blue3 A']} and {row['blue3 B']}",
        ],
    }

with open("../data/2023new_scouting_rotations.json", "w") as file:
    dump(rotation_json, file, indent=2)
