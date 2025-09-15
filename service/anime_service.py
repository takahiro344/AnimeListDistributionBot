from datetime import datetime

import httpx

from model.anime_dto import AnimeDto


class AnimeService:
    def __init__(self, api_url, access_token):
        self.api_url = api_url
        self.access_token = access_token

    def fetch_current_season_anime(self):
        if not self.access_token:
            raise ValueError(
                "ANNICT_ACCESS_TOKEN is not set in environment variables.")

        if not self.api_url:
            raise ValueError(
                "ANNICT_API_URL is not set in environment variables.")

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        current_season_anime_list = []

        page = 1
        while True:
            params = {
                "fields": "title,official_site_url",
                "filter_season": _get_current_season(),
                "filter_media": "tv",
                "page": page,
                "per_page": 50
            }

            with httpx.Client() as client:
                response = client.get(
                    self.api_url,
                    headers=headers,
                    params=params)
                response.raise_for_status()
                current_season_anime_list_per_page = response.json()["works"]
                if not current_season_anime_list_per_page:
                    break
                current_season_anime_list.extend(
                    current_season_anime_list_per_page)
                page += 1

        return _to_anime_dto(current_season_anime_list)


def _get_current_season():
    now = datetime.now()
    if now.month in [1, 2, 3]:
        season = "winter"
    elif now.month in [4, 5, 6]:
        season = "spring"
    elif now.month in [7, 8, 9]:
        season = "summer"
    elif now.month in [10, 11, 12]:
        season = "autumn"
    else:
        return None

    return f"{now.year}-{season}"


def _to_anime_dto(anime_list) -> list[AnimeDto]:
    anime_dto_list: list[AnimeDto] = []

    for anime in anime_list:
        anime_dto_list.append(
            AnimeDto(
                title=anime.get("title"),
                official_site_url=anime.get("official_site_url")
            )
        )

    return anime_dto_list
