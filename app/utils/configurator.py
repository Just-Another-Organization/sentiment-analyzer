from os import environ


def get_twitter_configurations():
    twitter_credentials = {
        'API_KEY': environ.get('API_KEY'),
        'API_KEY_SECRET': environ.get('API_KEY_SECRET'),
        'BEARER_TOKEN': environ.get('BEARER_TOKEN'),
    }

    return twitter_credentials
