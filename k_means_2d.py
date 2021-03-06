"""
CSC111 Final Project: Playlist Generator

Module Description
==================
This module was created as a copy of the k_means.py module intended to be used for testing
the k-means algorithm on 2D datasets. This dataset was primarily used for testing the algorithm
by graphing the state of a KMeansAlgo object at various iterations to see if the algorithm
was working as intended.

Copyright and Usage Information
===============================

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

This file is Copyright (c) 2021 Si Yuan Zhao, Hayk Nazaryan, Cliff Zhang, Joanne Pan.
"""
from __future__ import annotations
import matplotlib.pyplot as plt
import random
import csv
import time


class K_MEANS_Algo:
    """Class for k-means algorithm"""

    data: list
    centroids: list
    clusters: dict

    def __init__(self, data, k: int):
        self.data = data
        self.centroids = [random.choice(data) for _ in range(k)]
        self.clusters = self.update_clusters()
        self.graph()

    def run_n_times(self, n: int):
        for _ in range(n):
            self.run_once()
            time.sleep(2)

    def run_once(self):
        self.centroids = self.find_new_centroids(self.clusters)
        self.clusters = self.update_clusters()
        self.print_cluster_len()
        self.graph()

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

    def graph(self):
        points = []

        for cluster in self.clusters:
            points.extend(self.clusters[cluster])

        x = [point.pos[0] for point in points]
        y = [point.pos[1] for point in points]

        for point in self.centroids:
            x.append(point.pos[0])
            y.append(point.pos[1])

        colors = []
        colors_choices = ['navy', 'green', 'yellow', 'red', 'purple', 'pink', 'brown', 'black']

        c_i = 0
        for cluster in self.clusters:
            for _ in self.clusters[cluster]:
                colors.append(colors_choices[c_i])
            c_i += 1
        for _ in range(len(self.centroids)):
            colors.append('black')

        plt.scatter(x, y, c=colors)
        plt.show()





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
    raw_data = load_path("Kmeans Data/test_data_full_2d.csv")
    data = initialize_data(raw_data)

    k_means = K_MEANS_Algo(data, 4)


