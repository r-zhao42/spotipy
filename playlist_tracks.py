"""
Using the Spotify API

"""
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# import playlist_link from user_input


client_credentials_manager = SpotifyClientCredentials(
    'daf1fbca87e94c9db377c98570e32ece', '1a674398d1bb44859ccaa4488df1aaa9')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

df = pd.read_csv('data.csv')
data_ids = set(df['id'])
track_features = {}

playlist_link = 'https://open.spotify.com/playlist/1X2xbG50zdeAv5hAnTvbJU?si=648799b58b7e4e13'


def get_total_track_ids(playlist_link) -> list:
    """
    Given the user's playlist URI, return a list of track ids included in the playlist,
    excluding the tracks that do not exist in the dataset.
    """
    total_song_id_list = []
    playlist_id = parse_link_to_id(playlist_link)
    playlist = sp.playlist(playlist_id)
    for item in playlist['tracks']['items']:
        song_track = item['track']
        total_song_id_list.append(song_track['id'])
    return(total_song_id_list)


def get_non_existing_track_features(playlist_link) -> dict:
    """
    Return dictionary of track features, the keys represent 
    the track ids and the values are a list for each track's feature ordered in this fashion
    [acousticness, danceability, energy, duration_ms, instrumentalness, valence, tempo, liveliness, loudness, speechiness, key]
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


def parse_link_to_id(playlist_link) -> str:
    split_url = playlist_link.split('/')
    splitted = split_url[4]
    split_again = splitted.split('?')
    playlist_id = split_again[0]
    print(playlist_id)
    return playlist_id


def get_existing_track_ids(playlist_link) -> list:
    return list(
        set(get_total_track_ids(playlist_link)).intersection(data_ids))


def get_non_existing_track_ids(playlist_link) -> list:
    return list(
        set(get_total_track_ids(playlist_link)).difference(data_ids))


# print(get_existing_track_ids('https://open.spotify.com/playlist/5qUR1BTHhUMucQxb32JxXD?si=ruP35YDrSzqcD4q5CN-srw'))
# print(get_non_existing_track_ids('https://open.spotify.com/playlist/7ByDxKg4FmhrHe8GASNr23?si=8857e747ec7f4488'))
print(get_non_existing_track_features())
# print(get_total_track_ids('https://open.spotify.com/playlist/5qUR1BTHhUMucQxb32JxXD?si=ruP35YDrSzqcD4q5CN-srw'))
