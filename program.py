"""Program to add songs to spotify playlist."""
import os
import json
from typing import Tuple, List
import requests
from dotenv import load_dotenv

TOKEN = ""
PLAYLIST_ID = ""
SONGS = []


def does_song_exist(uri: str) -> bool:
    """This function checks if a song exists in the playlist

    Args:
        uri (str): song link

    Returns:
        bool: Returns a boolean if the song exists
    """

    for song in SONGS:
        song_uri = song["track"]["uri"]
        if song_uri == uri:
            return True
    return False


def add_song_to_playlist(song_uri: str) -> Tuple[str, bool]:
    """This function adds a song to the playlist

    Args:
        song_uri (str): song link

    Returns:
        Tuple[str, bool]: Returns a tuple with the status message and a boolean
    """

    url: str = (
        f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks?uris={song_uri}"
    )

    # print(url)

    headers: dict = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    # Check if song exsits
    if does_song_exist(song_uri):
        return "Song already exists", False

    res = requests.post(
        url,
        headers=headers,
        timeout=10,
    )

    # print(res.text)
    return "Song added to playlist", True
    # return "", True


def get_playlist_songs(playlist: str = PLAYLIST_ID) -> Tuple[List[str], bool]:
    """This function gets all the songs in the playlist

    Args:
        playlist (str): playlist id. Defaults to playlist_id.

    Returns:
        Tuple[str, bool]: _description_
    """

    # if playlist == "":
    #     if playlist_id == "":
    #         return "No playlist id found", False
    #     playlist = playlist_id

    url: str = f"https://api.spotify.com/v1/playlists/{playlist}/tracks?fields=items(track(name,uri))"

    headers: dict = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    song_list: List[str] = []

    res = requests.get(
        url,
        headers=headers,
        timeout=5,
    )

    song_list = json.loads(res.text)["items"]

    # print(songs[1]["track"]["name"])
    return song_list, True


def get_song(artists_list: List[str], title_og: str) -> Tuple[str, bool]:
    """This function gets a song from spotify

    Args:
        artists_list (List[str]): Song artists
        title_og (str): Song title

    Returns:
        Tuple[str, bool]: Returns a tuple with the status message and a boolean
    """

    title_og = title_og.strip()

    url: str = "https://api.spotify.com/v1/search?q="
    headers: dict = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    final_url: str = (
        f"{url} + track:{title_og} artist:{artists_list[0]}&type=track&limit=50"
    )

    res = requests.get(
        final_url,
        headers=headers,
        timeout=5,
    )

    res_json = json.loads(res.text)
    items = res_json["tracks"]["items"]
    if len(items) <= 0:
        final_url: str = f"{url} + track:{title_og}&type=track&limit=50"

        res = requests.get(final_url, headers, timeout=10)

        res_json = json.loads(res.text)
        items = res_json["tracks"]["items"]
        if len(items) <= 0:
            return "Song not found", False

    for item in items:
        artists = [artist["name"] for artist in item["artists"]]

        title = item["name"]
        for artist in artists:
            if artist.lower() in artists_list and title.lower() == title_og:
                print(f"Song title : {title}")
                song_id = item["uri"]
                print(f"Song uri : {song_id}")
                return song_id, True
    return f"Song not found - {title_og} - {artists}", False


def get_spotify_profile(api_token: str = TOKEN) -> bool:
    """This function gets the spotify profile of user with the token

    Args:
        api_token (str, optional): Api Token. Defaults to token.

    Returns:
        bool: Returns a boolean if the request was successful
    """
    url: str = "https://api.spotify.com/v1/me"

    headers: dict = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    res = requests.get(
        url,
        headers=headers,
        timeout=5,
    )

    print(res.json())
    if res.status_code == 200:
        return True
    return False


def format_entry(entry: str) -> Tuple[List[str], str]:
    """This function formats the song line from list.

    Args:
        entry (str): Takes one song line

    Returns:
        Tuple[List[str], str]: Returns a tuple with a list of artists and the song title
    """

    # Split the string by '-'
    splitting_char: str = " - "

    # Split the entry, take the frist line and split by ", " and make a list
    artists: List[str] = entry.split(splitting_char)[0].split(", ")
    # Convert all to lowercase
    artists = [artist.lower() for artist in artists]
    title: str = entry.split(splitting_char)[1]
    title = title.lower()

    return (artists, title)


def get_songs(file_name: str = "songs.txt") -> Tuple[str, bool]:
    """This function gets all the songs from the file

    Args:
        file_name (str, optional): Gets all songs from the text file. Defaults to "songs.txt".

    Returns:
        Tuple[str, bool]: Returns a tuple with the status message and a boolean
    """
    file = open(file_name, "r", encoding="utf-8")

    song_list: list = []

    # Read line by line

    song_list = file.readlines()

    file.close()

    if len(SONGS) <= 0:
        return "No songs found", False

    # Create a list of list of artists and song title
    list_of_entries: List(Tuple[List[str], str]) = []

    print("~~" * 10)
    for song in song_list:
        print(song)
        song_tuple = format_entry(song)
        list_of_entries.append(song_tuple)
        song_uri = get_song(song_tuple[0], song_tuple[1])
        # print(f"song uri : {song_uri}")
        res, _ = add_song_to_playlist(song_uri[0])
        print(res)
        print("~~" * 10)
        # print(song)
    return "Songs acquired", True


def main():
    """Main function"""
    load_dotenv()
    global TOKEN
    global PLAYLIST_ID
    TOKEN = os.environ.get("SPOTIFY_TOKEN")
    PLAYLIST_ID = os.environ.get("SPOTIFY_PLAYLIST_ID")

    global SONGS
    SONGS = get_playlist_songs()[0]
    # get_spotify_profile()

    get_songs()

    # add_song("changes", "xxxtentacion")


if "__main__" == __name__:
    main()
