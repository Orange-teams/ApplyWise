import requests

from config.settings import settings


HEADERS = {
    "User-Agent": settings.USER_AGENT
}


def get(url, params=None):
    response = requests.get(
        url,
        params=params,
        headers=HEADERS,
        timeout=settings.REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    return response