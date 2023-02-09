from json import load

from ..data_val_2023 import DataValidation2023


def example_scouting_data(
    scout_id: str = "falcon",
    match_key: str = "qm1",
    team_number: int = 4099,
    alliance: str = "red",
    driver_station: int = 1,
    preloaded: bool = True,
    mobile: bool = True,
    auto_cones: list[str] = ["High", "Mid", "Low"],
    auto_cubes: list[str] = ["High", "Mid", "Low"],
    auto_misses: list[tuple] = [("Mid", "Cone"), ("Low", "Cube")],
    teleop_cones: list[str] = ["High", "Mid", "Low"],
    teleop_cubes: list[str] = ["High", "Mid", "Low"],
    teleop_misses: list[tuple] = [("Mid", "Cone"), ("Low", "Cube")],
    auto_docked: bool = False,
    auto_engaged: bool = False,
    docked: bool = False,
    engaged: bool = False,
    defense_pct: float = 0.5,
    defense_rating: float = 5.0,
    counter_defense_pct: float = 0.5,
    counter_defense_rating: float = 5.0,
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
    :param preloaded: Whether or not the robot had a game piece preloaded when the match started.
    :param mobile: Whether or not the robot left the community during auto.
    :param auto_cones: A list containing the type of node where each cone was scored in auto.
    :param auto_cubes: A list containing the type of node where each cube was scored in auto.
    :param auto_misses: A list containing the type of node and the type of game piece that the robot missed in auto.
    :param teleop_cones: A list containing the type of node where each cone was scored in teleop.
    :param teleop_cubes: A list containing the type of node where each cube was scored in teleop.
    :param teleop_misses: A list containing the type of node and the type of game piece that the robot missed in teleop.
    :param auto_docked: A boolean representing whether or not the robot docked to the charge station in auto.
    :param auto_engaged: A boolean representing whether or not the robot was engaged to the charge station in auto.
    :param docked: A boolean representing whether or not the robot was docked to the charge station in endgame.
    :param engaged: A boolean representing whether or not the robot was engaged to the charge station in endgame.
    :param defense_pct: % representing how much the robot played defense.
    :param defense_rating: Rating on a scale of 1 to 5 on how well the robot played defense.
    :param counter_defense_pct: % representing how much the robot played counter defense.
    :param counter_defense_rating: Rating on a scale of 1 to 5 on how well the robot played counter defense.
    :param driver_rating: Rating on a scale of 1 to 5 on how good the driving was of the robot.
    :param auto_notes: Notes regarding anything about the robot during auto.
    :param teleop_notes: Notes regarding anything about the robot during teleop.
    :param misc_notes: Notes regarding any final thoughts about the robot overall.
    :return: Dictionary containing example scouting data with customizations provided.
    """
    return {
        "scout_id": scout_id,
        "match_key": match_key,
        "team_number": team_number,
        "alliance": alliance,
        "driver_station": driver_station,
        "preloaded": preloaded,
        "mobile": mobile,
        "auto_cones": auto_cones,
        "auto_cubes": auto_cubes,
        "auto_misses": auto_misses,
        "teleop_cones": teleop_cones,
        "teleop_cubes": teleop_cubes,
        "teleop_misses": teleop_misses,
        "auto_docked": auto_docked,
        "auto_engaged": auto_engaged,
        "docked": docked,
        "engaged": engaged,
        "defense_pct": defense_pct,
        "defense_rating": defense_rating,
        "counter_defense_pct": counter_defense_pct,
        "counter_defense_rating": counter_defense_rating,
        "driver_rating": driver_rating,
        "auto_notes": auto_notes,
        "teleop_notes": teleop_notes,
        "misc_notes": misc_notes,
    }


def test_defense_rating_but_no_defense_pct():
    """Tests `check_for_invalid_defense_data` to ensure errors are written w/ given defense rating but no defense %"""
    data_validator = DataValidation2023()
    data_validator._run_with_tba = False

    scouting_data_with_no_defense_pct = example_scouting_data(defense_pct=float("nan"))

    data_validator.validate_data(scouting_data=[scouting_data_with_no_defense_pct])

    with open("../data/errors.json") as file:
        errors = load(file)

    assert len(errors) == 1 and errors[0]["error_type"] == "MISSING DATA"


def test_defense_pct_but_no_defense_rating():
    """Tests `check_for_invalid_defense_data` to ensure errors are written w/ given defense % but no defense rating"""
    data_validator = DataValidation2023()
    data_validator._run_with_tba = False

    scouting_data_with_no_defense_rating = example_scouting_data(
        defense_rating=float("nan")
    )

    data_validator.validate_data(scouting_data=[scouting_data_with_no_defense_rating])

    with open("../data/errors.json") as file:
        errors = load(file)

    assert len(errors) == 1 and errors[0]["error_type"] == "MISSING DATA"


def test_counter_defense_rating_but_no_counter_defense_pct():
    """Tests `check_for_invalid_defense_data` w/ given counter defense rating but no counter defense %"""
    data_validator = DataValidation2023()
    data_validator._run_with_tba = False

    scouting_data_with_no_counter_defense_pct = example_scouting_data(
        counter_defense_pct=float("nan")
    )

    data_validator.validate_data(
        scouting_data=[scouting_data_with_no_counter_defense_pct]
    )

    with open("../data/errors.json") as file:
        errors = load(file)

    assert len(errors) == 1 and errors[0]["error_type"] == "MISSING DATA"


def test_counter_defense_pct_but_no_counter_defense_rating():
    """Tests `check_for_invalid_defense_data` w/ given counter defense % but no counter defense rating"""
    data_validator = DataValidation2023()
    data_validator._run_with_tba = False

    scouting_data_with_no_counter_defense_pct = example_scouting_data(
        counter_defense_rating=float("nan")
    )

    data_validator.validate_data(
        scouting_data=[scouting_data_with_no_counter_defense_pct]
    )

    with open("../data/errors.json") as file:
        errors = load(file)

    assert len(errors) == 1 and errors[0]["error_type"] == "MISSING DATA"
