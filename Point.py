from typing import Any


class Point:
    """This class is to represent a song in a graph"""

    pos: Any
    id: str
    neighbours: dict

    def __init__(self, pos: ..., point_id='NA') -> None:
        """Initializes Point class"""
        self.pos = pos
        self.id = point_id
        self.neighbours = dict()  # distance to Point

    def __repr__(self) -> str:
        """Returns the str of the id"""
        return str(self.id)

    def become_neighbour(self, point: ...) -> None:
        """
        ...
        """
        distance = self.distance_from(point)
        while distance in self.neighbours:
            distance += 0.0000000001
        self.neighbours[distance] = point
        point.neighbours[distance] = self

    def is_neighbour_with(self, point: ...):
        """Returns whether a point is neighbours with given point"""
        return point in self.neighbours.values()

    def get_neighbour(self, distance: ...) -> ...:
        """
        ...
        """
        return self.neighbours[distance]

    def distance_from(self, point) -> ...:
        """
        Returns the distance from a given point
        """
        dimension = len(self.pos)
        accumulator = 0
        for i in range(dimension):
            delta = self.pos[i] - point.pos[i]
            accumulator += delta ** 2
        return accumulator ** 0.5
