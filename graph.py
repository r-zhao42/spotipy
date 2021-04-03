from __future__ import annotations
from typing import Dict, Any


class _SongVertex:
    """
    This is a private class to represent a song vertex in a graph.

    Instance Attributes:
        - song_id: this is an attribute that stores the unique song id assign individually
         by Spotify
        - neighbours: a set that represents all of the other SongVertex-es that are adjacent to it

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """

    song_id: str
    neighbours: set[_SongVertex]

    def __init__(self, song_id: str, neighbours: set[_SongVertex]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.song_id = song_id
        self.neighbours = neighbours

    # Any more methods for this class????


class SongGraph:
    """
    This is a class that represents the graph from the Spotify song dataset


    """
    # Private Instance Attributes:
    #     - _vertices:
    #         This is a dictionary mapping that maps song ids to their _SongVertex objects

    _vertices: Dict[str, _SongVertex]

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
