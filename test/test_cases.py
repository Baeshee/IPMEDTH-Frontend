import asyncio
import json

import aiohttp
import pytest
from requestHandlers import (
    getImageRequest,
    getPatientRequest,
    loginRequest,
    makePatientRequest,
    sessionRequest,
    uploadRequest,
)


def test_login_valid():
    email = input("Correct email: ")
    password = input("Correct password: ")
    status, res = asyncio.run(loginRequest(email, password))
    global r
    r = res
    assert status == "Ok", "Test Failed"


def test_login_invalid():
    email = input("Incorrect email: ")
    password = input("Incorrect password: ")
    status, res = asyncio.run(loginRequest(email, password))
    assert status == "Failed", "Test Failed"


def test_new_patient_valid():
    token_type = "Bearer"
    token = r[0]
    name = "Unit Test"
    email = input("Email that doesnt exist yet: ")
    date = "2022-01-01"
    status, res = asyncio.run(makePatientRequest(token_type, token, name, email, date))
    assert status == "Ok", "Test Failed"


def test_new_patient_invalid():
    token_type = "Bearer"
    token = r[0]
    name = ""
    email = input("Already existing email: ")
    date = "2022-01-01"
    status, res = asyncio.run(makePatientRequest(token_type, token, name, email, date))
    assert status == "Failed", "Test Failed"


def test_get_patient_valid():
    token_type = "Bearer"
    token = r[0]
    status, res = asyncio.run(getPatientRequest(token_type, token))
    assert status == "Ok", "Test Failed"


def test_make_session_valid():
    token_type = "Bearer"
    token = r[0]
    patient_id = 1
    status, res = asyncio.run(sessionRequest(token_type, token, patient_id))
    global r2
    r2 = res
    assert status == "Ok", "Test Failed"


def test_make_session_invalid():
    token_type = "Bearer"
    token = r[0]
    patient_id = 500
    status, res = asyncio.run(sessionRequest(token_type, token, patient_id))
    assert status == "Failed", "Test Failed"


def test_get_image_valid():
    token_type = "Bearer"
    token = r[0]
    image = "1655383526-measurement.png"
    status, res = asyncio.run(getImageRequest(token_type, token, image))
    assert status == "Ok", "Test Failed"


def test_get_image_invalid():
    token_type = "Bearer"
    token = r[0]
    image = "0.png"
    status, res = asyncio.run(getImageRequest(token_type, token, image))
    assert status == "Failed", "Test Failed"


def test_upload_image_valid():
    token_type = "Bearer"
    token = r[0]
    session_id = r2
    handData = {
        "hand_type": "right",
        "hand_view": "pink_side",
        "hand_score": 0.95,
        "landmarks": {
            "finger_thumb": {
                "THUMB_IP": {"x": 268, "y": 278},
                "THUMB_CMC": {"x": 150, "y": 282},
                "THUMB_MCP": {"x": 217, "y": 275},
                "THUMB_TIP": {"x": 313, "y": 281},
            },
            "finger_index": {
                "INDEX_FINGER_DIP": {"x": 379, "y": 232},
                "INDEX_FINGER_MCP": {"x": 243, "y": 187},
                "INDEX_FINGER_PIP": {"x": 338, "y": 193},
                "INDEX_FINGER_TIP": {"x": 402, "y": 268},
            },
            "finger_middle": {
                "MIDDLE_FINGER_DIP": {"x": 398, "y": 235},
                "MIDDLE_FINGER_MCP": {"x": 234, "y": 183},
                "MIDDLE_FINGER_PIP": {"x": 349, "y": 187},
                "MIDDLE_FINGER_TIP": {"x": 421, "y": 277},
            },
            "finger_ring": {
                "PINKY_DIP": {"x": 341, "y": 265},
                "PINKY_MCP": {"x": 211, "y": 230},
                "PINKY_PIP": {"x": 297, "y": 237},
                "PINKY_TIP": {"x": 369, "y": 294},
            },
            "finger_pink": {
                "RING_FINGER_DIP": {"x": 382, "y": 253},
                "RING_FINGER_MCP": {"x": 222, "y": 196},
                "RING_FINGER_PIP": {"x": 334, "y": 204},
                "RING_FINGER_TIP": {"x": 405, "y": 295},
            },
            "wrist": {"WRIST": {"x": 54, "y": 247}},
        },
    }
    imagePath = "test/duimView.png"
    status, res = asyncio.run(
        uploadRequest(token_type, token, session_id, handData, imagePath)
    )
    assert status == "Ok", "Test Failed"


if __name__ == "__main__":
    pytest.main(["--no-header", "-v"])
