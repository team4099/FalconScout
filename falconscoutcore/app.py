from ast import literal_eval
from functools import partial
from json import dump, load
from typing import Any

import cv2
import numpy as np
import pandas as pd
import streamlit as st
from pyzbar.pyzbar import decode
from st_aggrid import AgGrid, GridOptionsBuilder


# Constants
SCOUTING_DATA_PAGE_SIZE = 6 * 5

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
def scan_qrcode(qr_code_col, status_message_col) -> None:
    """Uses st.camera_input to scan QR codes from the scouting app into backend.

    :param qr_code_col: The Streamlit column passed in for the QR code scanner (camera input).
    :param status_message_col: The Streamlit column passed in for displaying status messages.
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
            status_message_col=status_message_col
        )


def display_data() -> None:
    """Displays the scouting data in a table format that can be edited and is paginated."""
    with open(CONFIG["data_config"]["json_file"]) as data_file:
        scouting_data = load(data_file)
        scouting_df = pd.DataFrame.from_dict(scouting_data)

    builder = GridOptionsBuilder.from_dataframe(scouting_df)
    builder.configure_default_column(editable=True)
    builder.configure_pagination(
        paginationAutoPageSize=False,
        paginationPageSize=SCOUTING_DATA_PAGE_SIZE
    )

    grid_options = builder.build()

    resultant_df: pd.DataFrame = AgGrid(
        scouting_df,
        gridOptions=grid_options,
        try_to_convert_back_to_original_types=False,
        theme="streamlit"
    )["data"]

    # Convert numbers to their original types
    resultant_df = resultant_df.applymap(partial(pd.to_numeric, errors="ignore"))

    resultant_df.to_json(CONFIG["data_config"]["json_file"], orient="records", indent=2)


if __name__ == "__main__":
    st.write("# 🦅 FalconScout Core")

    qr_code_tab, data_tab = st.tabs(["📱 QR Code Scanner", "📝 Scouting Data"])

    with qr_code_tab:
        qr_code_col, status_message_col = st.columns([1.5, 1])

        qr_code_col.write("### 📱 QR Code Scanner")
        status_message_col.write("### ✅ Status Messages")

        # Two columns passed in where one is for the QR code scanner and the other for status codes.
        scan_qrcode(qr_code_col, status_message_col)

    with data_tab:
        st.write("### 📝 Scouting Data")
        display_data()
