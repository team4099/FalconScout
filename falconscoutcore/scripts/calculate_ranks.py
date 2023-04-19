import statistics

import pandas as pd

rankings = pd.read_csv("ranks.csv")
teams = [116, 122, 346, 384, 401, 422, 449, 611, 612, 614, 620, 623, 686, 836, 888, 977, 1086, 1111, 1123, 1262, 1389, 1418, 1599, 1610, 1629, 1727, 1731, 1895, 1908, 2028, 2068, 2106, 2199, 2363, 2377, 2421, 2537, 3136, 3373, 3939, 4099, 4456, 4472, 4541, 5115, 5338, 5549, 5587, 5724, 5804, 6326, 6802, 6863, 7770, 8230, 8592, 8622, 8726, 9033, 9072]
ranks = {team: [] for team in teams}

for team in teams:
    ranks[team].extend([1] * list(rankings["Red First"]).count(team))
    ranks[team].extend([2] * list(rankings["Red Second"]).count(team))
    ranks[team].extend([3] * list(rankings["Red Third"]).count(team))
    ranks[team].extend([1] * list(rankings["Blue First"]).count(team))
    ranks[team].extend([2] * list(rankings["Blue Second"]).count(team))
    ranks[team].extend([3] * list(rankings["Blue Third"]).count(team))

ranks = dict(sorted({team: statistics.mean(total_ranks) for team, total_ranks in ranks.items()}.items(), key=lambda pair: pair[1]))

for team, rank in ranks.items():
    print(f"{team} has an average rank of {rank}")