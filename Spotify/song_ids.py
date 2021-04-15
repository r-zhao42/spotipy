def get_song_ids(playlist_link, sp) -> list:
    """
    Given playlist URI, return all song ids included in the playlist.
    """
    total_song_id_list = []
    playlist_id = parse_link_to_id(playlist_link)
    playlist = sp.playlist(playlist_id)
    for item in playlist['tracks']['items']:
        song_track = item['track']
        total_song_id_list.append(song_track['id'])
    return(total_song_id_list)


def parse_link_to_id(playlist_link) -> str:
    split_url = playlist_link.split('/')
    splitted = split_url[4]
    split_again = splitted.split('?')
    playlist_id = split_again[0]
    # print(playlist_id)
    return playlist_id


if __name__ == '__main__':
    import spotipy

    credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
        'daf1fbca87e94c9db377c98570e32ece', '1a674398d1bb44859ccaa4488df1aaa9')
    sp = spotipy.Spotify(client_credentials_manager=credentials_manager)
    # print(get_song_ids('https://open.spotify.com/playlist/1nrmeYg6bEo34nxHgaid1u?si=b879d2b62dc743da', sp))
