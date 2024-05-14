from flask import Flask, render_template, jsonify, request
import requests
import json
import os
from threading import Timer

app = Flask(__name__)

def get_config():
    return {
        'server_address': os.getenv('SERVER_ADDRESS', 'localhost'),
        'server_port': os.getenv('SERVER_PORT', '8080'),
        'dash_port': os.getenv('DASH_PORT', '9069'),
        'password': os.getenv('PASSWORD', 'default_password')
    }

config_values = get_config()

LOGIN_URL = f"http://{config_values['server_address']}:{config_values['server_port']}/api/login"
SERVERS_URL = f"http://{config_values['server_address']}:{config_values['server_port']}/api/servers"
LIVE_INFO_URL = f"http://{config_values['server_address']}:{config_values['server_port']}/api/instance/{{id}}/live"

HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

token = None

def login():
    global token
    login_data = json.dumps({'password': config_values['password']})
    response = requests.post(LOGIN_URL, headers=HEADERS, data=login_data)
    response.raise_for_status()
    token = response.json()['token']

def get_live_info(instance_id):
    if token is None:
        login()
    headers_with_auth = HEADERS.copy()
    headers_with_auth['Authorization'] = f'Bearer {token}'
    response = requests.get(LIVE_INFO_URL.format(id=instance_id), headers=headers_with_auth)
    response.raise_for_status()
    return response.json()

def get_servers():
    if token is None:
        login()
    headers_with_auth = HEADERS.copy()
    headers_with_auth['Authorization'] = f'Bearer {token}'
    response = requests.get(SERVERS_URL, headers=headers_with_auth)
    response.raise_for_status()
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/live-info/<int:instance_id>')
def live_info(instance_id):
    try:
        data = get_live_info(instance_id)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/servers')
def servers():
    try:
        data = get_servers()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def refresh_token_periodically():
    login()
    Timer(3600, refresh_token_periodically).start()

if __name__ == '__main__':
    login()  # Initial login
    refresh_token_periodically()
    app.run(host='0.0.0.0', port=config_values['dash_port'])
