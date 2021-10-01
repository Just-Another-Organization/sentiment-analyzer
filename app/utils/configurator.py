from os import environ


def get_twitter_configurations():
    twitter_credentials = {
        'consumer_key': environ.get('CONSUMER_KEY'),
        'consumer_secret': environ.get('CONSUMER_SECRET'),
        'access_token': environ.get('ACCESS_TOKEN'),
        'access_token_secret': environ.get('ACCESS_TOKEN_SECRET')
    }

    return twitter_credentials
