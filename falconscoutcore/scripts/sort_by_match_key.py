from json import dump, load

with open("../data/2023new_match_data.json") as file:
    data = load(file)

data = sorted(data, key=lambda item: int(item["MatchKey"].replace("qm", "")))

with open("../data/2023new_match_data.json", "w") as file:
    dump(data, file, indent=2)