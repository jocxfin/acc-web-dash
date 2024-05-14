import os

def get_config():
    return {
        'server_address': os.getenv('SERVER_ADDRESS', '192.168.178.75'),
        'server_port': os.getenv('SERVER_PORT', '8069'),
        'password': os.getenv('PASSWORD', 'default_password')
    }
