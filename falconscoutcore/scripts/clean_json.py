from json import load, dump

with open("../data/2023chcmp_match_data.json") as file:
    scouting_data = load(file)
    new_scouting_data = []

    for submission in scouting_data:
        submission['AutoNotes'] = submission['AutoNotes'].replace('"', "'")
        submission['TeleopNotes'] = submission['TeleopNotes'].replace('"', "'")
        submission['EndgameNotes'] = submission['EndgameNotes'].replace('"', "'")
        submission['RatingNotes'] = submission['RatingNotes'].replace('"', "'")
        new_scouting_data.append(submission)

with open("../data/2023chcmp_match_data.json", "w") as new_file:
    dump(scouting_data, new_file, indent=2)
