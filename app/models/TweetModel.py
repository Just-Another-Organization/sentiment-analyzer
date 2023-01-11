from tweepy import Tweet


class TweetModel:
    def __init__(self, raw_tweet: Tweet):
        self.created_at = raw_tweet.created_at
        self.text = raw_tweet.text
        self.id = raw_tweet.id
        self.quote_count = 0 if not hasattr(raw_tweet, 'quote_count') is None else raw_tweet.quote_count
        self.reply_count = 0 if not hasattr(raw_tweet, 'reply_count') is None else raw_tweet.reply_count
        self.retweet_count = 0 if not hasattr(raw_tweet, 'retweet_count') is None else raw_tweet.retweet_count
        self.favorite_count = 0 if not hasattr(raw_tweet, 'favorite_count') is None else raw_tweet.favorite_count
