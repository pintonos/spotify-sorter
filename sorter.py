import spotipy
import argparse
import tqdm

import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth


def get_all_saved_tracks(sp, limit_step=50):
    tracks = []
    for offset in tqdm.trange(0, 10000, limit_step):
        response = sp.current_user_saved_tracks(
            limit=limit_step,
            offset=offset,
        )
        if len(response) == 0:
            break
        tracks.extend(response['items'])
    return tracks


scope = 'playlist-modify-public playlist-modify-private user-library-read'

parser = argparse.ArgumentParser()
parser.add_argument('--username', type=str, required=True)
parser.add_argument('--client_id', type=str, required=True)
parser.add_argument('--client_secret', type=str, required=True)
parser.add_argument('--playlist_name', type=str, default="spotify-sorter")
parser.add_argument('--genres', type=str, required=True)
parser.add_argument('--debug', type=bool, default=False)

args = parser.parse_args()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                                                username=args.username,
                                                scope=scope, 
                                                client_id=args.client_id,  
                                                client_secret=args.client_secret,
                                                redirect_uri='http://localhost/'))

create_playlist = sp.user_playlist_create(args.username, args.playlist_name, public=False,
                                    description=f'Playlist created by spotify-sorter with following genres: {args.genres}')

genres = args.genres.split(',')
track_ids = []
saved_tracks = get_all_saved_tracks(sp, limit_step=50)
for item in tqdm.tqdm(saved_tracks):
    track = item['track']
    artist_id = track['artists'][0]['id']
    artist = sp.artist(artist_id=artist_id)
    artist_genres = artist['genres']
    for genre in genres:
        if next((s for s in artist_genres if genre in s), None):
            track_ids.append(track['id'])
            break

    if len(track_ids) == 99:
        # add tracks to playlist
        results = sp.user_playlist_add_tracks(args.username, create_playlist['id'], track_ids) # can add maxium 100 tracks per request
        track_ids = []

# final add tracks to playlist
if len(track_ids) > 0:
    results = sp.user_playlist_add_tracks(args.username, create_playlist['id'], track_ids)

if args.debug:
    sp.user_playlist_unfollow(args.username, create_playlist['id'])
