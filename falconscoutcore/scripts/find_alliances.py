from json import dump, load

with open("../data/match_schedule.json") as match_schedule_file:
    match_schedule = load(match_schedule_file)

with open("../data/2023new_match_data.json", "r") as file:
    scouting_data = load(file)
    new_scouting_data = []

    for submission in scouting_data:
        team_key = f"frc{submission['TeamNumber']}"

        match_key = f"2023chcmp_{submission['MatchKey']}"
        red, blue = match_schedule[match_key]["red"], match_schedule[match_key]["blue"]

        if team_key in red:
            submission["Alliance"] = "red"
        else:
            submission["Alliance"] = "blue"

        new_scouting_data.append(submission)

with open("../data/2023new_match_data.json", "w") as file:
    dump(new_scouting_data, file, indent=2)
