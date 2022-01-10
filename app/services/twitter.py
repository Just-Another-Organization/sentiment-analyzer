from utils.configurator import get_twitter_configurations
from utils.logger import Logger


class Twitter:
    def __init__(self):
        self.logger = Logger('Twitter')
        self.configurations = get_twitter_configurations()
        self.logger.info(self.configurations)
