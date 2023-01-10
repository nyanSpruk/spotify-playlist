import os
from dotenv import load_dotenv
import requests
from typing import Tuple, Dict, List
import json


def does_song_exist(uri: str) -> bool:
    for song in songs:
        song_uri = song["track"]["uri"]
        if song_uri == uri:
            return True
    return False


def add_song_to_playlist(song_uri: str) -> Tuple[str, bool]:
    url: str = (
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={song_uri}"
    )

    # print(url)

    headers: dict = {
        "Authorization": f"Bearer " + token,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    # Check if song exsits
    if does_song_exist(song_uri):
        return "Song already exists", False

    res = requests.post(
        url,
        headers=headers,
    )

    # print(res.text)
    return "Song added to playlist", True
    # return "", True


def get_playlist_songs() -> Tuple[str, bool]:
    url: str = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?fields=items(track(name,uri))"

    headers: dict = {
        "Authorization": f"Bearer " + token,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    songs: List[str] = []

    res = requests.get(
        url,
        headers=headers,
    )

    songs = json.loads(res.text)["items"]

    # print(songs[1]["track"]["name"])
    return songs, True


def get_song(artists_list: List[str], title: str) -> Tuple[str, bool]:
    url: str = "https://api.spotify.com/v1/search?q="
    headers: dict = {
        "Authorization": f"Bearer " + token,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    finalUrl: str = (
        f"{url} + track:{title} artist:{artists_list[0]}&type=track&limit=50"
    )

    res = requests.get(
        finalUrl,
        headers=headers,
    )

    res_json = json.loads(res.text)
    items = res_json["tracks"]["items"]
    if len(items) <= 0:
        finalUrl: str = f"{url} + track:{title}&type=track&limit=50"

        res = requests.get(finalUrl, headers)

        res_json = json.loads(res.text)
        items = res_json["tracks"]["items"]
        if len(items) <= 0:
            return "Song not found", False

    for item in items:
        artists = [artist["name"] for artist in item["artists"]]

        title = item["name"]
        for artist in artists:
            if artist.lower() in artists_list:
                song_id = item["uri"]
                print(f"Song uri : {song_id}")
                return song_id, True
    return "Song not found", False


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


def format_entry(entry: str) -> Tuple[List[str], str]:
    # Split the string by '-'
    splitting_char: str = " - "

    # Split the entry, take the frist line and split by ", " and make a list
    artists: List[str] = entry.split(splitting_char)[0].split(", ")
    # Convert all to lowercase
    artists = [artist.lower() for artist in artists]
    title: str = entry.split(splitting_char)[1]
    title = title.lower()

    return (artists, title)


def get_songs() -> Tuple[str, bool]:
    file_name: str = "songs.txt"

    file = open(file_name, "r")

    songs: list = []

    # Read line by line

    songs = file.readlines()

    if len(songs) <= 0:
        return "No songs found", False

    # Create a list of list of artists and song title
    list_of_entries: List(Tuple[List[str], str]) = []

    print("~~" * 10)
    for song in songs:
        print(song)
        song_tuple = format_entry(song)
        list_of_entries.append(song_tuple)
        song_uri = get_song(song_tuple[0], song_tuple[1])
        # print(f"song uri : {song_uri}")
        res, isSucc = add_song_to_playlist(song_uri[0])
        print(res)
        print("~~" * 10)
        # print(song)


def main():
    load_dotenv()
    global token
    global playlist_id
    token = os.environ.get("SPOTIFY_TOKEN")
    playlist_id = os.environ.get("SPOTIFY_PLAYLIST_ID")

    global songs
    songs = get_playlist_songs()[0]
    # get_spotify_profile()

    get_songs()

    # add_song("changes", "xxxtentacion")


if "__main__" == __name__:
    main()
