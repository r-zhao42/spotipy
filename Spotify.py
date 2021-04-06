import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials('6af4f7c48ecd43258dc10f18315e58ca', 'bf479de0603a41efb016107ce8148928')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_track_ids(playlist_id):
    music_id_list = []
    playlist = sp.playlist(playlist_id)
    for item in playlist['tracks']['items']:
        music_track = item['track']
        music_id_list.append(music_track['id'])
    return music_id_list

playlist_id = '1nrmeYg6bEo34nxHgaid1u'
track_ids = get_track_ids(playlist_id)
print(track_ids)