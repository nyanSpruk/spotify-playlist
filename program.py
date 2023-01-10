import os
from dotenv import load_dotenv
import requests


def get_spotify_profile() -> bool:
    url: str = "https://api.spotify.com/v1/me"

    headers: dict = {
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


def get_songs() -> str:
    file_name: str = "songs.txt"


def add_song(song: str, artist: str) -> bool:
    return True


def main():
    load_dotenv()
    global token
    token = os.environ.get("SPOTIFY_TOKEN")

    # get_spotify_profile()

    add_song("changes", "xxxtentacion")


if "__main__" == __name__:
    main()
