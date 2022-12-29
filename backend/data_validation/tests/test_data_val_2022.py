from json import load

from data_val_2022 import DataValidation2022


def example_scouting_data(
    scout_id: str = "falcon",
    match_key: str = "qm1",
    team_number: int = 4099,
    alliance: str = "Red",
    driver_station: int = 1,
    preloaded_cargo: int = 0,
    auto_lower_hub: int = 1,
    auto_upper_hub: int = 1,
    auto_misses: int = 1,
    taxied: int = 1,
    auto_shooting_zones: str = "Elsewhere",
    teleop_lower_hub: int = 1,
    teleop_upper_hub: int = 1,
    teleop_misses: int = 1,
    teleop_shooting_zones: str = "Elsewhere",
    attempted_low: int = 0,
    attempted_mid: int = 1,
    attempted_high: int = 1,
    attempted_traversal: int = 1,
    climb_time: float = 15.0,
    final_climb_type: str = "Traversal",
    defense_pct: float = 1.0,
    defense_rating: int = 5,
    counter_defense_pct: int = 0,
    counter_defense_rating: int = 0,
    driver_rating: int = 5,
    auto_notes: str = "",
    teleop_notes: str = "",
    misc_notes: str = "",
) -> dict:
    """
    Represents example scouting data. Customizable via parameters.

    :param scout_id: ID of the scout.
    :param match_key: Key of scouted match (eg qm1).
    :param team_number: Number of team scouted (eg 4099).
    :param alliance: Alliance of team scouted.
    :param driver_station: Driver station of team scouted (eg 1 for Red 1).
    :param preloaded_cargo: Whether or not the robot had cargo preloaded when the match started.
    :param auto_lower_hub: Number of balls shot into the lower hub during Autonomous.
    :param auto_upper_hub: Number of balls shot into the upper hub during Autonomous.
    :param auto_misses: Number of balls missed when shot during Autonomous.
    :param taxied: Whether or not the robot left its tarmac during Autonomous.
    :param auto_shooting_zones: Zones the robot shot in during Autonomous.
    :param teleop_lower_hub: Number of balls shot into the lower hub during Teleop.
    :param teleop_upper_hub: Number of balls shot into the upper hub during Teleop.
    :param teleop_misses: Number of balls missed when shot during Teleop.
    :param teleop_shooting_zones: Zones the robot shot in during Teleop.
    :param attempted_low: Whether or not the robot attempted to get onto the Low rung during any point of Endgame.
    :param attempted_mid: Whether or not the robot attempted to get onto the Mid rung during any point of Endgame.
    :param attempted_high: Whether or not the robot attempted to get onto the High rung during any point of Endgame.
    :param attempted_traversal: Whether or not the robot attempted to get a traversal during any point of Endgame.
    :param climb_time: Time it took to climb to its final climb from when it started climbing.
    :param final_climb_type: Final rung the robot latched onto at the end of Endgame.
    :param defense_pct: % representing how much the robot played defense.
    :param defense_rating: Rating on a scale of 1 to 5 on how well the robot played defense.
    :param counter_defense_pct: % representing how much the robot played counter defense.
    :param counter_defense_rating: Rating on a scale of 1 to 5 on how well the robot played counter defense.
    :param driver_rating: Rating on a scale of 1 to 5 on how good the driving was of the robot.
    :param auto_notes: Notes regarding anything about the robot during Autonomous.
    :param teleop_notes: Notes regarding anything about the robot during Teleop.
    :param misc_notes: Notes regarding any final thoughts about the robot overall.
    :return: Dictionary containing example scouting data with customizations provided.
    """
    return {
        "scout_id": scout_id,
        "match_key": match_key,
        "team_number": team_number,
        "alliance": alliance,
        "driver_station": driver_station,
        "preloaded_cargo": preloaded_cargo,
        "auto_lower_hub": auto_lower_hub,
        "auto_upper_hub": auto_upper_hub,
        "auto_misses": auto_misses,
        "taxied": taxied,
        "auto_shooting_zones": auto_shooting_zones,
        "teleop_lower_hub": teleop_lower_hub,
        "teleop_upper_hub": teleop_upper_hub,
        "teleop_misses": teleop_misses,
        "teleop_shooting_zones": teleop_shooting_zones,
        "attempted_low": attempted_low,
        "attempted_mid": attempted_mid,
        "attempted_high": attempted_high,
        "attempted_traversal": attempted_traversal,
        "climb_time": climb_time,
        "final_climb_type": final_climb_type,
        "defense_pct": defense_pct,
        "defense_rating": defense_rating,
        "counter_defense_pct": counter_defense_pct,
        "counter_defense_rating": counter_defense_rating,
        "driver_rating": driver_rating,
        "auto_notes": auto_notes,
        "teleop_notes": teleop_notes,
        "misc_notes": misc_notes,
    }


def test_missing_shooting_zones():
    """Tests the `check_for_missing_shooting_zones` function to ensure errors are written into the JSON."""
    data_validator = DataValidation2022()

    # Takes fixture of example scouting data and changes the shooting zones.
    scouting_data_without_shooting_zones = example_scouting_data(
        auto_shooting_zones="", teleop_shooting_zones=""
    )

    # Runs the validation of data to ensure errors are put into the corresponding JSON.
    data_validator.validate_data(scouting_data=[scouting_data_without_shooting_zones])

    with open("errors.json") as file:
        errors = load(file)

    filtered_errors = [
        error for error in errors if "NOT SCOUTED" not in error["message"]
    ]
    assert (
        len(filtered_errors) == 2
        and filtered_errors[0]["error_type"] == "MISSING DATA"
        and filtered_errors[1]["error_type"] == "MISSING DATA"
    )


def test_double_scouted():
    """Tests the `check_team_numbers_for_each_match` function to ensure errors are written into the JSON."""
    data_validator = DataValidation2022()

    extra_scouting_data = [
        example_scouting_data(alliance="Red", team_number=3538),
        example_scouting_data(alliance="Red", team_number=1987),
        example_scouting_data(alliance="Red", team_number=1339),
        example_scouting_data(alliance="Red", team_number=1339),
        example_scouting_data(alliance="Blue", team_number=2614),
        example_scouting_data(alliance="Blue", team_number=3357),
        example_scouting_data(alliance="Blue", team_number=2359),
    ]

    data_validator.validate_data(scouting_data=extra_scouting_data)

    with open("errors.json") as file:
        errors = load(file)

    assert len(errors) == 1 and errors[0]["error_type"] == "EXTRA DATA"


def test_missing_teams():
    """Tests the `check_team_numbers_for_each_match` function to ensure errors are written into the JSON."""
    data_validator = DataValidation2022()

    extra_scouting_data = [
        example_scouting_data(alliance="Red", team_number=3538),
        example_scouting_data(alliance="Red", team_number=1987),
        example_scouting_data(alliance="Blue", team_number=2614),
        example_scouting_data(alliance="Blue", team_number=3357),
        example_scouting_data(alliance="Blue", team_number=2359),
    ]

    data_validator.validate_data(scouting_data=extra_scouting_data)

    with open("errors.json") as file:
        errors = load(file)

    assert len(errors) == 1 and errors[0]["error_type"] == "MISSING DATA"
