"""
CSC111 Final Project: Playlist Generator

Module Description
==================

This is the file to deal with the Spotify Client.
Here we regenerate the Spotify API Authorization Token

In this file we also create a new playlist and add new songs to it


Copyright and Usage Information
===============================

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

This file is Copyright (c) 2021 Si Yuan Zhao, Hayk Nazaryan, Cliff Zhang, Joanne Pan.
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
    Given the user's playlist URL, return a list of track ids included in the playlist.
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
        track_features[track_id].extend([features[0]['acousticness'],
                                         features[0]['danceability'],
                                         features[0]['energy'],
                                         features[0]['duration_ms'],
                                         features[0]['instrumentalness'],
                                         features[0]['valence'],
                                         features[0]['tempo'],
                                         features[0]['liveness'],
                                         features[0]['loudness'],
                                         features[0]['speechiness'],
                                         features[0]['key']])

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


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['pickle', 'tkinter', 'PIL', 'urllib', 'webbrowser',
                          'Recommendation', 'Spotify.Spotify_client', 'Spotify.song_features',
                          'k_means', 'spotipy', 'argparse', 'song_tkinter', 'preprocess',
                          'post_cluster', 'json', 'Track', 'Playlist', 'requests',
                          'spotipy.oauth2', 'spotipy.util', 'pandas'],
        'allowed-io': ['parse_link_to_id'],
        # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
