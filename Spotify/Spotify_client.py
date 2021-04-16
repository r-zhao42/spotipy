"""
COPYRIGHT OF: JOANNE PAN, HAYK NAZARYAN, CLIFF ZHANG, RYAN ZHAO

This file is responsible for creating the Spotify User Client so our program can access
personal data of users, such as playlists.

Furthermore, this file is also necessary in order to add songs and generate them to new playlists

"""

import json
from typing import Any
from Track import Track
from Playlist import Playlist
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import spotipy.util as util


class SpotifyClient:
    """SpotifyClient performs operations using the Spotify API."""

    # Private Instance Attributes:
    #      - _user_id: ID of the user
    #      - _authorization_token: Token used to authorize calls to the API
    #      - _tracks: ...
    #      - _url: ...
    #      - _playlist: ...
    #

    def __init__(self, recommended_tracks: ..., playlist_name: str,  # TODO***********
                 user_id='i2fc15uzt49drjhsp3fjcqqdw') -> None:
        """
        :param authorization_token (str): Spotify API token
        :param user_id (str): Spotify user id
        """
        self._user_id = user_id
        self._authorization_token = \
            util.prompt_for_user_token(user_id, 'playlist-modify-public',
                                       client_id='daf1fbca87e94c9db377c98570e32ece',
                                       client_secret='1a674398d1bb44859ccaa4488df1aaa9',
                                       redirect_uri='http://localhost:8888/callback')

        self._tracks = recommended_tracks
        self._url = ''
        self._playlist = self.create_playlist(playlist_name)

    def create_playlist(self, playlist_name: str) -> Playlist:
        """
        Creates and returns a new playlist based on the inputted playlist_name

        Preconditions:
            - isinstance(playlist_name, str)

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

    def add_to_playlist(self, playlist_id: str) -> Any:
        """Responsible for adding tracks to a playlist.
           Returns the API response



        REMOVE THIS MAYBE????
        # :param playlist (Playlist): Playlist to which to add tracks
        # :param tracks (list of Track): Tracks to be added to playlist
        # :return response: API response
        """
        track_ids = [Track(track) for track in self._tracks]
        track_uris = [track.create_track_uri() for track in track_ids]
        data = json.dumps(track_uris)
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = self._place_post_api_request(url, data)
        response_json = response.json()
        self._url = f'https://open.spotify.com/playlist/{playlist_id}'
        return response_json

    def _place_post_api_request(self, url: ..., data: ...) -> ...:  # TODO*****************
        """
        This function is responsible for...

        It returns...(something like, it returns the response which is...)


        """
        response = requests.post(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response
