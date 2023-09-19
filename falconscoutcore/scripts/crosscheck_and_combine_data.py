import json

import pandas as pd

AUTO_PIECES_THRESHOLD = 1
TELEOP_PIECES_THRESHOLD = 1

newton_data = pd.read_csv("../data/8592data.csv")
scouting_data = pd.read_json("../data/2023new_match_data.json")
errors = {}
charge_station_to_newton = {"": "Neither", "": "Neither", "Dock": "Docked", "Engage": "Balanced"}

for (match_key, team_number), submission_for_team in scouting_data.groupby(["MatchKey", "TeamNumber"]):
    if not errors.get(match_key):
        errors[match_key] = []
    
    errors_to_list = []

    our_submission = submission_for_team.iloc[0]

    try:
        newton_submission = newton_data[newton_data["What Team are you Observing"] == team_number].iloc[0]
    except IndexError:
        continue

    if our_submission["Mobile"] != (newton_submission["Autonomous - did they move out of the community zone?"] == "Yes"):
        errors_to_list.append(f"For team {team_number}, PRELOADED state is differing.")
    
    # Auto checks

    our_ah_cubes, newton_ah_cubes = our_submission["AutoCubes"].count("High"), newton_submission["Auto Cubes Placed High"]
    our_am_cubes, newton_am_cubes = our_submission["AutoCubes"].count("Mid") != (newton_submission["Auto Cubes Placed Mid"])
    our_al_cubes, newton_al_cubes = our_submission["AutoCubes"].count("Low") != (newton_submission["Auto Cubes Placed Low"])
    our_ah_cones, newton_ah_cones = our_submission["AutoCones"].count("High") != (newton_submission["Auto Cones Placed High"])
    our_am_cones, newton_am_cones = our_submission["AutoCones"].count("Mid") != (newton_submission["Auto Cones Placed Mid"])
    our_al_cones, newton_al_cones = our_submission["AutoCones"].count("Low") != (newton_submission["Auto Cones Placed Low"])

    if abs(our_ah_cubes - newton_ah_cubes) >= AUTO_PIECES_THRESHOLD:
        errors_to_list.append(f"For team {team_number}, we said {our_ah_cubes} CUBES were placed at HIGH for AUTO but Newton said {newton_ah_cubes} were placed.")
    if abs(our_am_cubes - newton_am_cubes) >= AUTO_PIECES_THRESHOLD:
        errors_to_list.append(f"For team {team_number}, we said {our_am_cubes} CUBES were placed at MID for AUTO but Newton said {newton_am_cubes} were placed.")
    if abs(our_al_cubes - newton_al_cubes) >= AUTO_PIECES_THRESHOLD:
        errors_to_list.append(f"For team {team_number}, we said {our_al_cubes} CUBES were placed at LOW for AUTO but Newton said {newton_al_cubes} were placed.")
    if abs(our_ah_cones - newton_ah_cones) >= AUTO_PIECES_THRESHOLD:
        errors_to_list.append(f"For team {team_number}, we said {our_ah_cones} CONES were placed at HIGH for AUTO but Newton said {newton_ah_cones} were placed.")
    if abs(our_am_cones - newton_am_cones) >= AUTO_PIECES_THRESHOLD:
        errors_to_list.append(f"For team {team_number}, we said {our_am_cones} CONES were placed at MID for AUTO but Newton said {newton_am_cones} were placed.")
    if abs(our_al_cones - newton_al_cones) >= AUTO_PIECES_THRESHOLD:
        errors_to_list.append(f"For team {team_number}, we said {our_al_cones} CONES were placed at LOW for AUTO but Newton said {newton_al_cones} were placed.")
    
    # Teleop checks

    our_th_cubes, newton_th_cubes = our_submission["TeleopCubes"].count("High"), newton_submission["Tele-Op Cubes Placed High"]
    our_tm_cubes, newton_tm_cubes = our_submission["TeleopCubes"].count("Mid") != (newton_submission["Tele-Op Cubes Placed Mid"])
    our_tl_cubes, newton_tl_cubes = our_submission["TeleopCubes"].count("Low") != (newton_submission["Tele-Op Cubes Placed Low"])
    our_th_cones, newton_th_cones = our_submission["TeleopCones"].count("High") != (newton_submission["Tele-Op Cones Placed High"])
    our_tm_cones, newton_tm_cones = our_submission["TeleopCones"].count("Mid") != (newton_submission["Tele-Op Cones Placed Mid"])
    our_tl_cones, newton_tl_cones = our_submission["TeleopCones"].count("Low") != (newton_submission["Tele-Op Cones Placed Low"])

    if abs(our_th_cubes - newton_th_cubes) >= TELEOP_PIECES_THRESHOLD:
        errors_to_list.append(f"For team {team_number}, we said {our_th_cubes} CUBES were placed at HIGH for TELEOP but Newton said {newton_th_cubes} were placed.")
    if abs(our_tm_cubes - newton_tm_cubes) >= TELEOP_PIECES_THRESHOLD:
        errors_to_list.append(f"For team {team_number}, we said {our_tm_cubes} CUBES were placed at MID for TELEOP but Newton said {newton_tm_cubes} were placed.")
    if abs(our_tl_cubes - newton_tl_cubes) >= TELEOP_PIECES_THRESHOLD:
        errors_to_list.append(f"For team {team_number}, we said {our_tl_cubes} CUBES were placed at LOW for TELEOP but Newton said {newton_tl_cubes} were placed.")
    if abs(our_th_cones - newton_th_cones) >= TELEOP_PIECES_THRESHOLD:
        errors_to_list.append(f"For team {team_number}, we said {our_th_cones} CONES were placed at HIGH for TELEOP but Newton said {newton_ah_cones} were placed.")
    if abs(our_tm_cones - newton_tm_cones) >= TELEOP_PIECES_THRESHOLD:
        errors_to_list.append(f"For team {team_number}, we said {our_tm_cones} CONES were placed at MID for TELEOP but Newton said {newton_tm_cones} were placed.")
    if abs(our_tl_cones - newton_tl_cones) >= TELEOP_PIECES_THRESHOLD:
        errors_to_list.append(f"For team {team_number}, we said {our_tl_cones} CONES were placed at LOW for TELEOP but Newton said {newton_tl_cones} were placed.")
    
    # Charge station checks
    if (our_state := charge_station_to_newton[our_submission["AutoChargingState"]]) != (newton_state := newton_submission["Autonomous ended - Docked or Balanced or Neither?"]):
        errors_to_list.append(f"For team {team_number}, we said their robot did {our_state} at the end of AUTO but Newton said they did {newton_state}")

    if (our_state := charge_station_to_newton[our_submission["EndgameFinalCharge"]]) != (newton_state := newton_submission["Teleop ended - Docked or Balanced or Neither?"]):
        errors_to_list.append(f"For team {team_number}, we said their robot did {our_state} at the end of AUTO but Newton said they did {newton_state}")
    
    submission_for_team["8592QualitativeData"] = {
        name: newton_submission[name] for name in [
            "How tippy are they?",
            "Driver rating",
            "Where do they get it from?",
            "Were they inactive?",
            "How well can they keep cones",
            "How well can they keep cubes",
            "What did you like about their performance",
            "What did you dislike about their performance",
            "Other comments:"
        ]
    }

    errors[match_key].append("\n".join(errors_to_list))

with open("../data/2023new_flagged_data.json", "w") as file:
    json.dump(errors, file, indent=2)

with open("../data/2023new_match_data.json", "w") as file:
    json.dump(scouting_data.to_dict(orient="records"), file, indent=2)
    