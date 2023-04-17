from json import load
from operator import itemgetter

from scipy import spatial

MATCH_KEY = "2023new_qm105"
MATCH_NUMBER = 105

TEAM_WANTED = 422

with (
    open("epas.json") as file,
    open("../data/match_schedule.json") as match_schedule_file,
):
    epas = load(file)
    match_schedule = load(match_schedule_file)

match_epas = [
    epas[team[3:]]
    for team in match_schedule[MATCH_KEY]["red"] + match_schedule[MATCH_KEY]["blue"]
]
match_epas = sorted(match_epas[:3]) + sorted(match_epas[3:])
similar_matches = {}

for full_match_key, alliances in match_schedule.items():
    specific_match_number = int(full_match_key.split("_")[-1][2:])
    teams = alliances["red"] + alliances["blue"]

    if TEAM_WANTED and f"frc{TEAM_WANTED}" not in teams:
        continue

    if specific_match_number < MATCH_NUMBER:
        match_specific_epas = [epas[team[3:]] for team in teams]
        match_specific_epas = sorted(match_specific_epas[:3]) + sorted(
            match_specific_epas[3:]
        )

        cosine_similarity = 1 - spatial.distance.cosine(match_epas, match_specific_epas)
        similar_matches[full_match_key] = cosine_similarity * 100

similar_matches = dict(sorted(similar_matches.items(), key=itemgetter(1), reverse=True))

for match_key, similarity in similar_matches.items():
    print(f"{match_key} had a similarity of {similarity:.2f}%")
