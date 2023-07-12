from aiohttp import ClientSession
from fake_headers import Headers
from config import BASE_URL


class Client:
    GET_ACTIVE_WATCHERS_URL = BASE_URL + "/api/getchatuserlist/"

    @staticmethod
    async def get_active_watchers(model_name: str) -> list[str]:
        params = {
            "roomname": model_name,
            "private": "false",
            "sort_by": "a",
            "exclude_staff": "true",
        }
        async with ClientSession(headers=Client._generate_headers()) as session:
            async with session.get(
                    Client.GET_ACTIVE_WATCHERS_URL, params=params
            ) as response:
                raw_users = (await response.text()).split(",")
        return Client._exclude_users(raw_users)

    @staticmethod
    def _exclude_users(raw_users: list[str]) -> list[str]:
        ret_users = []
        for user in raw_users:
            try:
                username, status, _, _ = user.split("|")
            except:  # Первая строка - число анонимных юзеров, пропускаем
                continue
            if status != "g":
                ret_users.append(username)
        return ret_users

    @staticmethod
    def _generate_headers() -> dict[str, str]:
        return Headers(browser="chrome", os="win").generate()


client = Client()
