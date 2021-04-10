from __future__ import annotations
from typing import Dict, Any, Tuple, List


class _SongVertex:
    """
    This is a private class to represent a song vertex in a graph.

    Instance Attributes:
        - song_id: this is an attribute that stores the unique song id assign individually
         by Spotify
        - neighbours: a set of tuples that represent all of the other SongVertex-es
        that are adjacent to it. The first element is the _SongVertex object, and the second element
        is the distance value of the edge that is derived from how "similar" each vertex in
        neighbours is compared to self.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """

    song_id: str
    neighbours: set[_SongVertex]

    def __init__(self, song_id: str, neighbours: set[_SongVertex]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.song_id = song_id
        self.neighbours = set(Tuple[_SongVertex, float])

    # Any more methods for this class????

    def get_vibe(self) -> str:
        """Returns the vibe of the song, in other words, it returns what cluster the song is in"""


class SongGraph:
    """
    This is a class that represents the graph from the Spotify song dataset


    Instance Attributes:
        - vertices: a mapping of song ids to their corresponding _SongVertex within the SongGraph

    """
    # Private Instance Attributes:
    #     - _clusters:
    #         This is a dictionary that stores the clusters of the database, derived from K-means
    #         clustering, and the values are the songs that are in that cluster
    #

    vertices: Dict[str, _SongVertex]
    _clusters: Dict[str, str]

    def __init__(self) -> None:
        """Initialize an empty SongGraph ."""
        self._vertices = {}

    def add_vertex(self, song_id: str) -> None:
        """This method is responsible for adding a new _SongVertex edge to SongGraph"""

        if song_id not in self._vertices:
            new_song_vertex = _SongVertex(song_id, set())

            self._vertices[song_id] = new_song_vertex

    def add_edge(self, song1: str, song2: str) -> None:
        """Add an edge between the two Song vertices with the given items in this SongGraph.

        Raise a ValueError if song1 or song2 do not appear as vertices in this graph.

        Preconditions:
            - song1 != song2
        """
        if song1 in self._vertices and song2 in self._vertices:
            v1 = self._vertices[song1]
            v2 = self._vertices[song2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def get_vertex(self, song_id: str) -> _SongVertex:
        """
        Returns the _SongVertex in the SongGraph based on the given song_id

        """

        return self._vertices[song_id]

    def adjacent(self, song_id1: Any, song_id2: Any) -> bool:
        """Return whether song_id1 and song_id2 are adjacent Song vertices in this SongGraph.

        Return False if song_id1 or song_id2 do not appear as Song vertices in this SongGraph.
        """
        if song_id1 in self._vertices and song_id2 in self._vertices:
            v1 = self._vertices[song_id1]
            return any(v2.song_id == song_id2 for v2 in v1.neighbours)
        else:
            # They are not adjacent
            return False


def add_new_songs(new_songs: Dict[str, List[str]], graph: SongGraph ) -> SongGraph:
    """Adds the new songs that are not in our database

    The dictionary of songs are *new* songs that are not in our database, but we will add them
    into our existing graph! Each key of the dictionary is a song ID and the value is a list of
    n dimensional attributes collected from the Spotify API.

    Using this data, we will figure out to which vertices we will add an edge!

    """

    for song in new_songs:
        for vertex in graph.vertices:

            old_vertex = graph.vertices[vertex]

            # Add vertex to our graph
            graph.add_vertex(song)

            distance = old_vertex.calculate_distance()
            graph


    return graph


def recommend_songs(graph: SongGraph, length: int, user_songs: list[str]) -> list[str]:
    """Returns a list of songs to recommend back to the user from the songs they inputted
    into the Tkinter UI"""

    song_to_recommend = []

    # Iterate through the vertices in the graph
    for vertex in graph.vertices:


    return song_to_recommend



