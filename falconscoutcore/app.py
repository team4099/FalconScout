from json import load, dump

import cv2
import numpy as np
import streamlit as st


# Load files for global use.
with open("config.json") as config_file:
    CONFIG = load(config_file)


def _process_data(raw_data: str) -> None:
    """Takes the raw data from a scanned QR code and processes it into a dictionary before writing it back to the data file.

    :param raw_data: A string split by a delimeter containing each data point in the QR code.
    :return:
    """
    data_labels = CONFIG["data_config"]["data_labels"]
    split_data = raw_data.split(CONFIG["data_config"]["delimiter"])

    if len(split_data) != len(data_labels):
        st.error(
            f"Scanned QR code has {len(split_data)} fields while Core expected {len(data_labels)} fields."
            f" The scouter is likely using an older version of FalconScout."
        )
        return

    data_map = {
        field: data for field, data in zip(data_labels, split_data)
    }

    with open(CONFIG["data_config"]["json_file"], "r+") as data_file:
        scouting_data = load(data_file)
        scouting_data.append(data_map)

        data_file.seek(0)
        dump(scouting_data, data_file, indent=2)
        data_file.truncate()

        st.success(f"QR code successfully scanned!")


def scan_qrcode() -> None:
    """Uses st.camera_input to scan QR codes from the scouting app into backend."""
    image = st.camera_input("QR Code Scanner")

    if not image:
        return

    # Read QR code
    bytes_data = image.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    detector = cv2.QRCodeDetector()

    qr_code_content, *_ = detector.detectAndDecode(cv2_img)

    # Process data and write it to the scouting data file.
    if qr_code_content:
        _process_data(qr_code_content)


if __name__ == '__main__':
    scan_qrcode()
