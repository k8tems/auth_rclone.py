import yaml
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
import configparser


def load_yaml(f_name):
    with open(f_name, 'r') as f:
        return yaml.safe_load(f.read())


class RCloneConfig:
    def __init__(self, f_name, config):
        self.f_name = f_name
        self.config = config

    @classmethod
    def open(cls, f_name):
        parser = configparser.ConfigParser()
        parser.read(f_name)
        return RCloneConfig(f_name, parser)

    def __getattr__(self, name):
        if name in ['client_id', 'client_secret']:
            return self.config['mygdrive'][name]
        elif name in ['refresh_token', 'expiry']:
            return json.loads(self.config['mygdrive']['token'])[name]
        raise AttributeError()

    def update_token(self, token):
        token_info = json.loads(self.config['mygdrive']['token'])
        token_info['access_token'] = token
        self.config['mygdrive'] = json.dumps(token_info)
        with open(self.f_name, 'w') as f:
            self.config.write(f)


if __name__ == '__main__':
    configparser.ConfigParser()
    config = RCloneConfig.open('rclone.conf')

    secrets = load_yaml('secrets.yaml')
    client_id = config.client_id
    client_secret = config.client_secret
    refresh_token = config.refresh_token
    token_expiry = config.expiry

    auth = HTTPBasicAuth(client_id, client_secret)
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)

    oauth = OAuth2Session(client_id, redirect_uri='http://127.0.0.1:53682/',
                          scope=["https://www.googleapis.com/auth/drive"])

    creds = Credentials.from_authorized_user_info(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
        }
    )

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    config.update_token(creds.token)
