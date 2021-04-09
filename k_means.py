import csv

class K_MEANS_Algo:
    """Class for k-means algorithm"""

    data: list
    k: int
    clusters: list


    def __init__(self, data, k: int):
        self.data = data
        self.k = k
        self.clusters = []


