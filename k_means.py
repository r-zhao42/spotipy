from __future__ import annotations
import random
import csv

class K_MEANS_Algo:
    """Class for k-means algorithm"""

    data: list
    centroids: list
    clusters: list


    def __init__(self, data, k: int):
        self.data = data
        self.centroids = [random.choice(data) for _ in range(k)]
        self.clusters = []

    def run_once(self):
        clusters = self.find_closest_centroid()
        return clusters

    def find_closest_centroid(self) -> dict:
        clusters = dict.fromkeys(self.centroids, set())
        for point in self.data:
            closest_center = self.centroids[0]
            max_distances = point.distance_from(closest_center)
            for centroid in self.centroids:
                curr_distance = point.distance_from(centroid)
                if curr_distance > max_distances:
                    max_distances = curr_distance
                    closest_center = centroid
            clusters[closest_center].add(closest_center)
        return clusters

    def update_centroid(self, centroid: Point, points: set):












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

    k_means = K_MEANS_Algo(data, 4, )
