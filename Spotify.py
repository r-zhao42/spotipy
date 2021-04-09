"""
Using the Spotify API

"""
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# import playlist_link from user_input


client_credentials_manager = SpotifyClientCredentials(
    '6af4f7c48ecd43258dc10f18315e58ca', 'bf479de0603a41efb016107ce8148928')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

df = pd.read_csv('data.csv')
data_ids = set(df['id'])
track_features = {}

playlist_link = 'spotify:playlist:2gd9KJtjuFYVXH6zdSonxD'


def get_total_track_ids(playlist_link):
    """
    Given the user's playlist URI, return a list of track ids included in the playlist,
    excluding the tracks that do not exist in the dataset.
    """
    total_song_id_list = []
    playlist_id = playlist_link[17:]
    playlist = sp.playlist(playlist_id)
    for item in playlist['tracks']['items']:
        song_track = item['track']
        total_song_id_list.append(song_track['id'])
    return(total_song_id_list)


existing_track_ids = list(
    set(get_total_track_ids(playlist_link)).intersection(data_ids))
non_existing_track_ids = list(
    set(get_total_track_ids(playlist_link)).difference(data_ids))


def get_non_existing_track_features():
    """
    Return dictionary of track features, the keys represent 
    the track ids and the values are a list for each track's feature ordered in this fashion
    [acousticness, danceability, energy, duration_ms, instrumentalness, valence, temp, loudness, speechiness, key]
    """
    track_ids = non_existing_track_ids
    track_features = {key: [] for key in track_ids}
    for track_id in track_ids:
        features = sp.audio_features('spotify:track:' + track_id)
        track_features[track_id].extend([features[0]['acousticness'], features[0]['danceability'], features[0]['energy'],
                                         features[0]['duration_ms'], features[0]['instrumentalness'], features[0]['valence'], features[0]['tempo'],
                                         features[0]['loudness'], features[0]['speechiness'], features[0]['key']])

    return track_features

# print(get_total_track_ids(playlist_link))
# print(len(get_total_track_ids(playlist_link)))

# print(existing_track_ids)
# print(len(existing_track_ids))

# print(non_existing_track_ids)
# print(len(non_existing_track_ids))

# print(get_non_existing_track_features())
