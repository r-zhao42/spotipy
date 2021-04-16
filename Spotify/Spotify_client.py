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

import json
from typing import Any
import spotipy
import requests
import spotipy.util as util
from Spotify.Track import Track
from Spotify.Playlist import Playlist
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyClient:
    """SpotifyClient performs operations using the Spotify API."""

    # Private Instance Attributes:
    #      - _user_id: ID of the user
    #      - _authorization_token: Token used to authorize calls to the API
    #      - _tracks: ...
    #      - _playlist: ...
    #

    url: str

    # Private:
    _user_id: str
    _authorization_token: str
    _tracks: Any
    _playlist: Any

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
                                       redirect_uri='http://localhost:10008')

        self._tracks = recommended_tracks
        self.url = ''
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
        playlist = Playlist(playlist_name, playlist_id)  # Something going wrong here
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
        self.url = f'https://open.spotify.com/playlist/{playlist_id}'
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


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['pickle', 'tkinter', 'PIL', 'urllib', 'webbrowser',
                          'Recommendation', 'Spotify.Spotify_client', 'Spotify.song_features',
                          'k_means', 'spotipy', 'argparse', 'song_tkinter', 'preprocess',
                          'post_cluster', 'json', 'Track', 'Playlist', 'requests',
                          'spotipy.oauth2', 'spotipy.util'],
        'allowed-io': ['UserPlaylistEntry.visualize()'],
        # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
