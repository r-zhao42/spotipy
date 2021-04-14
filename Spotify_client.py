import json
from Track import Track
from Playlist import Playlist
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import spotipy.util as util


class SpotifyClient:
    """SpotifyClient performs operations using the Spotify API."""

    def __init__(self, recommended_tracks, playlist_name, user_id='i2fc15uzt49drjhsp3fjcqqdw'):
        """
        :param authorization_token (str): Spotify API token
        :param user_id (str): Spotify user id
        """
        self._user_id = user_id
        self._authorization_token = util.prompt_for_user_token(user_id, 'playlist-modify-public',
                                                               client_id='daf1fbca87e94c9db377c98570e32ece',
                                                               client_secret='1a674398d1bb44859ccaa4488df1aaa9',
                                                               redirect_uri='http://localhost:8888/callback')
        # spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth('daf1fbca87e94c9db377c98570e32ece', '1a674398d1bb44859ccaa4488df1aaa9',  'http://localhost/'))
        # "BQB5RWcJEmQ7meAHN3OnV0u2b3Yc7MpfVCIwI4vjs3YM8H4Bkq2JnWz_6roicsob2iyd4WuXLh6jDCEv86Da9eoDGA7ZBnZaDDpO6k6hrXAeFGPvMjH5urNOOVjYWfukRZgqS2L_hrLs1l554GZd1Cs9T2s_o9rc4Lj14uHgFokF2z-_Wz_oe1UQ0mchJ9SJ-ZJZ_ng3_qfrashqJG8zubSWhGG8I011evoQVX4o1EUB2n78qTzf6g7MQhOoKhgAoTpuy30wSTozMBi6ZINSTcora9nJ7BDUkN1fql9U"
        # util.prompt_for_user_token(self._user_id, 'playlist-modify-public')
        self._tracks = recommended_tracks
        self._url = ''
        self._playlist = self.create_playlist(playlist_name)

    def create_playlist(self, playlist_name) -> Playlist:
        """
        :param name (str): New playlist name
        :return playlist (Playlist): Newly created playlist
        """
        data = json.dumps({
            "name": playlist_name,
            "description": "Recommended songs",
            "public": True
        })
        url = f"https://api.spotify.com/v1/users/{self._user_id}/playlists"
        response = self._place_post_api_request(url, data)
        response_json = response.json()
        # create playlist
        playlist_id = response_json['id']
        playlist = Playlist(playlist_name, playlist_id)
        playlist = self.add_to_playlist(playlist_id)
        return playlist

    def add_to_playlist(self, playlist_id):
        """Add tracks to a playlist.
        :param playlist (Playlist): Playlist to which to add tracks
        :param tracks (list of Track): Tracks to be added to playlist
        :return response: API response
        """
        track_ids = [Track(track) for track in self._tracks]
        track_uris = [track.create_track_uri() for track in track_ids]
        data = json.dumps(track_uris)
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = self._place_post_api_request(url, data)
        response_json = response.json()
        self._url = f'https://open.spotify.com/playlist/{playlist_id}'
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


test_tracks = ['3I9zZfbeaRo9ks1MB7zhmR', '5URYXSFGks9Q8eYePlgVdL', '01oc1NWevpGhtCkiX5flPH', '42tBlHWL3VfDkUM2iWcc5p', '5bknBRjKJZ643DAN2w8Yoy', '7bgwME1OmdDy9iUwYYwzts', '5WpLfhGebLyJOSM4xkW6qP', '0ToC28lLiwEKyQdN4FXypS', '1t4pPnbkOjzoA5RvsDjvUU', '55jQMevNp7aWtiW5LPlPoa', '4VYmdTVFXDq0LtYMoVswTv', '5mexbTuWx9d8DPZk4sDGF4', '7oopoWQa0jicMSf9SFtxMK', '6b4A1mLzePAHGn3XCicLAe', '2LNMhZ3YijTO7USmqjgJfG', '6FhEDaaRFyPRMYqhhXivO9', '2NjeQLvFsfeKdZoA7dbfL1', '4d8BSdhx6WT5GtTOWpv4rh', '5vm7y9SmcH0S1NOQanb8rQ', '2maEFaoAyNjQVv14Hm4esN', '7HRv1sYuwgoea1m0JRvChV', '0WWcJVmz8Yj5hOwJkyycxo', '6MU3ZTQNkV9mUcTSHgoxjr', '5BP0oaQ1VhuaznT77CBXQp', '6huoxhxVtmHGMGmq90U6bE', '4Pwjz3DfvfQWV0rO2V8jyh', '3903Tbix9PdoculpJLikHf', '439TlnnznSiBbQbgXiBqAd', '7pdCmGogZHZH3Xv7LnqVrH', '1hgKlrIGwepPfyq2psckW3', '5FxELQREUBIdy6ZRqZ4iuC', '0rFX6pVvOkXvDgiTR5v5kX', '4ox8bpBggBqCQv56b4XXTf', '6lVoMmI02u5rFFgexe9f3G',
                '295UjwiTtDQdWUDUrKR83W', '2Q0pt1s7gU5GowQDtaZ4CA', '30Yn1oFNYwyLJE1Wlb4Fiy', '73apJ2IYCakxQPuyn4Lp3W', '6NmWJdU1xBEPeK9ydJJ4uL', '7Ks4VCY1wFebnOdJrM13t6', '0N3W5peJUQtI4eyR6GJT5O', '1bxEpNR75Hq3T2oF9AZjt8', '2UOYzhusMTypF7oAQwksCj', '4tQcyj5488alHT1ZgFduzn', '5Mtt6tZSZA9cXTHGSGpyh0', '0v9Wz8o0BT8DU38R4ddjeH', '2Aqc48sn8He26hmTvQ2BMj', '3yM8iyra4fkuyf0H5RFHuE', '6A3hUBzQ0k6chtNJlGxDQn', '1vup3vAmSmFLxSIzGOM38V', '5RbV7Ps6HM2tBbxTd3FnDh', '2DgMxFMUQRPthW4ROhjen1', '1m4C9zlV89rXTfXStluvec', '4eSSRTR5guMgoLaB4YmFwi', '3YDjqMC2P5jW1RjXhaEuK2', '4Cv5PfRm2Qefuaxapdk9XQ', '66ZcOcouenzZEnzTJvoFmH', '6SSLgl0gywQ5Z4dlLj7laX', '0aO3OoQ9VdjiefNa2lwLnn', '6dHatCnuOb1TdBIeJTK3Y0', '1LUyHPbfI0EXbMkvHR0PNX', '7ItFoQDmQIh3MAPsxiP6Vt', '2kmpyKQjVw5UOcVlmkxnYY', '6R0GRYk2vs2XuBVemYK5YZ', '0mXDySw7m2OXK6Wd9hc9Js', '6iMo7yzmXqMC57FOHOSotz', '52d35Deejayu18L7EPCIjU', '0xlFTYyh8qnez0ndGKo5lj', '1eQBEelI2NCy7AUTerX0KS', '53xEdeXpJLWqufWzUeQWbn', '3mmLyEhphJAaW7hyEXAD8l', '4rmCUodFiPbIIV9Vdof42A', '6f4CxfbXGtD1a4VPHEpN48', '7IowzY0ZVbZ9PIrxBPjn92', '3MkYUoEo1Yk1peHN4cof0c', '6VgYcgaeVz0kehOM1qQqd7', '6NvRxjfYkkT2SpirAlmsjH', '5kgvRTKmoJChOc5PAdHZg3', '7oXRMDUzBPekkLRTJhSGvC', '5q453TyHMg7pxYdNG9nufn', '0wmaGiDKtKaRf7G8nBfNsQ', '1Pc3gTtQG4Cq1x81NcXtCN', '4IswprVy2RdWGhiJVKWYau', '4RdQZodcn9NwMVW6sGNnp6', '1Dhi8OBMSyukjUQ93uBfNz', '6mfKEPTYiBAYZ9z0429jsp', '2v8sPwkqVDgWprsmGIis25', '0jYhHo2DhmdkLfonFbPixV', '1cPqCQgCV3qEroz8WYWJK6', '3i5zMNOKm9jR5zLPs4r0Px', '0cAmjsP4d1AXzwAiL38lMr', '1qtYE16BSpHhrY9Tw4CnwU', '35XOKY7RGDCCDO2ovxMMNt', '1NPMFbh4fFDiBMqqcpxASA', '6f0nePKuRRQFfLeROOkt7F', '7llB3cQPT1Yfm7uiVTQTTC', '56zgAN1IE4gLKI2dbvknCI', '5SPFU6mys52n07fem3EXBA', '7bGOND7852tOD0RInMTO0u', '5xrkAXDPhJx44YeNpk9Z1f']
client = SpotifyClient(test_tracks, playlist_name='test')
print(client._url)
