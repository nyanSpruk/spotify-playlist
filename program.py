import os
from dotenv import load_dotenv
import requests


def get_spotify_profile() -> bool:
    url = "https://api.spotify.com/v1/me"

    headers = {
        "Authorization": f"Bearer " + token,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    res = requests.get(
        url,
        headers=headers,
    )
    print(res.json())
    if res.status_code == 200:
        return True
    else:
        return False


def add_song(song: str, artist: str) -> bool:
    return True


def main():
    load_dotenv()
    global token
    token = os.environ.get("SPOTIFY_TOKEN")
    add_song("changes", "xxxtentacion")
    get_spotify_profile()


if "__main__" == __name__:
    main()
