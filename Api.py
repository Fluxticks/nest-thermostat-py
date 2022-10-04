from Auth import Auth
import aiohttp


class Api:

    __slots__ = "_auth"

    def __init__(self, auth: Auth):
        self._auth = auth

    @property
    def project_id(self):
        return self._auth.project_id

    async def get_session_auth(self):
        session_token = self._auth.get_access_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session_token}",
        }
        return session_token, headers

    async def get_devices(self):
        DEVICES_URL = f"https://smartdevicemanagement.googleapis.com/v1/enterprises/{self._auth.project_id}/devices"
        _, headers = await self.get_session_auth()
        async with aiohttp.ClientSession() as session:
            async with session.get(DEVICES_URL, headers=headers) as resp:
                if resp.status != 200:
                    raise ValueError(
                        "Unable to access device list with given credentials"
                    )
                else:
                    return await resp.json().get("devices")

    async def get_exact_device(self, device_id: str):
        DEVICE_URL = f"https://smartdevicemanagement.googleapis.com/v1/enterprises/{self._auth.project_id}/devices/{device_id}"
        _, headers = await self.get_session_auth()
        async with aiohttp.ClientSession() as session:
            async with session.get(DEVICE_URL, headers=headers) as resp:
                if resp.status != 200:
                    raise ValueError(
                        f"Unable to access device with ID {device_id}. Could be incorrect credentials or device ID"
                    )
                else:
                    return await resp.json()

    async def post_command(self, device_id: str, command: str, params: dict):
        COMMAND_URL = f"https://smartdevicemanagement.googleapis.com/v1/enterprises/{self.project_id}/{device_id}:executeCommand"
        data = {"command": command, "params": params}
        _, headers = await self.get_session_auth()

        async with aiohttp.ClientSession() as session:
            async with session.post(COMMAND_URL, headers=headers, data=data) as resp:
                if resp.status != 200:
                    raise ValueError(
                        f"Unable to post command to device with ID {device_id}. Could be incorrect credentials or device ID"
                    )
                else:
                    return True
