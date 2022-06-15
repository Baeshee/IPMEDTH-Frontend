"""Handle all the requests to the API."""

import json
from datetime import date

import aiohttp
import requests

from const import BASE_URL


async def login_request(email, password):
    """Login request to the API.

    Args:
        email (str): Email of the user.
        password (str): Password of the user.
    """
    url = f"{BASE_URL}/api/auth/login"
    payload = {"email": email, "password": password}

    async with aiohttp.ClientSession() as request:
        async with request.post(url, data=payload) as response:
            if response.status == 200:
                res = await response.json()
                token = res["data"]["token"]
                token_type = res["data"]["token_type"]
                user = res["data"]["name"]
                return "Ok", [token, token_type, user]
            res = await response.json()
            return "Failed", res["message"]


async def logout_request(token_type, token):
    """Logout request to the API.

    Args:
        token_type (str): Token type that is been used.
        token: Token of the user.
    """
    headers = {"Authorization": f"{token_type} {token}"}
    url = f"{BASE_URL}/api/auth/logout"

    async with aiohttp.ClientSession() as request:
        async with request.post(url, headers=headers) as response:
            if response.status == 200:
                res = await response.json()
                return "Ok", res["message"]
            res = await response.json()
            return "Failed", res["message"]


async def session_request(token_type, token, patient_id):
    """Session request to the API.

    Args:
        token_type (str): Token type that is been used.
        token: Token of the user.
        patient: Used patient id.
    """
    headers = {"Authorization": f"{token_type} {token}"}
    url = f"{BASE_URL}/api/sessions"

    body = {
        "patient_id": patient_id,
        "date": date.today().strftime("%d-%m-%Y"),
    }
    async with aiohttp.ClientSession() as request:
        async with request.post(url, headers=headers, data=body) as response:
            if response.status == 200:
                res = await response.json()
                return "Ok", res["data"]["id"]
            res = await response.json()
            return "Failed", res["message"]


async def upload_request(token_type, token, session_id, hand_data, image_path):
    """Upload request to the API.

    Args:
        token_type (str): Token type that is been used.
        token: Token of the user.
        session_id: Used session id.
    """
    headers = {"Authorization": f"{token_type} {token}"}
    url = f"{BASE_URL}/api/measurements"
    image = open(image_path, "rb")

    body = {
        "session_id": session_id,
        "hand_type": hand_data["hand_type"],
        "hand_view": hand_data["hand_view"],
        "hand_score": hand_data["hand_score"],
        "finger_thumb": json.dumps(hand_data["landmarks"]["finger_thumb"]),
        "finger_index": json.dumps(hand_data["landmarks"]["finger_index"]),
        "finger_middle": json.dumps(hand_data["landmarks"]["finger_middle"]),
        "finger_ring": json.dumps(hand_data["landmarks"]["finger_ring"]),
        "finger_pink": json.dumps(hand_data["landmarks"]["finger_pink"]),
        "wrist": json.dumps(hand_data["landmarks"]["wrist"]),
    }

    files = {
        "image": image,
        "Content-Type": "image/png",
    }

    response = requests.post(url, headers=headers, data=body, files=files)
    if response.status_code == 200:
        image.close()
        res = response.json()
        return "Ok", res["message"]
    res = response.json()
    return "Failed", res["message"]


async def make_patient_request(token_type, token, name, email, date_of_birth):
    """Make patient request to the API.

    Args:
        token_type (str): Token type that is been used.
        token: Token of the user.
        name (str): Name of the patient.
        email (str): Email of the patient.
        date_of_birth (str): Date of birth of the patient.
    """
    headers = {"Authorization": f"{token_type} {token}"}
    url = f"{BASE_URL}/api/patients"

    body = {"name": name, "email": email, "date_of_birth": date_of_birth}
    async with aiohttp.ClientSession() as request:
        async with request.post(url, headers=headers, data=body) as response:
            if response.status == 200:
                res = await response.json()
                return "Ok", res
            res = response.json()
            return "Failed", res["message"]


async def get_patient_request(token_type, token):
    """Get patient request to the API.

    Args:
        token_type (str): Token type that is been used.
        token: Token of the user.
    """
    headers = {"Authorization": f"{token_type} {token}"}
    url = f"{BASE_URL}/api/patients"

    async with aiohttp.ClientSession() as request:
        async with request.get(url, headers=headers) as response:
            if response.status == 200:
                res = await response.json()
                return "Ok", res["data"]
            res = await response.json()
            return "Failed", res["message"]


async def get_image_request(token_type, token, image):
    """Get image request to the API.

    Args:
        token_type (str): Token type that is been used.
        token: Token of the user.
        image (str): Image name.
    """
    headers = {"Authorization": f"{token_type} {token}"}
    url = f"{BASE_URL}/images/measurements/{image}"

    async with aiohttp.ClientSession() as request:
        async with request.get(url, headers=headers) as response:
            if response.status == 200:
                res = await response.read()
                return "Ok", res
