from json import load, dump

new_scouting_data = []

with open("../data/2023_scouting_data.json", "r+") as scouting_file:
    scouting_data = load(scouting_file)

    for submission in scouting_data:
        scout_id = str(submission["ScoutId"])

        if "and" in scout_id:
            names = [name.strip().lower() for name in scout_id.split("and")]

            for name in names:
                new_scouting_data.append(submission | {"ScoutId": name})
        else:
            new_scouting_data.append(submission | {"ScoutId": scout_id.split()[0].lower() if scout_id.split() else scout_id.lower()})

    scouting_file.seek(0)
    dump(new_scouting_data, scouting_file, indent=2)
