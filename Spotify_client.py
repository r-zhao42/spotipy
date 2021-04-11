import json
from Track import Track
from Playlist import Playlist
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import requests



class SpotifyClient:
    """SpotifyClient performs operations using the Spotify API."""

    def __init__(self, authorization_token, user_id):
        """
        :param authorization_token (str): Spotify API token
        :param user_id (str): Spotify user id
        """
        self._authorization_token = authorization_token
        self._user_id = user_id


    def create_playlist(self, name):
        """
        :param name (str): New playlist name
        :return playlist (Playlist): Newly created playlist
        """
        data = json.dumps({
            "name": name,
            "description": "Recommended songs",
            "public": True
        })
        url = f"https://api.spotify.com/v1/users/{self._user_id}/playlists"
        response = self._place_post_api_request(url, data)
        response_json = response.json()

        # create playlist
        playlist_id = response_json['id']
        playlist = Playlist(name, playlist_id)
        return playlist

    def populate_playlist(self, playlist, tracks):
        """Add tracks to a playlist.
        :param playlist (Playlist): Playlist to which to add tracks
        :param tracks (list of Track): Tracks to be added to playlist
        :return response: API response
        """
        track_uris = [track.create_spotify_uri() for track in tracks]
        data = json.dumps(track_uris)
        url = f"https://api.spotify.com/v1/playlists/{playlist.id}/tracks"
        response = self._place_post_api_request(url, data)
        response_json = response.json()
        client_url = f'https://open.spotify.com/playlist/{playlist.id}'
        print(client_url)
        return response_json

    def _place_get_api_request(self, url):
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response

    def _place_post_api_request(self, url, data):
        response = requests.post(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
    )
        return response
client_credentials_manager = SpotifyClientCredentials(
    'daf1fbca87e94c9db377c98570e32ece', '1a674398d1bb44859ccaa4488df1aaa9')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
test_tracks = [Track('Killamonjaro', '537l7spEsGg6aWl6Y9eKAs', 'KILLY'), Track('Killamonjaro', '537l7spEsGg6aWl6Y9eKAs', 'KILLY')]
client = SpotifyClient(sp)
client.populate_playlist(client.create_playlist('fun'), test_tracks)



