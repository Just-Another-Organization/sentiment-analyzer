from slowapi import Limiter
from slowapi.util import get_remote_address

from utils.singleton import Singleton


@Singleton
class RequestLimiter:
    def __init__(self):
        self.limiter = Limiter(key_func=get_remote_address)
