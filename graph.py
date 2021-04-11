from __future__ import annotations
from typing import Dict, Any, Tuple, List, Optional


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


    Private Instance Attributes:
        - attribute_list: is a list of all the songs attributes with uniform format, for example:

                Index           Attribute Type
                0                  'acousticeness'
                1                  'danceability'
                2                   energy
                3                   duration_ms
                4                   instrument
                5                   valence
                6                   tempo
                7                   'liveness'
                8                   loudness
                9                   'speechness'
                10                  'key'


    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """

    song_id: str
    neighbours: Optional[set[Tuple[_SongVertex, float]]]

    _attribute_list: List[float]

    # Decide on whether this needs to be private or not
    cluster: Optional[str]

    def __init__(self, song_id: str, neighbours: set[Tuple[_SongVertex, float]], cluster: str,
                 _attribute_list: List[str]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.song_id = song_id
        self.neighbours = neighbours
        self.cluster = cluster

        self._attribute_list = attribute_list



class SongGraph:
    """
    This is a class that represents the graph from the Spotify song dataset


    Instance Attributes:
        - vertices: a mapping of song ids to their corresponding _SongVertex within the SongGraph

    """
    # Private Instance Attributes:
    #     - _clusters:
    #         This is a dictionary that stores the clusters of the database, derived from K-means
    #         clustering, and the values are the list of songs that are in that specific cluster
    #

    vertices: Dict[str, _SongVertex]
    clusters: Dict[str, List[str]]

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


def add_new_songs(new_songs: Dict[str, List[float]], graph: SongGraph) -> SongGraph:
    """Adds the new songs that are not in our database

    The dictionary of songs are *new* songs that are not in our database, but we will add them
    into our existing graph! Each key of the dictionary is a song ID and the value is a list of
    n dimensional attributes collected from the Spotify API.

    Using this data, we will figure out to which vertices we will add an edge!

    """

    # First iterate through every new song
    for song in new_songs:

        # Add the new vertex into our graph
        graph.add_vertex(song)

        nearest = []
        # Find the three nearest neighbours of this song
        for vertex in graph.vertices:
            list_of_attributes = new_songs[song]

            # Implemement this
            normalize(list_of_attributes)

            distance = vertex.get_distance(song)

            # Append the tuple(distance to current song, vertex in the graph)
            nearest.append((distance, vertex))

        # Sort nearest and get the 3 closest ones
        sorted_nearest = nearest.sorted(reverse=True)[:3]

        # Add edges from this song, to the three nearest vertices in our graph
        for i in range(len(sorted_nearest)):
            graph.add_edge(song, sorted_nearest[i][1])

        # Check if all have different clusters or not!
        is_all_different = all([sorted_nearest[i][0] != sorted_nearest[i + 1][0]
                                for i in range(len(sorted_nearest) - 1)])

        if is_all_different:
            # Here we would pick the cluster of the closest vertex

            target_cluster = sorted_nearest[0][0]

            # We add the *new song* to this cluster
            graph.clusters[target_cluster].append(song)

        else:   # In this case there would be a majority

            majority_cluster = _majority_cluster(sorted_nearest)

            # We add the *new song* to this majority cluster
            graph.clusters[majority_cluster].append(song)

    # We return the mutated graph
    return graph


def _majority_cluster(sorted_nearest: List[Tuple[float, str]]) -> str:
    """Helper function that returns the cluster that occurs the most in the list of nearest clusters


    >>> lst = [(3.59, 'a'), (4.78, 'a'), (6.89, 'b')]
    >>> _majority_cluster(lst)
    'a'

    """

    occurrence_dict = {}

    # Setup the dictionary
    for tup in sorted_nearest:
        occurrence_dict[tup[1]] = 0

    for tup in sorted_nearest:
        occurrence_dict[tup[1]] += 1

    return max(occurrence_dict, key=occurrence_dict.get)


def normalize(attributes: list[floats]) -> list[float]:
    """This function returns the normalized list of song attributes"""


# MAKE THIS A GRAPH METHOD
def distance(normalized_attributes: list[floats], vertex: _SongVertex) -> float:
    """Returns the distance of v_1 and v_2"""


def recommend_songs(graph: SongGraph, length: int, user_songs: list[str]) -> list[str]:
    """Returns a list of songs to recommend back to the user from the songs they inputted
    into the Tkinter UI"""

    song_to_recommend = []

    # Iterate through the vertices in the graph
    for vertex in graph.vertices:

        pass

    return lst
    # return song_to_recommend


if __name__ == '__main__':

    import doctest
    doctest.testmod()

