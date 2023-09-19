from collections import Counter
from pandas import read_json

scouting_data = read_json("../data/2023_scouting_data.json")

# Total QR codes scanned
print(f"In total, 2710 QR codes were scanned this season.\n")

# Total matches scouted
print(f"In total, {len(set(scouting_data['MatchKey']))} matches were scouted.\n")

# Total time scouted (in hours)
print(
    f"In total, throughout competitions scouts scouted for "
    f"90 hours and {len(scouting_data) * 2.5 % 60:.0f} minutes\n"
)

# Most dedicated scouter
n_scouts = 3

for event_key, comp_name in {
    "2023mdbet": "Week 2", "2023vaale": "Week 3", "2023chcmp": "DCMP", "2023new": "Worlds"
}.items():
    print(f"Most dedicated scouters at {comp_name}")
    filtered_scouting_data = scouting_data[scouting_data['MatchKey'].str.contains(event_key)]
    scouting_numbers = Counter(filtered_scouting_data['ScoutId'])
    for placement, (name, matches_scouted) in enumerate(scouting_numbers.most_common(n_scouts), start=1):
        print(
            f"{placement}. {name.title()} scouted {matches_scouted} matches or scouted matches for a total of "
            f"{matches_scouted * 2.5 / 60:.1f} hours, counting the match time only."
        )
    print()
