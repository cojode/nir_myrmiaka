import aiohttp
from bs4 import BeautifulSoup


class GroupParser:
    __resource = "https://home.mephi.ru/study_groups"
    target_element = "a"
    target_attrs = {"class": "list-group-item text-center text-nowrap"}

    def __init__(self, current_term: str | None = None):
        self.current_term = current_term

    async def get_groups(self, level: int = 0):
        params = {}
        if level != 0:
            params["level"] = level

        async with aiohttp.ClientSession() as client:
            response = await client.get(self.__resource, params=params)
            if response.status == 200:

                actual_current_term = str(
                    response.url.query.get("term_id", "")
                )

                if actual_current_term == self.current_term:
                    return None, None

                soup = BeautifulSoup(
                    await response.text(), features="html.parser"
                )
                return actual_current_term, [
                    item.contents[0].strip()
                    for item in soup.find_all(
                        self.target_element, attrs=self.target_attrs
                    )
                ]
