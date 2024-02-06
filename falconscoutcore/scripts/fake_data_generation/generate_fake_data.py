from enum import Enum
from json import dump, load
from random import choice, random, randint, shuffle


class Performance(Enum):
    BEST = 1
    GOOD = 2
    OKAY = 3
    POOR = 4
    VERY_POOR = 5


teams = {
    339: Performance.POOR,
    422: Performance.GOOD,
    539: Performance.VERY_POOR,
    540: Performance.POOR,
    612: Performance.OKAY,
    617: Performance.POOR,
    620: Performance.GOOD,
    836: Performance.BEST,
    1522: Performance.OKAY,
    1599: Performance.GOOD,
    1731: Performance.BEST,
    1895: Performance.OKAY,
    2106: Performance.GOOD,
    2199: Performance.GOOD,
    2421: Performance.OKAY,
    2534: Performance.POOR,
    2998: Performance.VERY_POOR,
    3136: Performance.GOOD,
    3373: Performance.OKAY,
    4099: Performance.BEST,
    4286: Performance.POOR,
    4505: Performance.POOR,
    5587: Performance.POOR,
    5954: Performance.VERY_POOR,
    6863: Performance.OKAY,
    8326: Performance.VERY_POOR,
    8590: Performance.POOR,
    8592: Performance.BEST,
    9684: Performance.POOR,
    9709: Performance.POOR
}

# match_schedule = []
# current_match_number = 1

# for repeat_by in range(1, 13):
#     teams_to_choose = list(teams.keys())

#     for match_number in range(1, 6):
#         if current_match_number == 60:
#             break

#         shuffle(teams_to_choose)

#         match_teams = teams_to_choose[:6]
#         red_alliance = match_teams[:3]
#         blue_alliance = match_teams[3:]

#         match_schedule.append(
#             {
#                 "match_key": f"qm{current_match_number}",
#                 "red_alliance": red_alliance,
#                 "blue_alliance": blue_alliance
#             }
#         )

#         for team in red_alliance + blue_alliance:
#             teams_to_choose.remove(team)
        
#         current_match_number += 1


# with open("./falconscoutcore/scripts/fake_data_generation/match_schedule.json", "w") as file:
#     dump(match_schedule, file, indent=2)

with open("match_schedule.json") as file:
    match_schedule = load(file)

scouting_data = []
parameters = {
    "AutoSpeaker": list(range(7)),
    "AutoAmp": list(range(3)),
    "TeleopSpeaker": list(range(12)),
    "TeleopAmp": list(range(6)),
    "TeleopTrap": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    "ClimbStatus": [True, False],
    "Harmonized": [True, False],
    "ClimbSpeed": ["Slow", "Fast"],
    "Disabled": [True, False],
    "DriverRating": ["Very Fluid", "Fluid", "Average", "Poor", "Very Poor"],
    "DefenseTime": ["Very Often", "Often", "Sometimes", "Rarely", "Never"],
    "DefenseSkill": ["Very Good", "Good", "Okay", "Poor", "Very Poor"],
    "CounterDefenseSkill": ["Very Good", "Good", "Okay", "Poor", "Very Poor"],
}
all_data = []

for match in match_schedule:
    red_alliance = True

    for idx, team in enumerate(match["red_alliance"] + match["blue_alliance"], start=1):
        if idx == 4:
            idx = 1
            red_alliance = False

        scouting_data = {
            "ScoutId": "shayaan",
            "MatchKey": match["match_key"],
            "Alliance": ("red" if red_alliance else "blue"),
            "DriverStation": idx,
            "TeamNumber": team,
        }
        team_strength = teams[team]
        dice = random()
        runs_amp_auto = dice < 0.1

        if team_strength == Performance.BEST:
            focus_on_amp = dice < 0.5
            total_cycles = choice(list(range(7, 12)))

            if focus_on_amp:
                tele_amp = int(randint(5, 7) / 10 * total_cycles)
                tele_speaker = total_cycles - tele_amp
            else:
                tele_speaker = int(randint(7, 10) / 10 * total_cycles)
                tele_amp = total_cycles - tele_speaker

            scouting_data.update(
                {
                    "AutoSpeaker": 0 if runs_amp_auto else choice(parameters["AutoSpeaker"][-4:]),
                    "AutoAmp": 0 if not runs_amp_auto else choice(parameters["AutoAmp"][-2:]),
                    "AutoLeave": True,
                    "AutoNotes": "",
                    "TeleopSpeaker": tele_speaker,
                    "TeleopAmp": tele_amp,
                    "TeleopTrap": choice(parameters["TeleopTrap"]),
                    "Parked": dice < 0.95,
                    "ClimbStatus": (climbs := dice < 0.9),
                    "Harmonized": climbs and dice < 0.5,
                    "ClimbSpeed": parameters["ClimbSpeed"][-1] if climbs else "",
                    "EndgameNotes": "",
                    "Disabled": dice < 0.02,
                    "DriverRating": choice(parameters["DriverRating"][:3]),
                    "DefenseTime": (defense_time := choice(parameters["DefenseTime"][-2:])),
                    "DefenseSkill": choice(parameters["DefenseSkill"][:2]) if defense_time != "Never" else "",
                    "CounterDefenseSkill": choice(parameters["CounterDefenseSkill"][:2]) if dice < 0.3 else "",
                    "RatingNotes": ""
                }
            )
        elif team_strength == Performance.GOOD:
            scouting_data.update(
                {
                    "AutoSpeaker": (auto_speaker := 0 if runs_amp_auto else choice(parameters["AutoSpeaker"][1:4])),
                    "AutoAmp": 0 if not runs_amp_auto else choice(parameters["AutoAmp"][:-1]),
                    "AutoLeave": False if auto_speaker <= 1 and not runs_amp_auto else True,
                    "AutoNotes": "",
                    "TeleopSpeaker": (teleop_speaker := choice(parameters["TeleopSpeaker"][2:8])),
                    "TeleopAmp": choice([amp_cycle for amp_cycle in parameters["TeleopAmp"] if amp_cycle + teleop_speaker <= 8]),
                    "TeleopTrap": 0,
                    "Parked": dice < 0.9,
                    "ClimbStatus": (climbs := dice < 0.7),
                    "Harmonized": climbs and dice < 0.3,
                    "ClimbSpeed": (parameters["ClimbSpeed"][0] if dice < 0.4 else parameters["ClimbSpeed"][1]) if climbs else "",
                    "EndgameNotes": "",
                    "Disabled": dice < 0.1,
                    "DriverRating": choice(parameters["DriverRating"][1:4]),
                    "DefenseTime": (defense_time := choice(parameters["DefenseTime"][-3:])),
                    "DefenseSkill": choice(parameters["DefenseSkill"][1:4]) if defense_time != "Never" else "",
                    "CounterDefenseSkill": choice(parameters["CounterDefenseSkill"][1:4]) if dice < 0.3 else "",
                    "RatingNotes": ""
                }
            )
        elif team_strength == Performance.OKAY:
            scouting_data.update(
                {
                    "AutoSpeaker": (auto_speaker := 0 if runs_amp_auto else choice(parameters["AutoSpeaker"][:3])),
                    "AutoAmp": 0 if not runs_amp_auto else choice(parameters["AutoAmp"][:-1]),
                    "AutoLeave": False if auto_speaker <= 1 and not runs_amp_auto else True,
                    "AutoNotes": "",
                    "TeleopSpeaker": (teleop_speaker := choice(parameters["TeleopSpeaker"][1:5])),
                    "TeleopAmp": choice([amp_cycle for amp_cycle in parameters["TeleopAmp"] if amp_cycle + teleop_speaker <= 5]),
                    "TeleopTrap": 0,
                    "Parked": dice < 0.9,
                    "ClimbStatus": (climbs := dice < 0.4),
                    "Harmonized": climbs and dice < 0.3,
                    "ClimbSpeed": (parameters["ClimbSpeed"][0] if dice < 0.7 else parameters["ClimbSpeed"][1]) if climbs else "",
                    "EndgameNotes": "",
                    "Disabled": dice < 0.2,
                    "DriverRating": choice(parameters["DriverRating"][2:]),
                    "DefenseTime": (defense_time := choice(parameters["DefenseTime"][-4:])),
                    "DefenseSkill": choice(parameters["DefenseSkill"][2:]) if defense_time != "Never" else "",
                    "CounterDefenseSkill": choice(parameters["CounterDefenseSkill"][2:]) if dice < 0.3 else "",
                    "RatingNotes": ""
                }
            )
        elif team_strength == Performance.POOR:
            scouting_data.update(
                {
                    "AutoSpeaker": choice(parameters["AutoSpeaker"][:3]),
                    "AutoAmp": 0,
                    "AutoLeave": auto_speaker > 1,
                    "AutoNotes": "",
                    "TeleopSpeaker": (teleop_speaker := choice(parameters["TeleopSpeaker"][:4])),
                    "TeleopAmp": 0,
                    "TeleopTrap": 0,
                    "Parked": dice < 0.9,
                    "ClimbStatus": (climbs := dice < 0.2),
                    "Harmonized": climbs and dice < 0.3,
                    "ClimbSpeed": (parameters["ClimbSpeed"][0] if dice < 0.9 else parameters["ClimbSpeed"][1]) if climbs else "",
                    "EndgameNotes": "",
                    "Disabled": dice < 0.3,
                    "DriverRating": choice(parameters["DriverRating"][3:]),
                    "DefenseTime": (defense_time := choice(parameters["DefenseTime"])),
                    "DefenseSkill": choice(parameters["DefenseSkill"][3:]) if defense_time != "Never" else "",
                    "CounterDefenseSkill": choice(parameters["CounterDefenseSkill"][2:]) if dice < 0.1 else "",
                    "RatingNotes": ""
                }
            )
        elif team_strength == Performance.VERY_POOR:
            scouting_data.update(
                {
                    "AutoSpeaker": choice(parameters["AutoSpeaker"][:2]),
                    "AutoAmp": 0,
                    "AutoLeave": dice < 0.2,
                    "AutoNotes": "",
                    "TeleopSpeaker": (teleop_speaker := choice(parameters["TeleopSpeaker"][:3])),
                    "TeleopAmp": 0,
                    "TeleopTrap": 0,
                    "Parked": dice < 0.6,
                    "ClimbStatus": False,
                    "Harmonized": False,
                    "ClimbSpeed": "",
                    "EndgameNotes": "",
                    "Disabled": dice < 0.6,
                    "DriverRating": choice(parameters["DriverRating"][4:]),
                    "DefenseTime": (defense_time := choice(parameters["DefenseTime"])),
                    "DefenseSkill": choice(parameters["DefenseSkill"][4:]) if defense_time != "Never" else "",
                    "CounterDefenseSkill": choice(parameters["CounterDefenseSkill"][4:]) if dice < 0.1 else "",
                    "RatingNotes": ""
                }
            )
        
        all_data.append(scouting_data)


with open("fake_data.json", "w") as file:
    dump(all_data, file, indent=2)
