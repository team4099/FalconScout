from collections import defaultdict
from json import dump, load

import numpy as np
import pandas as pd
from falcon_alliance import ApiClient
from numpy.lib.stride_tricks import sliding_window_view

POSITIONS_TO_INDICES = ["H", "M", "L"]
rankings = defaultdict(lambda: [0, []])

with open("../data/2023new_match_data.json") as file:
    scouting_data = pd.DataFrame.from_dict(load(file))

# Calculate scores
with ApiClient(
    api_key="6lcmneN5bBDYpC47FolBxp2RZa4AbQCVpmKMSKw9x9btKt7da5yMzVamJYk0XDBm"
) as api_client:
    event_matches = api_client.event("2023new_match_data.json").matches()
    total_scores = {
        f"{match.comp_level}{match.match_number}": [
            match.alliances["red"].score,
            match.alliances["blue"].score,
        ]
        for match in event_matches
    }

for match_key, submissions_by_match in scouting_data.groupby("MatchKey"):
    teams = {"red": [], "blue": []}
    co_op_criterion = []
    total_links = {"red": 0, "blue": 0}
    total_charge_station_points = {"red": 0, "blue": 0}
    total_ranking_points = {"red": 0, "blue": 0}
    scores_for_match = total_scores[match_key]

    for alliance, submissions_by_alliance in submissions_by_match.groupby("Alliance"):
        # set teams by alliance per match
        teams[alliance] = list(submissions_by_alliance["TeamNumber"])

        links = 0
        charge_station_points = 0

        # Charge station points
        charge_station_points += (
            len(
                submissions_by_alliance[
                    submissions_by_alliance["AutoChargingState"] == "Engaged"
                ]
            )
            * 12
        )
        charge_station_points += (
            len(
                submissions_by_alliance[
                    submissions_by_alliance["AutoChargingState"] == "Docked"
                ]
            )
            * 8
        )
        charge_station_points += (
            len(
                submissions_by_alliance[
                    submissions_by_alliance["EndgameFinalCharge"] == "Engage"
                ]
            )
            * 10
        )
        charge_station_points += (
            len(
                submissions_by_alliance[
                    submissions_by_alliance["EndgameFinalCharge"] == "Dock"
                ]
            )
            * 6
        )

        auto_grid = np.array([[0] * 9, [0] * 9, [0] * 9])
        for game_piece in (
            submissions_by_alliance["AutoGrid"]
            .apply(lambda info: info.split("|"))
            .sum()
        ):
            if not game_piece:
                continue

            auto_grid[
                POSITIONS_TO_INDICES.index(game_piece[1]), int(game_piece[0]) - 1
            ] = 1

        teleop_grid = np.array([[0] * 9, [0] * 9, [0] * 9])
        for game_piece in (
            submissions_by_alliance["TeleopGrid"]
            .apply(lambda info: info.split("|"))
            .sum()
        ):
            if not game_piece:
                continue

            teleop_grid[
                POSITIONS_TO_INDICES.index(game_piece[1]), int(game_piece[0]) - 1
            ] = 1

        for height in range(3):
            scoring_locations = np.where(
                np.logical_or(teleop_grid[height] == 1, auto_grid[height] == 1)
            )[0]

            try:
                game_pieces_in_link = set()
                sliding_window = sliding_window_view(scoring_locations, 3)

                for possible_link in sliding_window:
                    if np.diff(possible_link).sum() == 2 and all(
                        [
                            scoring_location not in game_pieces_in_link
                            for scoring_location in possible_link
                        ]
                    ):
                        game_pieces_in_link = game_pieces_in_link.union(possible_link)
                        links += 1
            except ValueError:
                pass

        co_op_grid = auto_grid[:, 3:6] + teleop_grid[:, 3:6]
        co_op_grid[co_op_grid > 1] = 1
        co_op_criterion.append(co_op_grid.sum() >= 3)

        total_links[alliance] = links
        total_charge_station_points[alliance] = charge_station_points

    co_op_criteria_met = all(co_op_criterion)

    # Winning ranking points
    if scores_for_match[0] > scores_for_match[1]:
        total_ranking_points["red"] += 2
    elif scores_for_match[1] > scores_for_match[0]:
        total_ranking_points["blue"] += 2
    else:
        total_ranking_points["red"] += 1
        total_ranking_points["blue"] += 1

    # Link ranking points
    if total_links["red"] == 5 or total_links["red"] == 4 and co_op_criteria_met:
        total_ranking_points["red"] += 1
    if total_links["blue"] == 5 or total_links["blue"] == 4 and co_op_criteria_met:
        total_ranking_points["blue"] += 1

    # Activation bonus ranking points
    if total_charge_station_points["red"] >= 26:
        total_ranking_points["red"] += 1
    if total_charge_station_points["blue"] >= 26:
        total_ranking_points["blue"] += 1

    # Add ranking points and calculate
    for team in teams["red"]:
        rankings[int(team)][0] += total_ranking_points["red"]
        rankings[int(team)][1].append(scores_for_match[0])

    for team in teams["blue"]:
        rankings[int(team)][0] += total_ranking_points["blue"]
        rankings[int(team)][1].append(scores_for_match[1])

rankings = {
    team_number: (sort_orders[0], np.mean(sort_orders[1]))
    for team_number, sort_orders in rankings.items()
}
rankings = dict(sorted(rankings.items(), key=lambda pair: pair[1], reverse=True))

with open("../data/2023new_calculated_rankings.json", "w") as file:
    dump(rankings, file, indent=2)
