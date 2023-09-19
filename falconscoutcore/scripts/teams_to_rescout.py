from json import load, dump

RESCOUTING_THRESHOLD = 5 # Number of matches needed for each team
teams = [1023, 11, 1123, 1156, 1466, 1468, 1501, 1538, 1629, 1746, 1757, 177, 179, 1816, 1836, 195, 2642, 2960, 2992, 3003, 3039, 3161, 3184, 3218, 3478, 3538, 3572, 3767, 3932, 3940, 4069, 4099, 4112, 4143, 4145, 4329, 4419, 4522, 4663, 4905, 4909, 494, 4944, 5006, 503, 5135, 5172, 5274, 5338, 5553, 5665, 5804, 5990, 6431, 6606, 6657, 6817, 6909, 7072, 7285, 7428, 7617, 8015, 8016, 857, 8592, 8717, 8808, 8847, 900, 9023, 9030, 9062, 9084, 9126, 9140, 955]
teams_to_rescout = []

with (
    open("../data/2023new_match_data.json") as file,
    open("../data/errors.json") as errors_file
):
    errors = load(errors_file)
    match_data = load(file)

    for team in teams:
        matches_scouted = [submission for submission in match_data if submission["TeamNumber"] == team]

        if len(matches_scouted) < RESCOUTING_THRESHOLD:
            errors_raised = sorted([
                error["match"] for error in errors if error["team_id"] == team and error["error_type"] == "MISSING DATA"
            ])
            teams_to_rescout.append(
                f"- {team} has {len(errors_raised)} missing matches ({', '.join(errors_raised)})"
            )

    print("\t\n".join(teams_to_rescout))