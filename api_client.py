import asyncio

from aiohttp import ClientSession
from fake_headers import Headers


class Client:
    def __init__(self):
        BASE_URL = "https://www.youtucam.com"
        self.GET_ACTIVE_WATCHERS_URL = BASE_URL + "/api/getchatuserlist/"

    async def get_active_watchers(self, model_name: str) -> list[str]:
        params = {
            "roomname": model_name,
            "private": "false",
            "sort_by": "a",
            "exclude_staff": "true",
        }
        async with ClientSession(headers=self._generate_headers()) as session:
            async with session.get(
                    self.GET_ACTIVE_WATCHERS_URL, params=params
            ) as response:
                raw_users = (await response.text()).split(",")
                print(await response.text())
        return self._exclude_users(raw_users)

    def _exclude_users(self, raw_users: list[str]) -> list[str]:
        ret_users = []
        for user in raw_users:
            try:
                username, status, _, _ = user.split("|")
            except:  # Первая строка - число анонимных юзеров, пропускаем
                continue
            if status != "g":
                ret_users.append(username)
        return ret_users

    def _generate_headers(self) -> dict[str, str]:
        return Headers(browser="chrome", os="win").generate()


client = Client()
