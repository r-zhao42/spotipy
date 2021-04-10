from __future__ import annotations
import matplotlib as plt
import random
import csv

class K_MEANS_Algo:
    """Class for k-means algorithm"""

    data: list
    centroids: list
    clusters: dict


    def __init__(self, data, k: int):
        self.data = data
        self.centroids = [random.choice(data) for _ in range(k)]
        self.clusters = self.update_clusters()

    def run_n_times(self, n: int):
        for _ in range(n):
            self.run_once()

    def run_once(self):
        self.centroids = self.find_new_centroids(self.clusters)
        self.clusters = self.update_clusters()
        self.print_cluster_len()
        print()


    def update_clusters(self) -> dict:
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

    def find_new_centroids(self, clusters: dict):
        new_centroids = []
        for centroid in clusters:
            new = self._update_centroid(centroid, clusters[centroid])
            new_centroids.append(new)
        return new_centroids

    def _update_centroid(self, centroid: Point, points: list):
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

    def print_cluster_len(self):
        for cluster in self.clusters:
            print(len(self.clusters[cluster]))



class Point:
    pos: list

    def __init__(self, pos: list):
        self.pos = pos

    def distance_from(self, point: Point):
        dimension = len(self.pos)
        accumulator = 0
        for i in range(dimension):
            delta = self.pos[i] - point.pos[i]
            accumulator += delta ** 2
        return accumulator ** 0.5

class Clusters:
    def __init__(self, points):
        self.points = points

    def __repr__(self):
        # return f'CLUSTER: {[str(point) for point in self.points]}'
        return f'CLUSTER: {len(self.points)} Points'

    def add_point(self, point):
        self.points.append(point)
        point.update_member(True)


def load_path(path: str):
    file = csv.reader(open(path))
    next(file)
    return [[float(val) for val in line] for line in file]

def initialize_data(data: list):
    return [Point(line) for line in data]

if __name__ == "__main__":
    raw_data = load_path("Data/test_data_sample.csv")
    data = initialize_data(raw_data)

    k_means = K_MEANS_Algo(data, 4)




