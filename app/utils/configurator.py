from os import environ


def get_twitter_configurations():
    twitter_credentials = {
        'CONSUMER_KEY': environ.get('CONSUMER_KEY'),
        'CONSUMER_KEY_SECRET': environ.get('CONSUMER_KEY_SECRET'),
        'BEARER_TOKEN': environ.get('BEARER_TOKEN'),
        'ACCESS_TOKEN': environ.get('ACCESS_TOKEN'),
        'ACCESS_TOKEN_SECRET': environ.get('ACCESS_TOKEN_SECRET'),
    }

    return twitter_credentials
