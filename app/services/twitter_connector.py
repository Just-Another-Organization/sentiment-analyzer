from utils.configurator import get_twitter_configurations


class Twitter:
    def __init__(self):
        self.configurations = get_twitter_configurations()
        print(self.configurations)

