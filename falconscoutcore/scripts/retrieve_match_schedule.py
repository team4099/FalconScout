from json import dump

import falcon_alliance

with (
    falcon_alliance.ApiClient(
        api_key="6lcmneN5bBDYpC47FolBxp2RZa4AbQCVpmKMSKw9x9btKt7da5yMzVamJYk0XDBm"
    ) as api_client,
    open("../data/match_schedule.json", "w") as file,
):
    match_schedule_formatted = {}
    event_matches: list[falcon_alliance.Match] = falcon_alliance.Event(
        "2024mdowi"
    ).matches()

    for match in event_matches:
        match_schedule_formatted[match.key] = {
            "red": match.alliances["red"].team_keys,
            "blue": match.alliances["blue"].team_keys,
        }

    dump(match_schedule_formatted, file, indent=2)
