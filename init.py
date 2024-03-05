import sys
from google_auth_oauthlib.flow import Flow
import refresh


redirect_uri = 'http://localhost:8080/'
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

    # TODO: コードをコピーして貼り付ける形式にするにはどうすればいい？
    auth_url, _ = flow.authorization_url(prompt='consent')

    print("Please go to this URL and authorize access:")
    print(auth_url)
    print("After authorizing, you will be redirected to a URL with a 'code' parameter.")
    print("Paste the full redirected URL here:")

    redirected_url = input()
    import os

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    flow.fetch_token(authorization_response=redirected_url)

    print("Access Token:", flow.credentials.token)
    print("Refresh Token:", flow.credentials.refresh_token)


if __name__ == '__main__':
    config = refresh.RCloneConfig.open(sys.argv[1])
    auth(config.client_id, config.client_secret)
