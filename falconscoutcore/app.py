from json import dump, load

import cv2
import numpy as np
import pandas as pd
import streamlit as st
from pyzbar.pyzbar import decode
from st_aggrid import AgGrid

# Load files for global use.
with open("config.json") as config_file:
    CONFIG = load(config_file)


# Helper functions
def _process_data(*data: list[str]) -> None:
    """Takes raw data from a scanned QR code and processes it into a dictionary before writing it back to the data file.

    :param raw_data: A variable amount of strings passed in representing the multiple different QR codes.
    :return:
    """
    data_maps = []

    for raw_data in data:
        data_labels = CONFIG["data_config"]["data_labels"]
        split_data = raw_data.split(CONFIG["data_config"]["delimiter"])

        if len(split_data) != len(data_labels):
            st.error(
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
            st.warning(
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

        st.success(f"{len(data_maps)} QR code(s) successfully scanned!", icon="✅")


# Main functions
def scan_qrcode() -> None:
    """Uses st.camera_input to scan QR codes from the scouting app into backend."""
    image = st.camera_input("QR Code Scanner", label_visibility="hidden")

    if not image:
        return

    # Read QR code
    bytes_data = image.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    gray_img = cv2.cvtColor(cv2_img, 0)
    qr_codes = decode(gray_img)

    # Process data and write it to the scouting data file.
    if qr_codes:
        _process_data(*[qr_code.data.decode("utf-8") for qr_code in qr_codes])


def display_data() -> None:
    """Displays the scouting data in a table format that can be edited and is paginated."""
    with open(CONFIG["data_config"]["json_file"]) as data_file:
        scouting_data = load(data_file)
        scouting_df = pd.DataFrame.from_dict(scouting_data)

    resultant_df = AgGrid(
        scouting_df,
        conversion_errors="coerce",
        editable=True,
        try_to_convert_back_to_original_types=True,
    )["data"]
    print(resultant_df)

    resultant_df.to_json(CONFIG["data_config"]["json_file"], orient="records", indent=2)


if __name__ == "__main__":
    st.write("# 🦅 FalconScout Core")

    qr_code_tab, data_tab = st.tabs(["📱 QR Code Scanner", "📝 Scouting Data"])

    with qr_code_tab:
        st.write("### 📱 QR Code Scanner")
        scan_qrcode()

    with data_tab:
        st.write("### 📝 Scouting Data")
        display_data()
