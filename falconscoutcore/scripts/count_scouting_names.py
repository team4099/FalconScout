from json import load

import pandas as pd


with open("../data/2023mdbet_match_data.json") as file:
    scouting_data = load(file)

    scoutingCount = {}

    for submission in scouting_data:

        """
        if "and " in submission["ScoutId"]:
            names = submission["ScoutId"].split("and ")
            name1, name2 = names[0].strip().lower(), names[1].strip().lower()
        else:
            name1 = submission["ScoutId"].strip().lower()
            name2 = "Missing second scout"



        if name1 in scoutingCount.keys():
            scoutingCount[name1] += 1
        else:
            scoutingCount[name1] = 1

        if name2 in scoutingCount.keys():
            scoutingCount[name2] += 1
        else:
            scoutingCount[name2] = 1
        """
        name = str(submission["ScoutId"]).lower()

        if name in scoutingCount.keys():
            scoutingCount[name] += 1
        else:
            scoutingCount[name] = 1

        
for key in scoutingCount:
   print(str(key) + ": " + str(scoutingCount[key]))
