# spotify-sorter

Filters songs in a given playlist based on genre and adds them to a newly created playlist.

## Setup

Install requirements with ```pip install -r requirements.txt```.

## Usage

Get your application values from: https://developer.spotify.com/dashboard/applications.

Start tool with:

```python sorter.py --username --client_id --client_secret --playlist_name --genres```

```--genres``` is a string list seperated by ```,```. Example: ```--genres "dnb,drum and bass,bass"```

Follow instructions in terminal.


## References

https://spotipy.readthedocs.io

https://developer.spotify.com/documentation/web-api/reference/search/search/

https://developer.spotify.com/console/post-playlists/

https://developer.spotify.com/documentation/web-api/reference/playlists/add-tracks-to-playlist/

https://developer.spotify.com/console/get-available-genre-seeds/

https://developer.spotify.com/console/get-artist/
