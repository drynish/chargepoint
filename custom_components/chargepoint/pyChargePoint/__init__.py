import aiohttp
import asyncio
import uuid


class API:
    """API pour se connecter à chargepoint"""

    def __init__(
        self,
        api_token: str,
        user_id: int,
    ):
        self.api_token = api_token
        self.uuid = str(uuid.uuid4()).upper()
        self.user_id = user_id

    async def action(self, type, session):
        """ type should be a string: startsession or stopSession """

        data = await self.info(session)

        url = f"https://account-ca.chargepoint.com/account/v1/driver/station/{type}"

        data = {
            "deviceData": {
                "manufacturer": "Apple",
                "model": "iPhone",
                "type": "IOS",
                "udid": self.uuid,
                "version": "5.73.0"
            },
            "deviceId": data["charging_status"]["device_id"],
            "portNumber": 1,
            "sessionId": data["charging_status"]["session_id"]
        }

        headers = {
            "CP-Session-Token": self.api_token,
            "Content-Type": "application/json",
            "Cookies": f"coulomb_sess={self.api_token}"
        }

        async with session.post(url, json=data, headers=headers) as resp:
            result = await resp.json()

        return result

    async def info(self, session):
        result = ""

        url = 'https://mc-ca.chargepoint.com/map-prod/v2'

        data = {
            "deviceData": {
                "manufacturer": "Apple",
                "model": "iPhone",
                "type": "IOS",
                "udid": self.uuid,
                "version": "5.73.0"
            },
            "charging_status": {
                "mfhs": {}
            },
            "user_id": self.user_id
        }

        headers = {
            "CP-Session-Token": self.api_token,
            "Content-Type": "application/json",
            "Cookies": f"coulomb_sess={self.api_token}"
        }

        async with session.post(url, json=data, headers=headers) as resp:
            result = await resp.json()

        return result
