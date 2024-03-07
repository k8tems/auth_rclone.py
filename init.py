import os
import sys
from google_auth_oauthlib.flow import Flow
import refresh


redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
scopes = ['https://www.googleapis.com/auth/drive']


def auth(client_id, client_secret):
    flow = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=scopes,
        redirect_uri=redirect_uri
    )
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    print("Please go to this URL and authorize access:")
    print(auth_url)
    code = input('Code: ')
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    flow.fetch_token(code=code)  # Use the provided code to fetch the token
    print("Access Token:", flow.credentials.token)
    print("Refresh Token:", flow.credentials.refresh_token)


if __name__ == '__main__':
    config = refresh.RCloneConfig.open(sys.argv[1])
    auth(config.client_id, config.client_secret)
