import json
from track import Track
from playlist import Playlist
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
        self._url = ''


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
        track_uris = [track.create_track_uri() for track in tracks]
        data = json.dumps(track_uris)
        url = f"https://api.spotify.com/v1/playlists/{playlist.id}/tracks"
        response = self._place_post_api_request(url, data)
        response_json = response.json()
        self._url = f'https://open.spotify.com/playlist/{playlist.id}'
        print(self._url)
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


test_tracks = [Track('537l7spEsGg6aWl6Y9eKAs'), Track('537l7spEsGg6aWl6Y9eKAs')]
client = SpotifyClient('BQCc0fzzNOmtDH1WyelW-1ZWupJzJnIrrobXhLY-iyF31zd6bEF3QBoYdqIC3HLBQda_uhs9ATDZKSzFIbUj_F-2plU4FFus3K7Y7LswTqcMwzvx2WmFG4YWx_rtDACUxyN0WIJKVsTGZlKaA8jhlpQpApkqYzcHfYb4sZHizKT0P6iso-ZaYXZHqKagELZCWSWky1nWuxcg9nGHL2nCZn5An7HZsJFWRqs6zm8PWdhp20uu6Un3vxyA74hDVZ6VkwLDNIVjDSKvzwm2pq7xQ5T_Yp7bocjn8qPFXb3O', 	'i2fc15uzt49drjhsp3fjcqqdw')
client.populate_playlist(client.create_playlist('fun'), test_tracks)



