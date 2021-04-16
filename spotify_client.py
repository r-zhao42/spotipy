import spotipy


class Spotify_Client:
    def __init__(self):
        self.public_id = 'daf1fbca87e94c9db377c98570e32ece'
        self.secret_id = '1a674398d1bb44859ccaa4488df1aaa9'
        # self.redirect_uri = 'https://google.com'
        self.redirect_uri = 'https://pass-post.netlify.app'

    def init_user(self):
        return spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(scope="playlist-modify-public",
                                                                        client_id=self.public_id,
                                                                        client_secret=self.secret_id,
                                                                        redirect_uri=self.redirect_uri))

    def create_playlist(self, playlist_name, song_ids):
        user = self.init_user()
        user_id = user.me()['id']
        playlist_data = user.user_playlist_create(user=user_id, name=playlist_name, public=True)
        user.playlist_add_items(playlist_data['id'], song_ids)
        playlist_link = playlist_data['external_urls']['spotify']
        return playlist_link

    def get_song_features(self, song_id):
        # Doesn't return all features. Only the ones we're considering for clustering.
        user = self.init_user()
        user.trace = True
        features = user.audio_features(song_id)[0]
        return [features['acousticness'], features['danceability'],
                features['energy'], features['duration_ms'],
                features['instrumentalness'], features['valence'],
                features['tempo'], features['liveness'],
                features['loudness'], features['speechiness'],
                features['key']]

    def get_song_ids(self, playlist_link):
        user = self.init_user()
        playlist_id = self.parse_link_to_id(playlist_link)
        res = user.playlist_items(playlist_id,
                                  offset=0,
                                  fields='items.track.id',
                                  additional_types=['track'])['items']
        return [item['track']['id'] for item in res]

    def parse_link_to_id(self, playlist_link):
        split_1 = playlist_link.split('/')[4]
        split_2 = split_1.split('?')
        return split_2[0]


if __name__ == '__main__':
    from pprint import pprint

    song_ids = ['5eI3fMgQoYfYh9NykE78Sn', '70jb2bIurVzYfxhhsRd4ew']
    playlist_name = 'spotify_client test'

    instance = Spotify_Client()
    print(instance.create_playlist(playlist_name, song_ids))
    pprint(instance.get_song_features('5eI3fMgQoYfYh9NykE78Sn'))
    pprint(instance.get_song_ids('https://open.spotify.com/playlist/1fKVI2pKH5EGS0fX2ncoN6'))
    # print(instance.get_song_ids('https://open.spotify.com/playlist/5qUR1BTHhUMucQxb32JxXD?si=T8fWzBbvQUibUxpPOcLn7Q'))
