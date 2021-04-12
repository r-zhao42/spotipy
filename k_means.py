"""A module containing the classes needed to perform the k-means clustering algorithm"""

from __future__ import annotations
from typing import Optional, List, Union
import random
import csv


class KMeansAlgo:
    """Class for k-means algorithm

    Attributes:
        - data: A list of Point objects that are used in the algorithm to form clusters
        - centroids: A list of Point objects that describe the centers of the cluster
        - cluster: A dictionary mapping a centroid to a list of Points in that cluster

    Preconditions:
        - k > 0
    """

    data: list
    centroids: list
    clusters: dict

    def __init__(self, data: list, k: int):
        """Initializes the k_means object with k number of centroids that are picked randomly
        from the data points. The initialization also does the first round of clustering based
        on those centroids."""
        self.data = data
        self.centroids = [random.choice(data) for _ in range(k)]
        self.clusters = self.update_clusters()

    def run_n_times(self, n: int) -> None:
        """Run the k_means algorithm n times. Function will not run if n <= 0.
        """
        for _ in range(n):
            self.run_once()

    def run_once(self) -> None:
        """Runs the k-means algorithm once. The algorithm first finds the new centers of the
        clusters and then updates the clusters themselves. The function stores the new clusters
        in it's attributes and prints the number of Points in each cluster."""
        self.centroids = self.find_new_centroids(self.clusters)
        self.clusters = self.update_clusters()
        self.print_cluster_len()
        print()

    def update_clusters(self) -> dict:
        """Sorts every point in self.data into a cluster based on the centroid that the point
        is closest to. Returns a dictionary mapping each centroid to a list of points which
        represents the clusters."""
        clusters = dict((key, []) for key in self.centroids)
        for i in range(len(data)):
            point = self.data[i]
            closest_center = self.centroids[0]
            min_distances = point.distance_from(closest_center)

            for centroid in self.centroids:
                curr_distance = point.distance_from(centroid)
                if curr_distance < min_distances:
                    min_distances = curr_distance
                    closest_center = centroid

            clusters[closest_center].append(point)

        return clusters

    def find_new_centroids(self, clusters: dict) -> List[Point]:
        """Finds the centers of each cluster and returns the new center as a list of Points"""
        new_centroids = []
        for centroid in clusters:
            new = self._update_centroid(centroid, clusters[centroid])
            new_centroids.append(new)
        return new_centroids

    def _update_centroid(self, centroid: Point, points: list) -> Point:
        """Returns the new center of the cluster associated with the given centroid. If the
        cluster is empty, then the original centroid is returned. Otherwise, a new Point object
        is created with the position of the new center is returned."""
        if len(points) == 0:
            return centroid
        else:
            new_pos = []
            dimensions = len(centroid.pos)

            for i in range(dimensions):
                accumulator = 0
                for point in points:
                    accumulator += point.pos[i]

                new_pos.append(accumulator / len(points))
            return Point(new_pos)

    def print_cluster_len(self) -> None:
        """Print the lengths of each cluster in self.cluster"""
        for cluster in self.clusters:
            print(len(self.clusters[cluster]))

    def get_clusters(self) -> List[List[Point]]:
        """Returns the clusters stored in the object as a list of lists where each inner
        list is a cluster."""
        accumulator = []
        for cluster in self.clusters:
            accumulator.append(self.clusters[cluster])
        return accumulator


class Point:
    """Class representing a point/song in the program.

    Attributes:
        - id: A string representing the spotify id that is is used to retrieve song information.
        - pos: A list of floats that represents the position of the point in n-dimensions, where n\
        is the length of pos
    """
    id: Optional[str]
    pos: list

    def __init__(self, pos: list, id: str = 'NA'):
        """Initializes a Point object. The id value is default to 'NA' if none is provided"""
        self.pos = pos
        self.id = id

    def distance_from(self, point: Point) -> float:
        """Returns the Euclidean Distance between self and another point."""
        dimension = len(self.pos)
        accumulator = 0
        for i in range(dimension):
            delta = self.pos[i] - point.pos[i]
            accumulator += delta ** 2
        return accumulator ** 0.5


def load_path(path: str) -> List[List]:
    """Loads the .csv file at path. This function assumes that the first column represents the id
    of the song and the rest of the columns represent the position values. The function
    returns a list of lists, where each inner list is a row in the .csv file."""
    file = csv.reader(open(path))
    next(file)
    accumulator = []

    for line in file:
        entry = list()
        entry.append(line[0])
        entry.extend([float(val) for val in line[1:]])
        accumulator.append(entry)

    return accumulator


def initialize_data(data: List[List]) -> List[Point]:
    """Given a list of lists in the appropriate format, returns a list of Point objects.

    Precondition:
        - all(type(line[0]) == str for line in data)
        - all([type(val) == Union[float, int] for val in line[1:]] for line in data)
    """
    return [Point(line[1:], line[0]) for line in data]


if __name__ == "__main__":
    raw_data = load_path("Data/Hayk's dropped data.csv")
    data = initialize_data(raw_data)

    k_means = KMeansAlgo(data, 200)
