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
    auto_cones: list[str] = [],
    auto_cubes: list[str] = [],
    teleop_cones: list[str] = [],
    teleop_cubes: list[str] = [],
    auto_charging_state: str = "None",
    teleop_charging_state: str = "None",
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
    :param teleop_cones: A list containing the type of node where each cone was scored in teleop.
    :param teleop_cubes: A list containing the type of node where each cube was scored in teleop.
    :param auto_charging_state: A string representing the state of the robot during Autonomous on the charge station.
    :param teleop_charging_state: A string representing the state of the robot during Teleop on the charge station.
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
        "teleop_cones": teleop_cones,
        "teleop_cubes": teleop_cubes,
        "auto_charging_state": auto_charging_state,
        "teleop_charging_state": teleop_charging_state,
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


def test_more_than_one_docked_robot_in_auto():
    """Tests `auto_charge_station_checks` for when more than one robot is marked as docked/engaged."""
    data_validator = DataValidation2023()
    data_validator._run_with_tba = False

    scouting_data_with_invalid_auto = [
        example_scouting_data(alliance="red", auto_docked=True, auto_engaged=True),
        example_scouting_data(alliance="red", auto_docked=True, auto_engaged=True),
        example_scouting_data(alliance="red"),
    ]

    data_validator.validate_data(scouting_data=scouting_data_with_invalid_auto)

    with open("../data/errors.json") as file:
        errors = load(file)

    assert len(errors) == 1 and errors[0]["error_type"] == "INCORRECT DATA"


def test_for_if_engaged_but_not_docked_auto():
    """Tests `auto_charge_station_checks` for when a robot is marked as engaged but not docked."""
    data_validator = DataValidation2023()
    data_validator._run_with_tba = False

    scouting_data_with_invalid_auto = [
        example_scouting_data(alliance="red", auto_docked=False, auto_engaged=True),
        example_scouting_data(alliance="red"),
        example_scouting_data(alliance="red"),
    ]

    data_validator.validate_data(scouting_data=scouting_data_with_invalid_auto)

    with open("../data/errors.json") as file:
        errors = load(file)

    assert len(errors) == 1 and errors[0]["error_type"] == "INCORRECT DATA"


def test_for_if_engaged_but_not_docked():
    """Tests `check_if_engaged_but_not_docked` for when a robot is marked as engaged but not docked."""
    data_validator = DataValidation2023()
    data_validator._run_with_tba = False

    scouting_data_with_invalid_endgame = [
        example_scouting_data(alliance="red", docked=False, engaged=True),
        example_scouting_data(alliance="red"),
        example_scouting_data(alliance="red"),
    ]

    data_validator.validate_data(scouting_data=scouting_data_with_invalid_endgame)

    with open("../data/errors.json") as file:
        errors = load(file)

    assert len(errors) == 1 and errors[0]["error_type"] == "INCORRECT DATA"


def test_for_inconsistent_engaged():
    """Tests `check_for_inconsistent_engaged` for when a robot is marked as engaged but not docked."""
    data_validator = DataValidation2023()
    data_validator._run_with_tba = False

    scouting_data_with_invalid_endgame = [
        example_scouting_data(alliance="red", docked=True, engaged=True),
        example_scouting_data(alliance="red", docked=True, engaged=False),
        example_scouting_data(alliance="red", docked=True, engaged=True),
    ]

    data_validator.validate_data(scouting_data=scouting_data_with_invalid_endgame)

    with open("../data/errors.json") as file:
        errors = load(file)

    assert len(errors) == 1 and errors[0]["error_type"] == "INCORRECT DATA"


def test_for_only_one_robot_engaged():
    """Tests `check_if_engaged_for_only_one_robot` for when only one robot is marked as docked/engaged (impossible)."""
    data_validator = DataValidation2023()
    data_validator._run_with_tba = False

    scouting_data_with_invalid_endgame = [
        example_scouting_data(alliance="red", docked=True, engaged=True),
        example_scouting_data(alliance="red"),
        example_scouting_data(alliance="red"),
    ]

    data_validator.validate_data(scouting_data=scouting_data_with_invalid_endgame)

    with open("../data/errors.json") as file:
        errors = load(file)

    assert len(errors) == 1 and errors[0]["error_type"] == "INCORRECT DATA"


def test_for_invalid_cones_scored_in_auto_without_preloaded():
    """Tests `validate_auto_attempted_game_pieces` for when an invalid amount of game pieces is scored without a preloaded game piece."""  # noqa
    data_validator = DataValidation2023()
    data_validator._run_with_tba = False

    scouting_data_with_invalid_auto = [
        example_scouting_data(auto_cones=["Mid"] * 5, preloaded=False)
    ]

    data_validator.validate_data(scouting_data=scouting_data_with_invalid_auto)

    with open("../data/errors.json") as file:
        errors = load(file)

    assert len(errors) == 1 and errors[0]["error_type"] == "INCORRECT DATA"


def test_for_invalid_cones_scored_in_auto_with_preloaded():
    """Tests `validate_auto_attempted_game_pieces` for when an invalid amount of game pieces is scored with a preloaded game piece."""  # noqa
    data_validator = DataValidation2023()
    data_validator._run_with_tba = False

    scouting_data_with_invalid_auto = [
        example_scouting_data(auto_cones=["Mid"] * 6, preloaded=True)
    ]

    data_validator.validate_data(scouting_data=scouting_data_with_invalid_auto)

    with open("../data/errors.json") as file:
        errors = load(file)

    assert len(errors) == 1 and errors[0]["error_type"] == "INCORRECT DATA"


def test_for_invalid_amount_of_cones_scored():
    """Tests `validate_attempted_game_pieces` for when an invalid amount of cones (>21) is scored during the game."""
    data_validator = DataValidation2023()
    data_validator._run_with_tba = False

    scouting_data_with_invalid_auto = [example_scouting_data(teleop_cones=["Mid"] * 22)]

    data_validator.validate_data(scouting_data=scouting_data_with_invalid_auto)

    with open("../data/errors.json") as file:
        errors = load(file)

    assert len(errors) == 1 and errors[0]["error_type"] == "INCORRECT DATA"


def test_for_invalid_amount_of_cubes_scored():
    """Tests `validate_attempted_game_pieces` for when an invalid amount of cubes (>15) is scored during the game."""
    data_validator = DataValidation2023()
    data_validator._run_with_tba = False

    scouting_data_with_invalid_auto = [example_scouting_data(teleop_cubes=["Mid"] * 16)]

    data_validator.validate_data(scouting_data=scouting_data_with_invalid_auto)

    with open("../data/errors.json") as file:
        errors = load(file)

    assert len(errors) == 1 and errors[0]["error_type"] == "INCORRECT DATA"


def test_for_invalid_amount_of_game_pieces_scored():
    """Tests `validate_attempted_game_pieces` for when more than 27 game pieces are scored during the game."""
    data_validator = DataValidation2023()
    data_validator._run_with_tba = False

    scouting_data_with_invalid_auto = [
        example_scouting_data(teleop_cones=["Mid"] * 15, teleop_cubes=["Mid"] * 13)
    ]

    data_validator.validate_data(scouting_data=scouting_data_with_invalid_auto)

    with open("../data/errors.json") as file:
        errors = load(file)

    assert len(errors) == 1 and errors[0]["error_type"] == "INCORRECT DATA"
