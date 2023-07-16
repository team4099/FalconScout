import asyncio
import datetime
import os
from ast import literal_eval
from json import dump, load
from typing import Any

import cv2
import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from github import Github
from pyzbar.pyzbar import decode
from streamlit.components.v1 import html

# Hacky solution to work around Streamlit raising an error about "no event loop" - breaks PEP8
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

from data_validation.data_val_2023 import DataValidation2023

load_dotenv()
github_instance = Github(os.getenv("GITHUB_KEY"))

# Load files for global use.
with open("config.json") as config_file:
    CONFIG = load(config_file)

# Streamlit page configuration
st.set_page_config(layout="wide")


# Helper functions
def _convert_string_to_proper_type(value: str) -> Any:
    """Converts a string to its proper type (eg "3" -> 3) for converting the Pandas dataframe.

    :param value: A string representing the value to convert to its proper type.
    :return:
    """
    try:
        return literal_eval(value)
    except (ValueError, SyntaxError):
        return value


def _process_data(*data: list[str], status_message_col) -> None:
    """Takes raw data from a scanned QR code and processes it into a dictionary before writing it back to the data file.

    :param raw_data: A variable amount of strings passed in representing the multiple different QR codes.
    :param status_message_col: The Streamlit column for displaying status messages.
    :return:
    """
    data_maps = []

    for raw_data in data:
        data_labels = CONFIG["data_config"]["data_labels"]
        split_data = raw_data.split(CONFIG["data_config"]["delimiter"])

        if len(split_data) != len(data_labels):
            status_message_col.error(
                f"Scanned QR code from {split_data[0]} has {len(split_data)} fields "
                f"while Core expected {len(data_labels)} fields."
                f" The scouter is likely using an older version of FalconScout."
            )
            return

        data_maps.append({field: data for field, data in zip(data_labels, split_data)})

    with open(CONFIG["data_config"]["json_file"], "r+") as data_file:
        scouting_data = load(data_file)
        data_maps = [
            data_map for data_map in data_maps if data_map not in scouting_data
        ]

        # If some QR codes were already scanned
        if len(data_maps) != len(data):
            status_message_col.warning(
                f"{len(data) - len(data_maps)} QR code(s) were already scanned.",
                icon="🚨",
            )

            # If all QR codes were already scanned
            if len(data_maps) == 0:
                return

        scouting_data.extend(data_maps)

        data_file.seek(0)
        dump(scouting_data, data_file, indent=2)
        data_file.truncate()

        status_message_col.success(f"{len(data_maps)} QR code(s) successfully scanned!", icon="✅")


# Main functions
def scan_qrcode(qr_code_col) -> None:
    """Uses st.camera_input to scan QR codes from the scouting app into backend.

    :param qr_code_col: The Streamlit column passed in for the QR code scanner (camera input).
    """
    image = qr_code_col.camera_input("QR Code Scanner", label_visibility="hidden")

    if not image:
        return

    # Read QR code
    bytes_data = image.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    gray_img = cv2.cvtColor(cv2_img, 0)
    qr_codes = decode(gray_img)

    # Process data and write it to the scouting data file.
    if qr_codes:
        _process_data(
            *[qr_code.data.decode("utf-8") for qr_code in qr_codes],
            status_message_col=qr_code_col
        )


def write_dataval_errors(data_val_col) -> None:
    """Writes the data validation errors contained in `errors.json` into the column."""
    with (
        open(CONFIG["data_config"]["error_json"]) as error_file,
        open("./streamlit_components/error_component.html", "r") as component_file
    ):
        scouting_data_errors = load(error_file)
        error_component = component_file.read()

        errors_by_match = sorted(
            scouting_data_errors,
            key=lambda error: int(error["match"][2:]),
            reverse=True
        )

        with data_val_col:
            for error in errors_by_match[:4]:
                html(
                    error_component.format(
                        error_title=error["message"],
                        error_type=error["error_type"],
                        match_key=error["match"],
                        height="150px"
                    ),
                    height=150
                )


def run_dataval(success_col) -> None:
    """Runs the data validation on the current data and writes the errors to `errors.json`

    :param success_col: The column to write status messages for running the data validator in.
    """
    data_validator = DataValidation2023("./data_validation/config.yaml")

    with open(CONFIG["data_config"]["json_file"]) as scouting_data_file:
        data_validator.validate_data(
            load(scouting_data_file)
        )

    # Read how many errors were raised for the status message.
    with open(CONFIG["data_config"]["error_json"]) as error_file:
        amount_of_errors = len(load(error_file))

    if amount_of_errors > 0:
        success_col.warning(
            f"{amount_of_errors} errors were raised when validating the data.",
            icon="🚨"
        )
    else:
        success_col.success(
            "No errors were raised when validating the data!",
            icon="✅"
        )


def sync_to_github(success_col) -> None:
    """Syncs the current scouting data JSON and CSV to GitHub with their respective files.

    :param success_col: The column to write success messages into.
    """
    with open(CONFIG["data_config"]["json_file"]) as file:
        file_json_data = load(file)

    file_csv_data = pd.read_csv(
        CONFIG["data_config"].get(
            "csv_file",
            CONFIG["data_config"]["json_file"].replace("json", "csv")
        )
    )

    repo = github_instance.get_repo(CONFIG["repo_config"]["repo"])
    contents = repo.get_contents(CONFIG["repo_config"]["update_json"])
    repo.update_file(
        contents.path,
        f'updated data @ {datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}',
        str(file_json_data),
        contents.sha,
    )

    contents = repo.get_contents(CONFIG["repo_config"]["update_csv"])
    repo.update_file(
        contents.path,
        f'updated data @ {datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}',
        str(file_csv_data),
        contents.sha,
    )

    success_col.success("Successfully synced to Github", icon="✅")


def display_data() -> None:
    """Displays the scouting data in a table format that can be edited and is paginated."""
    with open(CONFIG["data_config"]["json_file"]) as data_file:
        scouting_data = load(data_file)
        scouting_df = pd.DataFrame.from_dict(scouting_data)

    data_display_col, status_message_col = st.columns([1.5, 1], gap="medium")

    data_display_col.write("### 📊 Scouting Data Editor")
    status_message_col.write("### ✅ Status Messages")

    resultant_df = data_display_col.data_editor(scouting_df, num_rows="dynamic")

    # Check if the data changed
    if not scouting_df[~scouting_df.apply(tuple, 1).isin(resultant_df.apply(tuple, 1))].empty:
        status_message_col.success("Data changed successfully!", icon="✅")

    resultant_df.to_json(CONFIG["data_config"]["json_file"], orient="records", indent=2)


if __name__ == "__main__":
    st.write("# 🦅 FalconScout Core")

    qr_code_tab, data_tab = st.tabs(["📱 QR Code Scanner", "📝 Scouting Data"])

    # QR code page
    with qr_code_tab:
        qr_code_col, data_val_errors_col = st.columns([1.5, 1])

        qr_code_col.write("### 📱 QR Code Scanner")
        data_val_errors_col.write("### ✅ DataVal Errors")

        scan_qrcode(qr_code_col)
        write_dataval_errors(data_val_errors_col)

        # Add different buttons (validate data and sync to github).
        with st.sidebar:
            st.write("# 🦾 Actions")

            if st.button("Validate Data"):
                run_dataval(qr_code_col)

            if st.button("Sync Github"):
                sync_to_github(qr_code_col)

    # Scouting data editor page
    with data_tab:
        display_data()
