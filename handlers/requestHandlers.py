import requests
from datetime import date

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
        r = requests.post(url, data=body, headers=headers)
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
        "finger_thumb": handData["landmarks"]["finger_thumb"],
        "finger_index": handData["landmarks"]["finger_index"],
        "finger_middle": handData["landmarks"]["finger_middle"],
        "finger_ring": handData["landmarks"]["finger_ring"],
        "finger_pink": handData["landmarks"]["finger_pink"],
        "wrist": handData["landmarks"]["wrist"],
        "image": image
    }
    try:
        r = requests.post(url, data=body, headers=headers)
        image.close()
        # res = r.json()
        
        if r.status_code == 200:
            return 'Ok', "Saved successfully"
        else:
            return 'Failed', "Failed to save"
    except requests.exceptions.HTTPError as e:
        print(e)