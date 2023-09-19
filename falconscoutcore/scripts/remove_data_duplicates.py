import json

with open("../data/2023new_match_data.json", "r") as file:
    scouting_data = json.load(file)

no_duplicates_data = []

for submission in scouting_data:
    if submission not in no_duplicates_data:
        no_duplicates_data.append(submission)

with open("../data/2023new_match_data.json", "w") as file:
    json.dump(no_duplicates_data, file, indent=2)
