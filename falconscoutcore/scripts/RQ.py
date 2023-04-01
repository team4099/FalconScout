from json import load

import falcon_alliance
import matplotlib.pyplot as plt

with (
    open("../data/2023vaale_match_data.json") as file,
    falcon_alliance.ApiClient(api_key="6lcmneN5bBDYpC47FolBxp2RZa4AbQCVpmKMSKw9x9btKt7da5yMzVamJYk0XDBm") as api_client
):
    alexandria_event = falcon_alliance.Event("2023vaale")
    scouting_data = load(file)
    plotter = falcon_alliance.Plotter(auto_plot=False)

    teams = [team.key.replace("frc", "") for team in alexandria_event.teams()]
    cycle_amounts = {
        team: [len(submission["AutoCones"]) + len(submission["AutoCubes"]) + len(submission["TeleopCones"]) + len(submission["TeleopCubes"]) for submission in scouting_data if submission["TeamNumber"] == int(team)] 
        for team in teams
    }
    cycle_amounts = dict(sorted(cycle_amounts.items(), key=lambda tup: sum(tup[1]), reverse=True))
    

    _, ax = plotter.violin_plot(cycle_amounts.values(), range(len(teams)), title="Point Distribution at 2023vaale")
    ax.set_xticks(range(len(teams)), cycle_amounts.keys(), rotation=90)
    plt.show()
    
