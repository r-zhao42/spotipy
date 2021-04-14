import json
from track import Track
from playlist import Playlist
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests


class SpotifyClient:
    """SpotifyClient performs operations using the Spotify API."""

    def __init__(self, authorization_token, user_id = 'i2fc15uzt49drjhsp3fjcqqdw'):
        """
        :param authorization_token (str): Spotify API token
        :param user_id (str): Spotify user id
        """
        self._authorization_token = authorization_token
        self._user_id = user_id
        self._url = ''

    def create_empty_playlist(self, name) -> Playlist:
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

    def add_to_playlist(self, playlist, tracks):
        """Add tracks to a playlist.
        :param playlist (Playlist): Playlist to which to add tracks
        :param tracks (list of Track): Tracks to be added to playlist
        :return response: API response
        """
        track_uris = [track.create_track_uri() for track in tracks]
        data = json.dumps(track_uris)
        url = f"https://api.spotify.com/v1/playlists/{playlist.id}/tracks"
        response = self._place_post_api_request(url, data)
        response_json = response.json()
        self._url = f'https://open.spotify.com/playlist/{playlist.id}'
        # print(self._url)
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


test_tracks = [Track('537l7spEsGg6aWl6Y9eKAs'),
               Track('537l7spEsGg6aWl6Y9eKAs')]
client = SpotifyClient('BQCfcrUsdeSXG11qOZ9zLQEDMgzZKLO8lUHIMfb37uP_NCuyq9ZNc7xpSum-RqEmYWBQz96BvE-9NzFSYuJI-ClLp_w7elIDsZ6PnmD9JxPl_-vRv7sQjVTeh83vhPm22asBGsxRGdsEKSzGuejlQ1KLB9sg3lWjR-zwKjEJBOaqHPMGM0M0geGAl7359p_JC1EuCj4B6SVGQUb_OY-64fh87z5KO5esEQ8NEGZwyKktIyDrFQYokTM_PtaYN4gU71dpuSD7lpz5OM8hSvxg9CrefBLKmfj9lckf9u-v')
client.add_to_playlist(client.create_empty_playlist('fun'), test_tracks)
