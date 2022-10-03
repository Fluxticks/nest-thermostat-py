from time import time
import aiohttp


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
        self._next_refresh = None
        self._client_id = client_id
        self._client_secret = client_secret

    async def get_access_token(self):
        if time() < self._next_refresh:
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
                    raise ValueError(
                        "Unable to reauthorize and grant new access token!"
                    )
                else:
                    data = await resp.json()
                    self._access_token = data.get("access_token")
                    self._next_refresh = time() + data.get("expires_in")
        return self._access_token

    async def get_devices(self):
        session_token = await self.get_access_token()
        DEVICES_URL = f"https://smartdevicemanagement.googleapis.com/v1/enterprises/{self._project_id}/devices"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session_token}",
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(DEVICES_URL, headers=headers) as resp:
                if resp.status != 200:
                    raise ValueError(
                        "Unable to access device list with given credentials"
                    )
                else:
                    return await resp.json().get("structures")
