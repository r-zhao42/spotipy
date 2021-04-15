class Track:
    """
    A Track object represents a single song.
    """

    def __init__(self, id):
        self.id = id

    def create_track_uri(self):
        return "spotify:track:" + self.id