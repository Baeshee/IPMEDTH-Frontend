import requests

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