# spotify-playlist
Add songs to spotify playlist

<!-- USAGE -->
## Getting Started
Create .env file with the following variables:
```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```
Example can be found in `.env_example`

Create a `songs.txt` file with the songs you want to add to the playlist. Each song should be in a new line and in the following format:
```txt
Artist - Song
```
Example can be found in `songs.example.txt`

To run the script:
```python
python3 program.py
```

If the token is correct, it will list all the playlists you have and ask you to choose one.

The program will then add the songs to the playlist.

Any song that was not found will be added to a `not_found.txt` file.


### Disclaimer
This is a personal project and is not affiliated with Spotify in any way.
