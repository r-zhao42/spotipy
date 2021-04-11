import os
import Track
import Playlist
from spotifyclient import SpotifyClient


def main():
    spotify_client = SpotifyClient(os.getenv("BQC4otRfd760_smILaAWjhrD51blI4crPaykdiDf88o0i9o \
        bbIDudfmnAE9mOEXKTLG3rWXkfiKptf3QXvYMMsRPy1-wyP7GiVukJJpEqGLiGDJFldBCkiShgjviFJHFTi1dEdYJu1NBC0 \
            -DCQSDAV9hVt5PX9eFmpAc5-AshS_hJ922kfrY2RDhsHMI68Yr4LygcsClLG_QMY-s_j2ov2yZBxJTCtP--j9iUr9seUkHA \
                yREVlEoJSfLzF5J5GmBxHAe2CT_kHxsJeBCPzS1wXvypWOKGesaHi34s-41"),
                                   os.getenv("i2fc15uzt49drjhsp3fjcqqdw"))

    playlist = spotify_client.create_playlist(playlist_name)
    print(f"\nPlaylist '{playlist.name}' was created successfully.")

    # populate playlist with recommended tracks
    
    print(
        f"\nRecommended tracks successfully uploaded to playlist '{playlist.name}'.")


if __name__ == "__main__":
    main()
