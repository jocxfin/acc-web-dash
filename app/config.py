import os

def get_config():
    return {
        'server_address': os.getenv('SERVER_ADDRESS', 'localhost'),
        'server_port': os.getenv('SERVER_PORT', '8080'),
        'password': os.getenv('PASSWORD', 'default_password')
    }
