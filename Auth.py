from time import time
from typing import Coroutine, Tuple
import aiohttp


class ResponseCode(Exception):
    def __init__(self, code: int, error: dict, *args: object) -> None:
        super().__init__(*args)
        self.code = code
        if isinstance(error.get("error"), dict):
            self.status = error.get("error").get("status")
            self.message = error.get("error").get("message")
        else:
            self.status = error.get("error")
            self.message = error.get("error_description")

    def __str__(self):
        return f"{self.code} - {self.status} : {self.message}"


async def call_handler(api_call: dict) -> Tuple[bool, str]:
    # api_call : {"function": Coroutine, "args": [], "kwargs": {}}
    function: Coroutine = api_call.get("function")
    args = api_call.get("args", [])
    kwargs = api_call.get("kwargs", {})
    try:
        result = await function(*args, **kwargs)
        return result, "success"
    except ResponseCode as e:
        return False, e.message


class Auth:
    __slots__ = (
        "_project_id",
        "_access_token",
        "_refresh_token",
        "_next_refresh",
        "_client_id",
        "_client_secret",
    )

    def __init__(
        self,
        project_id: str,
        access_token: str,
        refresh_token: str,
        client_id: str,
        client_secret: str,
    ):
        self._project_id = project_id
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._next_refresh = 0
        self._client_id = client_id
        self._client_secret = client_secret

    async def get_access_token(self):
        if self._access_token is not None and time() < self._next_refresh:
            return self._access_token

        REAUTH_URL = f"https://www.googleapis.com/oauth2/v4/token"
        params = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "refresh_token": self._refresh_token,
            "grant_type": "refresh_token",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(REAUTH_URL, params=params) as resp:
                if resp.status != 200:
                    raise ResponseCode(resp.status, error=await resp.json())
                else:
                    data = await resp.json()
                    self._access_token = data.get("access_token")
                    self._next_refresh = time() + data.get("expires_in")
        return self._access_token

    @property
    def project_id(self):
        return self._project_id
