import requests
from datetime import date
import json

import aiohttp

async def loginRequest(email, password):
    url = "https://www.ipmedth.nl/api/auth/login"
    payload = {
        'email': email,
        'password': password
        }

    async with aiohttp.ClientSession() as request:
        async with request.post(url, data=payload) as r:
            if r.status == 200:
                res = await r.json()
                token = res['data']['token']
                token_type = res['data']['token_type']
                user = res['data']['name']
                return 'Ok', [token, token_type, user]
            else:
                res = await r.json()
                return 'Failed', res['message']
        

async def logoutRequest(token_type, token):
    headers = {'Authorization': f'{token_type} {token}'}
    url = "https://www.ipmedth.nl/api/auth/logout"

    async with aiohttp.ClientSession() as request:
        async with request.post(url, headers=headers) as r:
            if r.status == 200:
                res = await r.json()
                return 'Ok', res['message']
            else:
                res = await r.json()
                return 'Failed', res['message']


async def sessionRequest(token_type, token, patient):
    headers = {'Authorization': f'{token_type} {token}'}
    url = "https://www.ipmedth.nl/api/sessions"
    
    body = {
        "patient_id": patient,
        "date": date.today().strftime("%d-%m-%Y"),
    }
    async with aiohttp.ClientSession() as request:
        async with request.post(url, headers=headers, data=body) as r:
            if r.status == 200:
                res = await r.json()
                return 'Ok', res['data']['id']
            else:
                res = await r.json()
                return 'Failed', res['message']

        
async def uploadRequest(token_type, token, s_id, handData, imagePath):
    headers = {'Authorization': f'{token_type} {token}'}
    url = "https://www.ipmedth.nl/api/measurements"
    image = open(imagePath, 'rb')

    body = {
        "session_id": s_id,
        "hand_type": handData["hand_type"],
        "hand_view": handData["hand_view"],
        "hand_score": handData["hand_score"],
        "finger_thumb": json.dumps(handData["landmarks"]["finger_thumb"]),
        "finger_index": json.dumps(handData["landmarks"]["finger_index"]),
        "finger_middle": json.dumps(handData["landmarks"]["finger_middle"]),
        "finger_ring": json.dumps(handData["landmarks"]["finger_ring"]),
        "finger_pink": json.dumps(handData["landmarks"]["finger_pink"]),
        "wrist": json.dumps(handData["landmarks"]["wrist"]),
    }
    
    files = {
        'image': image,
        'Content-Type': 'image/png',
    }
    
    r = requests.post(url, headers=headers, data=body, files=files)
    if r.status_code == 200:
        image.close()
        res = r.json()
        return 'Ok', res['message']
    else:
        res = await r.json()
        return 'Failed', res['message']


async def makePatientRequest(token_type, token, name, email, date):
    headers = {'Authorization': f'{token_type} {token}'}
    url = "https://www.ipmedth.nl/api/patients"
    
    body = {
        "name": name,
        "email": email,
        "date_of_birth": date
    }
    async with aiohttp.ClientSession() as request:
        async with request.post(url, headers=headers, data=body) as r:
            if r.status == 200:
                res = await r.json()
                return 'Ok', res
            else:
                res = await r.json()
                return 'Failed', res['message']

        
async def getPatientRequest(token_type, token):
    headers = {'Authorization': f'{token_type} {token}'}
    url = "https://www.ipmedth.nl/api/patients"
    
    async with aiohttp.ClientSession() as request:
        async with request.get(url, headers=headers) as r:
            if r.status == 200:
                res = await r.json()
                return 'Ok', res['data']
            else:
                res = await r.json()
                return 'Failed', res['message']
        
async def getImageRequest(token_type, token, image):
    headers = {'Authorization': f'{token_type} {token}'}
    url = f"https://www.ipmedth.nl/images/measurements/{image}"
    
    async with aiohttp.ClientSession() as request:
        async with request.get(url, headers=headers) as r:
            if r.status == 200:
                res = await r.read()
                return 'Ok', res
            else:
                res = await r.json()
                return 'Failed', res
