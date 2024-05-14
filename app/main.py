import requests
import json
import os
import sys

if __name__ == "__main__" and (__package__ is None or __package__ == ''):
    sys.path.append(os.path.dirname(sys.path[0]))
    import config
else:
    from . import config

config_values = config.get_config()

# Construct URLs
LOGIN_URL = f"http://{config_values['server_address']}:{config_values['server_port']}/api/login"
TOKEN_URL = f"http://{config_values['server_address']}:{config_values['server_port']}/api/token"

HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

def login():
    login_data = json.dumps({'password': config_values['password']})
    response = requests.post(LOGIN_URL, headers=HEADERS, data=login_data)
    response.raise_for_status()
    return response.json()['token']

def refresh_token():
    token = login()
    print("Token refreshed, new token:", token)

if __name__ == '__main__':
    token = login()
    print("Initial token obtained:", token)
