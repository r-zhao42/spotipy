class Playlist:
    """
    A Playlist object represents a Spotify playlist.

    Instance Attributes:
        - name: a string value that represents the name of the playlist
        - id: a string value that represents the ID of the playlist

    Representation Invariants:
        - isinstance(self.name, str)
        - isinstance(self.id, str)

    """

    name: str
    id: str

    def __init__(self, name: str, id: str) -> None:
        """Initializes a Playlist class"""
        self.name = name
        self.id = id
