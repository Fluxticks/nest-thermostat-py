from Auth import Auth
import aiohttp


class Api:

    __slots__ = "_auth"

    def __init__(self, auth: Auth):
        self._auth = auth

    async def get_devices(self):
        session_token = await self._auth.get_access_token()
        DEVICES_URL = f"https://smartdevicemanagement.googleapis.com/v1/enterprises/{self._auth.project_id}/devices"
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
                    return await resp.json().get("devices")

    async def get_exact_device(self, device_id: str):
        session_token = await self._auth.get_access_token()
        DEVICE_URL = f"https://smartdevicemanagement.googleapis.com/v1/enterprises/{self._auth.project_id}/devices/{device_id}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session_token}",
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(DEVICE_URL, headers) as resp:
                if resp.status != 200:
                    raise ValueError(
                        f"Unable to access device with ID {device_id}. Could be incorrect credentials or device ID"
                    )
                else:
                    return await resp.json()
