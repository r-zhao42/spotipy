"""A module containing the classes needed to perform the k-means clustering algorithm

For our project, to use this module, a KMeansAlgo object should be initialized with the
path 'Data/normalized_data_final.csv' and k of 100. we ran the clustering algorithm
15 times to refine the clusters.


"""

from __future__ import annotations
from typing import List
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Point import Point
import random
import pickle
import csv
from preprocess import Data


class KMeansAlgo:
    """Object to store data and methods for executing k-means algorithm. Specifically,
    the object stores the state of a dataset during a single iteration of k-means. The class
    contains methods to execute the algorithm on the data that is stored.

    Attributes:
        - data: A list of Point objects that are used in the algorithm to form clusters
        - centroids: A list of Point objects that describe the centers of the cluster
        - cluster: A dictionary mapping a centroid to a list of Points in that cluster

    Representation Invariants:
        - k > 0
    """

    data: list
    centroids: list
    clusters: dict

    def __init__(self, path: str, k: int):
        """Initializes the k_means object with k number of centroids that are picked randomly
        from the data points. The initialization also does the first round of clustering based
        on those centroids.

        Preconditions:
            - k > 0
            - path contains a file that is formatted correctly for the load_path function
        """
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
        # initialize a dictionary mapping each current centroid to a empty list
        clusters = dict((key, []) for key in self.centroids)

        # Iterate through every data point and sort into a centroid based on distance
        for i in range(len(self.data)):
            point = self.data[i]
            closest_center = self.centroids[0]
            min_distances = point.distance_from(closest_center)

            # Iterate through each centroid and check distance between centroid and point
            # Closest centroid is saved in closest_center
            for centroid in self.centroids:
                curr_distance = point.distance_from(centroid)
                if curr_distance < min_distances:
                    min_distances = curr_distance
                    closest_center = centroid

            # Append current point to the cluster of the associated center
            clusters[closest_center].append(point)

        return clusters

    def find_new_centroids(self, clusters: dict) -> List[Point]:
        """Returns the new centroids for each cluster based on the average of the attributes of the
        points in each cluster. The new centroids are returned as a list of Point objects"""
        new_centroids = []

        # Iterate through the clusters and update each center
        for centroid in clusters:

            # Helper function finds the new center for each individual cluster
            new = self._update_centroid(centroid, clusters[centroid])
            new_centroids.append(new)

        # returns a list of the new centroids which will be used to update the clusters
        return new_centroids

    def _update_centroid(self, centroid: Point, points: list) -> Point:
        """Returns the new center of the cluster associated with the given centroid. If the
        cluster is empty, then the original centroid is returned. Otherwise, a new Point object
        is created with the position of the new center is returned."""

        if len(points) == 0:
            # If the length of the associated cluster is 0, return original centroid
            return centroid
        else:
            # If length of associated cluster is > 0, find new centroid
            new_pos = []
            dimensions = len(centroid.pos)

            # Iterate through each attribute of the clusters and find the average
            for i in range(dimensions):
                accumulator = 0
                for point in points:
                    accumulator += point.pos[i]
                # Append the average to the pos value of new centroid
                new_pos.append(accumulator / len(points))

            # Return point object with pos of new centroid
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

    def graph_3d(self, x: str, y: str, z: str, n: int):
        """
        Graph the furthest n clusters in 3 dimensions based on the attributes given
        for x, y, and z.

        Preconditions:
             - x in {acousticness, danceability, energy, duration_ms, instrumentalness, valence,
            tempo, liveness, loudness, speechiness, key}
            - y in {acousticness, danceability, energy, duration_ms, instrumentalness, valence,
            tempo, liveness, loudness, speechiness, key}
            - z in {acousticness, danceability, energy, duration_ms, instrumentalness, valence,
            tempo, liveness, loudness, speechiness, key}
            - n <= len(self.cluster)
            - x != y != z
        """
        # If matplotlib is displaying a graph, clear the graph
        if plt.get_fignums():
            plt.clf()

        # Map input str to associated index in pos
        attribute_to_index = {'acousticness': 0, 'danceability': 1, 'energy': 2, 'duration_ms': 3,
                              'instrumentalness': 4, 'valence': 5, 'tempo': 6, 'liveness': 7,
                              'loudness': 8, 'speechiness': 10, 'key': 11}

        x_index = attribute_to_index[x]
        y_index = attribute_to_index[y]
        z_index = attribute_to_index[z]
        points = []

        # Find n centroids that are the furthest from each other
        clusters_to_graph = self.find_furthest_n_clusters(n)

        for cluster in clusters_to_graph:
            points.extend(self.clusters[cluster])

        # Generate the x, y, z values to plot
        x = [point.pos[x_index] for point in points]
        y = [point.pos[y_index] for point in points]
        z = [point.pos[z_index] for point in points]

        for point in self.centroids:
            x.append(point.pos[x_index])
            y.append(point.pos[y_index])
            z.append(point.pos[z_index])

        colors = []
        colors_choices = list(plt.cm.colors.cnames)

        # Generate color map for graph
        c_i = 10
        for cluster in clusters_to_graph:
            for _ in self.clusters[cluster]:
                colors.append(colors_choices[c_i])
            c_i += 1
            if c_i >= len(colors_choices):
                c_i = 0
        for _ in range(len(self.centroids)):
            colors.append('black')

        # Plot graph
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(xs=x, ys=y, zs=z, color=colors)
        plt.show()

    def graph_2d(self, x: str, y: str, n: int):
        """
        Graph the clusters in 2 dimensions based on the attributes given for x and y

        Preconditions:
            - x in {acousticness, danceability, energy, duration_ms, instrumentalness, valence,
            tempo, liveness, loudness, speechiness, key}
            - y in {acousticness, danceability, energy, duration_ms, instrumentalness, valence,
            tempo, liveness, loudness, speechiness, key}
            - n <= len(self.clusters)
            - x != y
        """
        # If matplotlib is displaying a graph, clear the graph
        if plt.get_fignums():
            plt.clf()

        # Map input str to associated index in pos
        attribute_to_index = {'acousticness': 0, 'danceability': 1, 'energy': 2, 'duration_ms': 3,
                              'instrumentalness': 4, 'valence': 5, 'tempo': 6, 'liveness': 7,
                              'loudness': 8, 'speechiness': 10, 'key': 11}

        x_index = attribute_to_index[x]
        y_index = attribute_to_index[y]

        points = []

        # Find n centroids that are the furthest from each other
        clusters_to_graph = self.find_furthest_n_clusters(n)

        for cluster in clusters_to_graph:
            points.extend(self.clusters[cluster])

        # Generate the x, y values to plot
        x = [point.pos[x_index] for point in points]
        y = [point.pos[y_index] for point in points]

        for point in self.centroids:
            x.append(point.pos[x_index])
            y.append(point.pos[y_index])

        colors = []
        colors_choices = list(plt.cm.colors.cnames)

        # Generate color map for graph
        c_i = 10
        for cluster in clusters_to_graph:
            for _ in self.clusters[cluster]:
                colors.append(colors_choices[c_i])
            c_i += 1
            if c_i >= len(colors_choices):
                c_i = 0

        for _ in range(len(self.centroids)):
            colors.append('black')

        # Plot graph
        plt.scatter(x, y, c=colors)
        plt.show()

    def find_furthest_n_clusters(self, n: int) -> list:
        """Returns a list of clusters that are far away from each other"""
        centroids = list(self.clusters)
        distances = []

        # Find the distances of every unique pair of centroids and store in list as tuple
        # with values as distance, centroid1, centroid2
        for i in range(len(centroids)):
            centroid1 = centroids[i]
            for j in range(i, len(centroids)):
                centroid2 = centroids[j]
                if centroid1 != centroid2:
                    distances.append((centroid1.distance_from(centroid2), centroid1, centroid2))
        # Sort the tuples by descending distance
        distances.sort(reverse=True)

        result = set()

        i = 0

        # Take the first n values and put the centroids in a list
        while len(result) < n:
            result.add(distances[i][1])
            result.add(distances[i][2])
            i += 1

        # Return the result as a list of centroids
        return list(result)


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


if __name__ == "__main__":
    # raw_data = load_path("Data/normalized_Hayks data with id.csv")
    # data = initialize_data(raw_data)
    # k_means = KMeansAlgo("Data/normalized_data_final.csv", 20)
    # k_means.run_n_times(10)
    pickle_file = open(f'Cluster_Final.pickle', 'rb')
    centroid_to_clusters = pickle.load(file=pickle_file)

    # str = "'4vxz7KB3l06mWdzsRNdmwN','50YW5s4ZsaZrzN12E6CUAj','7okHiZwiZD9nILstUvueqA','2p5zujmiMKjIvE7F4bPLXs','7b02ASgJ2cUFa7VV5kdjaH','5829G0yclOOhpD41OxSqRD','3kqg0gYmuQZvqVZQvRG3Ni','007SutdC0rVG2CSkuQMtJw','3c8lbDVKiW03lobLl7g070','1K2pZLhxXt9iS6qHvKvKAL','4vxz7KB3l06mWdzsRNdmwN','0wL2AEvlDnDm3vxT7AGVer','14DEFzUKmqBlbrB9LQCtJY','5xlRxcBGa6RqPRBzKP8fwv'"
    # str2 = "'02efbC46vYabdIzACziv48', '59F43S4fSrHLFd23HKZbfx', '62jhxOtw1COJk5mXsxBDSH', '32bAR5FU86uAHywmllMu8w', '6eHDdGXvOyKE7v0LVjx35E', '6nH2PL1X4UeS2cTFyGdT4m', '5w24UcHajQ4VJmrkhFWaFP', '0mUUHWkyT0ooQ1Hpjtj3he', '76EQ0fFYsGKyVl0qANQXXb', '03CRy0Ti6SlC9Miejx9k91', '78wPUh4RGROfyDeAmMhkTB', '0YwlC9RkXUNATmbP4N6hsb', '4tV2GAiMdElyGG9Koz3sQd', '4BMHp3DkI8VLsuB9Kr0pzu', '3WC59lU76oCtIdtLw7Jrun', '0OvihwJhbFe6hadqs9knFv', '4djhFqSUhihI2N4i8wKB3t', '2y5dtwS93dpV23ocYxmWGK', '7nAg8faqy1Oivy4fzDDwzK', '0qUqdEglnF03xrKHRQf4o6', '6cetjl3dKU4uqbZoZGGycB', '3CZ6dewgB5uzSfIgj05xe8', '0m5NMTlhs0BaH4ItVCKjSy', '62NWNNurPM7bKIlclxDk98', '5rJtRfZZzQPSFniihmS5Vy', '4viN0zu1qICvrovmBExUnt', '25QmGBhQEu04ru2UotShr2', '4UVkcTyd6h95ZTj5qjvvs0', '5LAwJN9tqGeyduMb4B4r4G', '7aoZmfCBOmAnwJUXc3wjan', '29lj9cYO8ni1UfUF7sEuHY', "
    #
    # new2 = str2.replace("'", "")
    # new1 = new2.replace('"', '')
    # new = new1.replace(" ", "")
    #
    # new4 = str.replace("'", "")
    #
    # str_lst = new4.split(',')






    # for id in str_lst:
    #     for cluster in centroid_to_clusters:
    #         centroid_ids = [point.id for point in centroid_to_clusters[cluster]]
    #         if id in centroid_ids:
    #             print(cluster.pos)







    all_cluster_ids = set()

    for cluster in centroid_to_clusters:
        for point in centroid_to_clusters[cluster]:
            all_cluster_ids.add(point.id)

    data = Data()

    id_column = data.data['id']

    raw_id_list = id_column.tolist()

    raw_id_set = set(raw_id_list)

    humble = '7KXjTSCq5nL1LoYtL7XAwS'
    recommendation = '0ykQtZ84NGXhHIVFQgbxyj'

    for cluster in centroid_to_clusters:
        centroid_ids = [point.id for point in centroid_to_clusters[cluster]]
        if humble in centroid_ids:
            print(cluster.pos)

    for cluster in centroid_to_clusters:
        centroid_ids = [point.id for point in centroid_to_clusters[cluster]]
        if recommendation in centroid_ids:
            print(cluster.pos)



    print('input')
    # inputs = ['6IParsannfwoLCcNSfxQPh', '57BGVV6wcyhbn3hsjlqEZB', '2SAqBLGA283SUiwJ3xOUVI',
    #           '2r6OAV3WsYtXuXjvJ1lIDi', '1t9WgS8FN0534tLBRwbaxO', '1VLtjHwRWOVJiE5Py7JxoQ',
    #           '0ZLuW8uOXdFNWcI40C0OC2', '3nS9a01VvXHQriLqJYwRqG', '2h4cmbyb6S7e8igDZIITJU',
    #           '5SWnsxjhdcEDc7LJjq9UHk']

    inputs = ['3s4mrPrEFFPF0LmAfutW0n', '6Yqmv7XJLCrQEauMbPGZSw', '2xLMifQCjDGFmkHkpNLD9h',
              '1KIQ0RscHwxXPJUvhuO5Bl', '6gi6y1xwmVszDWkUqab1qw', '6Ozh9Ok6h4Oi1wUSLtBseN',
              '7KXjTSCq5nL1LoYtL7XAwS', '0TlLq3lA83rQOYtrqBqSct', '3YeJXuRSNS5FYwOsDu44kD',
              '62vpWI1CHwFy7tMIcSStl8', '2DQ1ITjI0YoLFzuADN1ZBW', '6ya8ejoKgw906Y8LWclqrp',
              '07KXEDMj78x68D884wgVEm', '2d8JP84HNLKhmd6IYOoupQ', '3R9j8urSPiBbapNbyuSYkE',
              '3nAq2hCr1oWsIU54tS98pL', '1ThmUihH9dF8EV08ku5AXN', '7rC5Pl8rQSX4myONQHYPBK',
              '2u7mxWSeoqTXndK5e08jMp', '2FUNBaa5DwItJtYEBgAblU', '4rgwri7LajWVZvdj2N81SS',
              '3JAeYOjyJodI4PRs44lx2l', '0ESJlaM8CE1jRWaNtwSNj8', '598yNsG1JFrGd4n2kMoz7F',
              '7lAK3oHbfEnvUQWosrMMpR', '3wwo0bJvDSorOpNfzEkfXx', '27GmP9AWRs744SzKcpJsTZ',
              '49zD0wr2S3d0lZPib0K4e1', '6LyAwkJsHlW7RQ8S1cYAtM', '1dUHF4RyMmMTveJ0Rby6Xm',
              '7wBJfHzpfI3032CSD7CE2m', '2gwkD6igEhQbDQegRCcdoB', '1jQsKN68yE94tMYml0wHMd',
              '5yY9lUy8nbvjM1Uyo1Uqoc',
              '5NFYuqu8V6QXc6mzcLImd6', '3eekarcy7kvN4yt5ZFzltW', '7pas6O1LYbaeChEFQBhPFU',
              '6hkQ6OQ6nhe7QCckH91aGa', '7ycWLEP1GsNjVvcjawXz3z', '0AluA5RNsa4Cx6XRhf2hWZ',
              '2durxb17bXcmQJHSt8JAdO', '32xx0fAv3CIeGmNaWTHvEF', '1e1JKLEDKP7hEQzJfNAgPl',
              '51EC3I1nQXpec4gDk0mQyP', '0Fpen1PTuEnCmOJtUU9Iud', '6NMtzpDQBTOfJwMzgMX0zl',
              '7sO5G9EABYOXQKNPNiE9NR', '6fwdbPMwP1zVStm8FybmkO', '6PoKfDY78ih5OveWirggRX',
              '4EWCNWgDS8707fNSZ1oaA5', '74lnM5V6ecvoTPV0fvptx9', '577YBGuskWkVDCxZrLRB4v',
              '50a8bKqlwDEqeiEknrzkTO', '5MPPttjfGap2C6j6eKcO6J', '0tdCy39PgWN8LFWu34ORn3',
              '4dVpf9jZjcORqGTLUaeYj9', '3ODXRUPL44f04cCacwiCLC', '6gBFPUFcJLzWGx4lenP6h2',
              '1cZlBZwnwGPtYeRIeQcoFh', '40oKW22ZNNkEdZLJTScaQI', '40jxatV29fk82SAziDsPqN',
              '39Yp9wwQiSRIDOvrVg7mbk', '2IRZnDFmlqMuOrYOLnZZyc', '4iVD0fTHGxV9JWloujsL3s']
    for input in inputs:
        for cluster in centroid_to_clusters:
            centroid_ids = [point.id for point in centroid_to_clusters[cluster]]
            if input in centroid_ids:
                print(cluster.pos)

    print('recommendations')

    recommendations = ['7Djpvy4lZJNI8rTOVLf1H7',
                       '241vjXeYFDwQDG5ZdgvZqs',
                       '64B98qTPN7DLorGZPf2EP6',
                       '02RCbjb9czvQKNGBmEmWob',
                       '3FDhfKLu9mV5RoRQXR5Fj3',
                       '5lehoWkVPujeOAwb8BO0uK',
                       '5i0eJv1DzuyhaYnro4wTKg',
                       '41a7dZcq30Ss5kPMayWRV0',
                       '1XRgIKC5TPwo7nWGyKqgG0',
                       '59J5nzL1KniFHnU120dQzt',
                       '5nayhWICkQGMTkisxVMbRw',
                       '1Xunvmk47Mju6oZlgzm2Ty',
                       '5qDlo2g8QwkA36PNqWpDCz',
                       '22mhfCPBE5YzXWYekGJUdS',
                       '2nKYHpmwjLaEOXS3o7QMiz',
                       '3cWmqvMwVQKDigWLSZ3w9h',
                       '47vzQk78oRe1g9vpT5663T',
                       '4sudugmLvBQasfnRPGUoIy',
                       '3ieLey98V9mIIh3W9gBlPF',
                       '70LcF31zb1H0PyJoS1Sx1r',
                       '20RHWjtCLr7ODGQEItdZXg',
                       '1OjmlSFuzYflWjSMTCyTJv',
                       '4CvWeXMo3PJdpTy6btPwkn',
                       '1K5KBOgreBi5fkEHvg5ap3',
                       '5uEcJOBx1Wz3MvFZ7XTKR0',
                       '3gTK8TzE4on9Xe05QlVIFI',
                       '3a8r3EYOFZB7cT1OkK4zXF',
                       '4bvqOj9QiH6qKecLiefKst',
                       '59JWp4PjZ9TRM8cmtaDYB1',
                       '5NQdweL8O7nGdM7e4IS1lf',
                       '465hVdgg75kPgRdpJfEFFT',
                       '6DWdTk7UaZ6LIYYCFvmgX7',
                       '7la8N6YLMUDAXl2iAEe9Sy',
                       '7DcvwMAiqKJQD1rrdfxSDx',
                       '5u64RlrnvvbtNh6R0EMh6o',
                       '7pnBwXmQuffahj74xsGvRL',
                       '4S99rQA9ixLlvaHK1fJn6n',
                       '4MO2Rtx0FGgOukZO7gw1qB',
                       '2G2ptmdyAhWEIb53U93fZa',
                       '4apiNNK0jp9uqn3JDG9My1',
                       '4aZirFFDJlUUuvhpjY5cAH',
                       '1egFecJPKqG7IcsE3sjZCr',
                       '3BtuIIrQlkujKPuWF2B85z',
                       '4MBxX1P21a0yEZJEHA7zw1',
                       '7huo2wvrCgRucUsjdSDLQV',
                       '0ndVtaoJarSoK9SBCRkaJt',
                       '3cL9ivTyGpd7XMpB4Img2I',
                       '03sEEzFv7vnD54KRwU47Ue',
                       '3feDdjOYqdMd8BCJOZ36P1',
                       '0JFOXqd9N6RlMaAFlaaqFw',
                       '3nqnWEZnYoetfO2ksMZZVK',
                       '6KkAC41nNRiWA6w3ZD9cJ8',
                       '1i0kVfX5LdEdo52St39QM0',
                       '1I0FXGm889xuUAFqcx9bCp',
                       '0zUb5MPkQCcDxqTkXiEIud',
                       '4u4mSxeOuRZHqC9gn1imoJ',
                       '0lTGv9B3KeHGv9yqOMleZX',
                       '3CuKcfH8BJ5The5G3llaKD',
                       '56sNhTYp0mGC1cXaagTNv1',
                       '4a6q8CR2hzLk2plDkSxkfD',
                       '4awnQTwynhz0j6Rk2ZwM6A',
                       '07RXBKfyCYIYRMLCvlGWXU',
                       '5ri4zqtWhG07hIuNNDWP76',
                       '05nbZ1xxVNwUTcGwLbp7CN']

    for id in recommendations:
        for cluster in centroid_to_clusters:
            centroid_ids = [point.id for point in centroid_to_clusters[cluster]]
            if id in centroid_ids:
                print(cluster.pos)

    # true = 0
    # for id in raw_id_list:
    #     if id not in all_cluster_ids:
    #         print(id)
    #     else:
    #         true += 1
    #
    # print('second')
    # true2 = 0
    # for id in all_cluster_ids:
    #     if id not in raw_id_set:
    #         print(id)
    #     else:
    #         true2 += 1
    #




    # cluster_points = []
    #
    # for cluster in centroid_to_clusters:
    #     lst = []
    #     for i in range(100):
    #         lst.append(random.choice(centroid_to_clusters[cluster]).id)
    #     cluster_points.append(lst)
    #
    # out_file = open('Recommendation.txt', "w")
    # for i in range(len(cluster_points)):
    #     for recommendation in cluster_points[i]:
    #         out_file.write(f"'{recommendation}',\n")
    #     out_file.write(f'\n')
