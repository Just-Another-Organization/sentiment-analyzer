import os
from os import environ


class Configurator:

    def __init__(self):
        self.twitter_credentials = {
            'CONSUMER_KEY': environ.get('CONSUMER_KEY'),
            'CONSUMER_KEY_SECRET': environ.get('CONSUMER_KEY_SECRET'),
            'BEARER_TOKEN': environ.get('BEARER_TOKEN'),
            'ACCESS_TOKEN': environ.get('ACCESS_TOKEN'),
            'ACCESS_TOKEN_SECRET': environ.get('ACCESS_TOKEN_SECRET'),
            'LABEL_30_DAY': environ.get('LABEL_30_DAY'),
            'LABEL_FULL_ARCHIVE': environ.get('LABEL_FULL_ARCHIVE'),
            'USE_USER_CONTEXT': environ.get('USE_USER_CONTEXT') == 'True',
        }
        self._api_key = os.environ.get('API_KEY')
        self._api_key_header = os.environ.get('API_KEY_HEADER')

    def get_twitter_configurations(self):
        return self.twitter_credentials

    def get_api_key(self):
        return self._api_key

    def get_api_key_header(self):
        return self._api_key_header
