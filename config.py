import configparser
import json


class RCloneConfig:
    def __init__(self, config):
        self.config = config

    @classmethod
    def open(cls, f_name):
        parser = configparser.ConfigParser()
        parser.read(f_name)
        return RCloneConfig(parser)

    def __getattr__(self, name):
        if name in ['client_id', 'client_secret']:
            return self.config['mygdrive'][name]
        elif name in ['refresh_token', 'expiry']:
            return self.token_info[name]
        raise AttributeError()

    @property
    def token_info(self):
        return json.loads(self.config['mygdrive']['token'])

    def update_token(self, f, token):
        token_info = self.token_info
        token_info['access_token'] = token
        self.config['mygdrive']['token'] = json.dumps(token_info)
        self.config.write(f)
