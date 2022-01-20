from datetime import datetime

from slowapi import Limiter
from slowapi.util import get_remote_address

import utils.constants as constants
import utils.utilities as utilities
from utils.singleton import Singleton


@Singleton
class RequestLimiter:
    API_REQUEST_WINDOW_INTERVAL = utilities.get_interval_by_string(constants.API_REQUESTS_WINDOW)

    def __init__(self):
        self.limiter = Limiter(key_func=get_remote_address)
        self.api_requests_number = 0
        self.api_last_check_timestamp = datetime.now()

    def api_limit_not_reached(self, new_api_requests_number):
        self.check_request_window()
        if self.api_requests_number + new_api_requests_number > constants.API_REQUESTS_LIMIT:
            return False
        else:
            self.check_request_window()
            self.api_requests_number += new_api_requests_number
            return True

    def check_request_window(self):
        now = datetime.now()
        if int((now - self.api_last_check_timestamp).total_seconds()) >= self.API_REQUEST_WINDOW_INTERVAL:
            self.api_requests_number = 0
            self.api_last_check_timestamp = now
