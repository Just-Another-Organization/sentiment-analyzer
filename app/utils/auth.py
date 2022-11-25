from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette import status

from utils.configurator import Configurator
from utils.logger import Logger


class Auth:
    api_key_header = APIKeyHeader(name=Configurator().get_api_key_header(), auto_error=False)

    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
        self.configurator = Configurator()

    def api_key_auth(self, api_key: str = Security(api_key_header)):
        if api_key != self.configurator.get_api_key():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Forbidden"
            )
