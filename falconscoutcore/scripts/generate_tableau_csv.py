from json import load

import pandas as pd

headers = [
    "H1",
    "H2",
    "H3",
    "H4",
    "H5",
    "H6",
    "H7",
    "H8",
    "H9",
    "M1",
    "M2",
    "M3",
    "M4",
    "M5",
    "M6",
    "M7",
    "M8",
    "M9",
    "LCube1",
    "LCube2",
    "LCube3",
    "LCube4",
    "LCube5",
    "LCube6",
    "LCube7",
    "LCube8",
    "LCube9",
    "LCone1",
    "LCone2",
    "LCone3",
    "LCone4",
    "LCone5",
    "LCone6",
    "LCone7",
    "LCone8",
    "LCone9",
]

new_headers = [
    "Scout Name",
    "Match Key",
    "Alliance",
    "Driver Station",
    "Team Number",
    "Preloaded",
    "Auto H1",
    "Auto H2",
    "Auto H3",
    "Auto H4",
    "Auto H5",
    "Auto H6",
    "Auto H7",
    "Auto H8",
    "Auto H9",
    "Auto M1",
    "Auto M2",
    "Auto M3",
    "Auto M4",
    "Auto M5",
    "Auto M6",
    "Auto M7",
    "Auto M8",
    "Auto M9",
    "Auto LCube1",
    "Auto LCube2",
    "Auto LCube3",
    "Auto LCube4",
    "Auto LCube5",
    "Auto LCube6",
    "Auto LCube7",
    "Auto LCube8",
    "Auto LCube9",
    "Auto LCone1",
    "Auto LCone2",
    "Auto LCone3",
    "Auto LCone4",
    "Auto LCone5",
    "Auto LCone6",
    "Auto LCone7",
    "Auto LCone8",
    "Auto LCone9",
    "Auto Misses",
    "Mobile",
    "Auto Attempted",
    "Auto Final Charge",
    "Auto Notes",
    "Teleop H1",
    "Teleop H2",
    "Teleop H3",
    "Teleop H4",
    "Teleop H5",
    "Teleop H6",
    "Teleop H7",
    "Teleop H8",
    "Teleop H9",
    "Teleop M1",
    "Teleop M2",
    "Teleop M3",
    "Teleop M4",
    "Teleop M5",
    "Teleop M6",
    "Teleop M7",
    "Teleop M8",
    "Teleop M9",
    "Teleop LCube1",
    "Teleop LCube2",
    "Teleop LCube3",
    "Teleop LCube4",
    "Teleop LCube5",
    "Teleop LCube6",
    "Teleop LCube7",
    "Teleop LCube8",
    "Teleop LCube9",
    "Teleop LCone1",
    "Teleop LCone2",
    "Teleop LCone3",
    "Teleop LCone4",
    "Teleop LCone5",
    "Teleop LCone6",
    "Teleop LCone7",
    "Teleop LCone8",
    "Teleop LCone9",
    "Teleop Misses",
    "Teleop Notes",
    "Endgame Attempted",
    "Endgame Final Charge",
    "Final Charge Time",
    "Endgame Notes",
    "Disable",
    "Tippy",
    "Defense Time",
    "Defense Rating",
    "Driver Rating",
    "Rating Notes",
    "Attempted Triple Balance",
    "Successful Triple Balance",
    "Supercharged Nodes"
]

with open("../data/2023chcmp_match_data.json") as file:
    scouting_data = load(file)

    for submission in scouting_data:
        submission["Preloaded"] = int(submission["Preloaded"] == "true")
        submission["Mobile"] = int(submission["Mobile"] == 1.0)
        submission["Disable"] = int(submission["Disable"] == 1.0)
        submission["Tippy"] = int(submission["Tippy"] == 1.0)
        submission["AutoAttemptedCHarge"] = submission["AutoAttemptedCharge"] == "Engage"
        submission["EndgameAttemptedCHarge"] = submission["EndgameAttemptedCharge"] == "Engage"
        # submission["AttemptedTripleBalance"] = int(submission["AttemptedTripleBalance"])
        # submission["SuccessfulTripleBalance"] = int(
        #     submission["SuccessfulTripleBalance"]
        # )

        auto_grid = submission["AutoGrid"].split("|")

        for header in headers:
            if header[::-1] in auto_grid:
                submission[f"Auto {header}"] = 1
            elif (
                    header.replace("Cone", "").replace("Cube", "")[::-1]
                    + header[1:5].lower()
                    in auto_grid
            ):
                submission[f"Auto {header}"] = 1
            else:
                submission[f"Auto {header}"] = 0

        teleop_grid = submission["TeleopGrid"].split("|")

        for header in headers:
            if header[::-1] in teleop_grid:
                submission[f"Teleop {header}"] = 1
            elif (
                    header.replace("Cone", "").replace("Cube", "")[::-1]
                    + header[1:5].lower()
                    in teleop_grid
            ):
                submission[f"Teleop {header}"] = 1
            else:
                submission[f"Teleop {header}"] = 0

        submission["SuperchargedNodes"] = len(teleop_grid) - len(set(teleop_grid))

        submission.pop("AutoGrid")
        submission.pop("TeleopGrid")

    submission_df = pd.DataFrame.from_dict(scouting_data)

    submission_df = submission_df[
        [
            "ScoutId",
            "MatchKey",
            "Alliance",
            "DriverStation",
            "TeamNumber",
            "Preloaded",
            "Auto H1",
            "Auto H2",
            "Auto H3",
            "Auto H4",
            "Auto H5",
            "Auto H6",
            "Auto H7",
            "Auto H8",
            "Auto H9",
            "Auto M1",
            "Auto M2",
            "Auto M3",
            "Auto M4",
            "Auto M5",
            "Auto M6",
            "Auto M7",
            "Auto M8",
            "Auto M9",
            "Auto LCube1",
            "Auto LCube2",
            "Auto LCube3",
            "Auto LCube4",
            "Auto LCube5",
            "Auto LCube6",
            "Auto LCube7",
            "Auto LCube8",
            "Auto LCube9",
            "Auto LCone1",
            "Auto LCone2",
            "Auto LCone3",
            "Auto LCone4",
            "Auto LCone5",
            "Auto LCone6",
            "Auto LCone7",
            "Auto LCone8",
            "Auto LCone9",
            "AutoMissed",
            "Mobile",
            "AutoAttemptedCharge",
            "AutoChargingState",
            "AutoNotes",
            "Teleop H1",
            "Teleop H2",
            "Teleop H3",
            "Teleop H4",
            "Teleop H5",
            "Teleop H6",
            "Teleop H7",
            "Teleop H8",
            "Teleop H9",
            "Teleop M1",
            "Teleop M2",
            "Teleop M3",
            "Teleop M4",
            "Teleop M5",
            "Teleop M6",
            "Teleop M7",
            "Teleop M8",
            "Teleop M9",
            "Teleop LCube1",
            "Teleop LCube2",
            "Teleop LCube3",
            "Teleop LCube4",
            "Teleop LCube5",
            "Teleop LCube6",
            "Teleop LCube7",
            "Teleop LCube8",
            "Teleop LCube9",
            "Teleop LCone1",
            "Teleop LCone2",
            "Teleop LCone3",
            "Teleop LCone4",
            "Teleop LCone5",
            "Teleop LCone6",
            "Teleop LCone7",
            "Teleop LCone8",
            "Teleop LCone9",
            "TeleopMissed",
            "TeleopNotes",
            "EndgameAttemptedCharge",
            "EndgameFinalCharge",
            "EndgameChargeTime",
            "EndgameNotes",
            "Disable",
            "Tippy",
            "DefenseTime",
            "DefenseRating",
            "DriverRating",
            "RatingNotes",
            "AttemptedTripleBalance",
            "SuccessfulTripleBalance",
            "SuperchargedNodes"
        ]
    ]

    submission_df.columns = new_headers
    submission_df.to_csv("../data/tableau_data.csv")
