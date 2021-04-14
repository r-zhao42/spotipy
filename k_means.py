"""A module containing the classes needed to perform the k-means clustering algorithm

For our project, to use this module, a KMeansAlgo object should be initialized with the
path 'Kmeans Data/normalized_data_final.csv' and k of 150
"""

from __future__ import annotations
from typing import Optional, List, Union
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Point import Point
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

    def __init__(self, path: str, k: int):
        """Initializes the k_means object with k number of centroids that are picked randomly
        from the data points. The initialization also does the first round of clustering based
        on those centroids."""
        self.data = initialize_data(load_path(path))
        self.centroids = [random.choice(self.data) for _ in range(k)]
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
        for i in range(len(self.data)):
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

    # def get_clusters(self) -> List[List[Point]]:
    #     """Returns the clusters stored in the object as a list of lists where each inner
    #     list is a cluster."""
    #     accumulator = []
    #     for cluster in self.clusters:
    #         accumulator.append(self.clusters[cluster])
    #     return accumulator
    def get_clusters(self) -> dict:
        """Returns the clusters stored in the object as a list of lists where each inner
        list is a cluster."""
        return self.clusters

    def graph_3d(self, x: str, y: str, z: str):
        """
        Graph the clusters in 3 dimensions based on the attributes given for x, y, and z

        Preconditions:
             - x in {acousticness, danceability, energy, duration_ms, instrumentalness, valence,
            tempo, liveness, loudness, speechiness, key}
            - y in {acousticness, danceability, energy, duration_ms, instrumentalness, valence,
            tempo, liveness, loudness, speechiness, key}
            - z in {acousticness, danceability, energy, duration_ms, instrumentalness, valence,
            tempo, liveness, loudness, speechiness, key}
        """
        attribute_to_index = {'acousticness': 0, 'danceability': 1, 'energy': 2, 'duration_ms': 3,
                              'instrumentalness': 4, 'valence': 5, 'tempo': 6, 'liveness': 7,
                              'loudness': 8, 'speechiness': 10, 'key': 11}

        x_index = attribute_to_index[x]
        y_index = attribute_to_index[y]
        z_index = attribute_to_index[z]
        points = []

        for cluster in self.clusters:
            points.extend(self.clusters[cluster])

        x = [point.pos[x_index] for point in points]
        y = [point.pos[y_index] for point in points]
        z = [point.pos[z_index] for point in points]

        for point in self.centroids:
            x.append(point.pos[x_index])
            y.append(point.pos[y_index])
            z.append(point.pos[z_index])

        colors = []
        colors_choices = list(plt.cm.colors.cnames)

        c_i = 0
        for cluster in self.clusters:
            for _ in self.clusters[cluster]:
                colors.append(colors_choices[c_i])
            c_i += 1
            if c_i >= len(colors_choices):
                c_i = 0
        for _ in range(len(self.centroids)):
            colors.append('black')

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(xs=x, ys=y, zs=z, color=colors)
        plt.show()

    def graph_2d(self, x: str, y: str):
        """
        Graph the clusters in 2 dimensions based on the attributes given for x and y

        Preconditions:
            - x in {acousticness, danceability, energy, duration_ms, instrumentalness, valence,
            tempo, liveness, loudness, speechiness, key}
            - y in {acousticness, danceability, energy, duration_ms, instrumentalness, valence,
            tempo, liveness, loudness, speechiness, key}
        """
        attribute_to_index = {'acousticness' : 0, 'danceability': 1, 'energy': 2, 'duration_ms': 3,
                              'instrumentalness': 4, 'valence': 5, 'tempo': 6, 'liveness': 7,
                              'loudness': 8, 'speechiness': 10, 'key': 11}

        x_index = attribute_to_index[x]
        y_index = attribute_to_index[y]

        points = []

        for cluster in self.clusters:
            points.extend(self.clusters[cluster])

        x = [point.pos[x_index] for point in points]
        y = [point.pos[y_index] for point in points]

        for point in self.centroids:
            x.append(point.pos[x_index])
            y.append(point.pos[y_index])

        colors = []
        colors_choices = list(plt.cm.colors.cnames)

        c_i = 0
        for cluster in self.clusters:
            for _ in self.clusters[cluster]:
                colors.append(colors_choices[c_i])
            c_i += 1
            if c_i >= len(colors_choices):
                c_i = 0

        for _ in range(len(self.centroids)):
            colors.append('black')

        plt.scatter(x, y, c=colors)
        plt.show()



def load_path(path: str) -> List[List]:
    """Loads the .csv file at path. This function assumes that the first column represents the id
    of the song and the rest of the columns represent the position values. The function
    returns a list of lists, where each inner list is a row in the .csv file.

    Preconditions:
        - The .csv file stored at path must be formatted such that the columns are ordered in the
        following way from left to right
            [acousticness, danceability, energy, duration_ms, instrumentalness, valence, tempo,
            loudness, speechiness, key]
    """
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


# def project_point(pos: list) -> list:
#     """Take a point in 11 dimension and projects it into 3 dimensions
#
#     Specifically, we want to project a 11 dimensional vector onto the volume
#     [x, y, z, 0, 0, 0, 0, 0, 0, 0, 0]
#
#     The equation for a projection is
#         proj_v (u) = ((u * v)/ ||v||^2) * v
#
#     In our case, pos is u and [x, y, z, 0, 0, 0, 0, 0, 0, 0, 0] is v
#     """
#     return []
# def reduce_dimension(pos: list) -> list:
#     t = 1 / pos[-1]
#     return [pos[i] * t for i in range(len(pos) - 1)]
#
# def project_3d(pos: list) -> list:
#     result = pos
#     for _ in range(8):
#         result = reduce_dimension(pos)
#     return result
#
# def project_2d(pos: list) -> list:
#     result = pos
#     for _ in range(9):
#         result = reduce_dimension(pos)
#     return result


if __name__ == "__main__":
    # raw_data = load_path("Data/normalized_Hayks data with id.csv")
    # data = initialize_data(raw_data)
<<<<<<< HEAD
    k_means = KMeansAlgo("Kmeans Data/normalized_data_final.csv", 20)
=======
    # k_means = KMeansAlgo("Kmeans Data/normalized_data_final.csv", 4)
    pass
>>>>>>> d19400608ebd075af2a31ac09cc29af27ace9fd0
