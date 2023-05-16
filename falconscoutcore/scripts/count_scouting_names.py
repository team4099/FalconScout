from collections import defaultdict
from json import load

with open("../data/2023new_match_data.json") as file:
    scouting_data = load(file)
    scouting_count = defaultdict(int)

    for submission in scouting_data:
        scout_id = submission["ScoutId"]
        specific_scout = scout_id.strip().lower().split()[0]
        matches_with_scout = set()

        if "and" in scout_id.split():
            for scout in scout_id.split(" and "):
                specific_scout = scout.strip().lower().split()[0]

                if specific_scout not in matches_with_scout:
                    scouting_count[specific_scout] += 1

                matches_with_scout.add(specific_scout)

        scouting_count[specific_scout] += 1


for key in dict(sorted(scouting_count.items(), key=lambda tup: tup[1])):
    print(str(key) + ": " + str(scouting_count[key]))
