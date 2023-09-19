from json import dump

import pandas as pd

pit_scouting_data = pd.read_csv("data/2023new_pit_scouting_data.csv")

with open("data/2023new_pit_scouting_data.json", "w") as file:
    dump(pit_scouting_data.to_dict("records"), file, indent=2)
