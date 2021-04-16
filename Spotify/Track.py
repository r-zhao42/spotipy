class Track:
    """
    A Track object that represents a single song.

    Instance Attributes:
        - id: the string that represents the unique ID of a given song


    Representation Invariants:
        - isinstance(self.id, str)

    """

    id: str

    def __init__(self, id: str) -> None:
        self.id = id

    def create_track_uri(self) -> str:
        """Creates and returns the Spotify track URI for an arbitrary song"""
        return "spotify:track:" + self.id
