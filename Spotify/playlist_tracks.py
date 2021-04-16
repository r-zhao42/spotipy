"""
Using the Spotify API in this file we get the song features/attributes of songs that are not
already in our database

AND... # TODO **************************************************************************************

"""
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Validating Spotify credentials to use API
client_credentials_manager = SpotifyClientCredentials(
    'daf1fbca87e94c9db377c98570e32ece', '1a674398d1bb44859ccaa4488df1aaa9')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Reading the csv file!
df = pd.read_csv('data.csv')
data_ids = set(df['id'])
track_features = {}


def get_total_track_ids(playlist_link: ...) -> list:  # TODO****************************************
    """
    Given the user's playlist URI, return a list of track ids included in the playlist.
    """
    total_song_id_list = []
    playlist_id = parse_link_to_id(playlist_link)
    playlist = sp.playlist(playlist_id)
    for item in playlist['tracks']['items']:
        song_track = item['track']
        total_song_id_list.append(song_track['id'])

    return total_song_id_list


def get_non_existing_track_features(playlist_link: ...) -> dict:  # TODO****************************
    """
    Return dictionary of track features, the keys represent
    the track ids and the values are a list for each track's feature ordered in this fashion
    [acousticness, danceability, energy, duration_ms, instrumentalness, valence, tempo, liveliness,
     loudness, speechiness, key]
    """
    track_ids = get_total_track_ids(playlist_link)
    track_features = {key: [] for key in track_ids}
    for track_id in track_ids:
        features = sp.audio_features('spotify:track:' + track_id)
        track_features[track_id].extend([features[0]['acousticness'], features[0]['danceability'], features[0]['energy'],
                                         features[0]['duration_ms'], features[0]['instrumentalness'], features[
                                             0]['valence'], features[0]['tempo'], features[0]['liveness'],
                                         features[0]['loudness'], features[0]['speechiness'], features[0]['key']])

    return track_features


def parse_link_to_id(playlist_link: ...) -> str:  # TODO********************************************
    """
    Responsible for...
    Returns...

    """
    split_url = playlist_link.split('/')
    splitted = split_url[4]
    split_again = splitted.split('?')
    playlist_id = split_again[0]
    print(playlist_id)
    return playlist_id


def get_existing_track_ids(playlist_link: ...) -> list:  # TODO************************************
    """
    Responsible for...
    Returns...

    """

    return list(
        set(get_total_track_ids(playlist_link)).intersection(data_ids))


def get_non_existing_track_ids(playlist_link: ...) -> list:  # TODO*********************************
    """
    Responsible for...

    Returns...


    """

    return list(
        set(get_total_track_ids(playlist_link)).difference(data_ids))
