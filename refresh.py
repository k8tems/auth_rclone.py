import yaml
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session


def load_yaml(f_name):
    with open(f_name, 'r') as f:
        return yaml.safe_load(f.read())


if __name__ == '__main__':
    secrets = load_yaml('secrets.yaml')
    client_id = secrets['client_id']
    client_secret = secrets['client_secret']
    refresh_token = secrets['refresh_token']
    token_expiry = secrets['token_expiry']

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

    config = f"""[mygdrive]
type = drive
client_id = {client_id}
client_secret = {client_secret}
scope = drive
root_folder_id = 
service_account_file = 
token = {{"access_token":"{creds.token}","token_type":"Bearer","refresh_token":"{refresh_token}","expiry":"{token_expiry}"}}
"""
    with open('rclone.conf', 'w') as f:
        f.write(config)
