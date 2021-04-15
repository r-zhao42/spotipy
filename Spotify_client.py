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


test_tracks = ['2OCTC6cPRdI3Dvdb25jRDC',
'5eI3fMgQoYfYh9NykE78Sn',
'70jb2bIurVzYfxhhsRd4ew',
'1uDjaezEbalGyGnuH80zDK',
'6Y9kdB2O0h9gq9y2vclsWT',
'4VeCg1rkHHiu1utqoNNUhH',
'5SehvGGC53A7SZKCLXQcyt',
'5qDlo2g8QwkA36PNqWpDCz',
'4Tid4MwqgR1CfKCun3tFon',
'3hoiinUc5VA9xUEJID7R8V',
'01vaUGpeRew7Tvfxsf4jcQ',
'4RnSzXTmFBEvGRL7vSCSCO',
'5dv4YSgkpflUQ31vIW9qXg',
'4WQJd6v3HIDGZnn2kJTEc9',
'5mu1uv8RmzDkF8foePK5qa',
'5YGhm6pI5s0uxJ2DwrDYqO',
'6SvuMwPea2zKEN03IWCElv',
'3IrcvqIf3ZiBhf3xdsctRX',
'43BlKpJcSrC9AsJ3F1DKg9',
'5MnXRG5LzgSzdpIkg5nagT',
'1z1btB03Hw1gYwSLPlt67z',
'26w9NTiE9NGjW1ZvIOd1So',
'28oZsTW7GQZ47qtmuS0mjl',
'12PPtN6iHLnPVKuVzxfWSM',
'5PONCrsJnRyMsHBsnUS6I9',
'0XGLsSU6wtfnKXiMNvQr61',
'1eMNW1HQjF1dbb4GtnmpaX',
'0E8R8Ro8cRouDHCJFbsbP1',
'3Zcv9IeYgCvEhxFTfsduaQ',
'0hwkukpHcBJfGcIUxi1tK2',
'0IJA9KP6rT55jrP1YpTdhx',
'5NqOsPI4rA9Bl6LcCftzI2',
'40j4RoqmLiivqzRObbQ4BF',
'423EcxblW9F4nnQkqcqMlK',
'2yJ9GVCLMmzBBfQAnfzlwr',
'34KUIBsIUiPV7oCIzSdDAU',
'1NbBNVSjRfj4jsZCMQ3D9l',
'5y5REf9y44dGuMAHHN3R2L',
'156LzfvMNKuXuiot4uzhGD',
'2ZdCrBA52bb4pIG3tOOZiQ',
'2TlGQg8UKymxu3frqMXeO2',
'6225vlQNgif1W5dE5KN6Y6',
'0EgigrGFGb4PHaVNb7fgK7',
'6zvsh5ev7zJ8gz96bfBnZx',
'1qsHYUd2c1wFGcn7e63QmG',
'4VXIryQMWpIdGgYR4TrjT1',
'44sQXptPXVOrYvcvf9TSUk',
'7la8N6YLMUDAXl2iAEe9Sy',
'6N3oYlfZ2RPdjMYdHCRmFS',
'24qj0Qd0qjiqJlejTIA6ik',
'4pCEIQ6wBVuaJdER5bALtO',
'2u3EyuCqqV31woqGvO9LBz',
'04aqUZa6iLLzRoK5eEb7Zh',
'2jLb0PsBm7OjcvGvVyajua',
'4MOy68Xuz84lkfu1NQH6Bg',
'2DsdZx34mT4jVtnPk1eoFM',
'3VygfAvvgVaJUeaBUSzlZu',
'3JnbauRAM5tvB042wbuorJ',
'6dDcfbMUFkFDk6x93kITY7',
'42er1na9BHF1ERol51wg8M',
'3nXrCAE44KlevAkQB2XWcN',
'217aRtYP4ExBpSNEAVNJkR',
'2g1KggY9PKvsoEAOaiz4xx',
'6IIPfyGQp3SyOcLRO68dWJ',
'71DxDMPiElIeGgvJvtITXR',
'1lguQJjlNrIOoOylYVZN3M',
'2J4P46vCFm1rPkNkp9pZWX',
'53oWwSxPuyH2cjYKXH8fgO',
'0jiW3PNiHJxOhWh9oPBJ7m',
'14Bljc3pOOG0xQX3wqhLN9',
'0RLLvYBopDwooCyvnTwgYu',
'6arLnfArtdWKOcCYzDd4rS',
'7klPHv3HnXdUY3dSfTccNc',
'5uWsTciqKP9yjq9VenPWyR',
'6GskIhdM6TN6EkPgeSjVfW',
'12PNcnMsjsZ3eHm62t8hiy']


client = SpotifyClient(test_tracks, playlist_name='test')
print(client._url)
