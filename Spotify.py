"""
Taking the user inputed playlist link to generate an array of track ids using spotipy (Spotify's API) and
discarding the tracks that do not exist in our dataset.
"""
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# import playlist_link from user_input


client_credentials_manager = SpotifyClientCredentials(
    '6af4f7c48ecd43258dc10f18315e58ca', 'bf479de0603a41efb016107ce8148928')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

df = pd.read_csv('data.csv')
ids = set(df['id'])

playlist_link = 'spotify:playlist:2MaKHEugScv6B9QUPIewYP'

def get_track_ids(playlist_link):
    playlist_id = playlist_link[17:]
    song_id_list = []
    playlist = sp.playlist(playlist_id)
    for item in playlist['tracks']['items']:
        song_track = item['track']
        song_id_list.append(song_track['id'])
    return(list(remove_non_existing_songs(song_id_list)))


def remove_non_existing_songs(song_id_list):
    return(set(song_id_list).intersection(ids))

print(get_track_ids(playlist_link))
print(len(get_track_ids(playlist_link)))