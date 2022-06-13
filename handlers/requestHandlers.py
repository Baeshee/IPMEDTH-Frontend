import requests
from datetime import date
import json
from PIL import Image

def loginRequest(email, password):
    url = "https://www.ipmedth.nl/api/auth/login"
    payload = {
        'email': email,
        'password': password
        }
    try:
        r = requests.post(url, data=payload)
        res = r.json()
        
        if r.status_code == 200:
            token = res['data']['token']
            token_type = res['data']['token_type']
            user = res['data']['name']
            return 'Ok', [token, token_type, user]
        else:
            return 'Failed', res['message']
    except requests.exceptions.HTTPError as e:
        print(e)
        

def logoutRequest(token_type, token):
    headers = {'Authorization': f'{token_type} {token}'}
    url = "https://www.ipmedth.nl/api/auth/logout"
    try:
        r = requests.post(url, headers=headers)
        res = r.json()
        
        if r.status_code == 200:
            return 'Ok', res['message']
        else:
            return 'Failed', res['message']
    except requests.exceptions.HTTPError as e:
        print(e)


def sessionRequest(token_type, token, patient):
    headers = {'Authorization': f'{token_type} {token}'}
    url = "https://www.ipmedth.nl/api/sessions"
    
    body = {
        "patient_id": patient,
        "date": date.today().strftime("%d-%m-%Y"),
    }
    try:
        r = requests.post(url, headers=headers, data=body)
        res = r.json()
        
        if r.status_code == 200:
            return 'Ok', res['data']['id']
        else:
            return 'Failed', res['message']
    except requests.exceptions.HTTPError as e:
        print(e)

        
def uploadRequest(token_type, token, s_id, handData, imagePath):
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
    try:
        r = requests.post(url, headers=headers, data=body, files=files)
        image.close()
        res = r.json()
        
        if r.status_code == 200:
            return 'Ok', res['message']
        else:
            return 'Failed', res['message']
    except requests.exceptions.HTTPError as e:
        print(e)


def makePatientRequest(token_type, token, name, email, date):
    headers = {'Authorization': f'{token_type} {token}'}
    url = "https://www.ipmedth.nl/api/patients"
    
    body = {
        "name": name,
        "email": email,
        "date_of_birth": date
    }
    try:
        r = requests.post(url, headers=headers, data=body)
        res = r.json()
        
        if r.status_code == 200:
            return 'Ok', res
        else:
            return 'Failed', res['message']
    except requests.exceptions.HTTPError as e:
        print(e)

        
def getPatientRequest(token_type, token):
    headers = {'Authorization': f'{token_type} {token}'}
    url = "https://www.ipmedth.nl/api/patients"
    
    try:
        r = requests.get(url, headers=headers)
        res = r.json()
        
        if r.status_code == 200:
            return 'Ok', res['data']
        else:
            return 'Failed', res['message']
    except requests.exceptions.HTTPError as e:
        print(e)
