import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
import configparser
from config import RCloneConfig


if __name__ == '__main__':
    configparser.ConfigParser()
    in_f_name = sys.argv[1]
    out_f_name = sys.argv[2]
    config = RCloneConfig.open(in_f_name)

    client_id = config.client_id
    client_secret = config.client_secret
    refresh_token = config.refresh_token
    token_expiry = config.expiry

    auth = HTTPBasicAuth(client_id, client_secret)
    client = BackendApplicationClient(client_id=client_id)

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

    with open(out_f_name, 'w') as f:
        config.update_token(f, creds.token)
