import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class DBSCAN_Algo:
    def __init__(self, data, epsilon, min_points):
        self.data = data
        self.epsilon = epsilon
        self.min_points = min_points
        self.clusters = []

    def print_clusters(self):
        for cluster in self.clusters:
            print(cluster)
            print('\n')

    def draw_with_matplotlib(self):
        def cycle_color(num):
            colors = ['darkkhaki', 'turquoise', 'mediumorchid', 'teal', 'deepskyblue', 'olivedrab', 'lightgray',
                      'black', 'maroon', 'rosybrown', 'darkseagreen', 'deeppink', 'darkorange', 'slateblue', 'chocolate']
            num = num % len(colors)
            return colors[num]

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        for cluster_id, cluster in enumerate(self.clusters):
            xs = [point.x for point in cluster.points]
            ys = [point.y for point in cluster.points]
            zs = [0 for i in range(len(xs))]
            ax.scatter(xs=xs, ys=ys, zs=zs, color=cycle_color(cluster_id), marker='.')

        plt.show()

    def run(self):
        noise = Cluster([])
        self.clusters.append(noise)

        for point in self.data:
            if not point.visited:
                point.update_visited(True)
                points_within_epsilon = self.get_points_within_epsilon(point)
                if len(points_within_epsilon) < self.min_points:
                    noise.add_point(point)
                else:
                    expanded_cluster = Cluster([])
                    self.expand_cluster(
                        expanded_cluster, point, points_within_epsilon)
                    if expanded_cluster not in self.clusters:
                        self.clusters.append(expanded_cluster)

    def expand_cluster(self, cluster, cur_point, points_within_epsilon):
        cluster.add_point(cur_point)
        for close_point in points_within_epsilon:
            if not close_point.visited:
                close_point.update_visited(True)
                points_within_epsilon_to_close_point = self.get_points_within_epsilon(
                    close_point)
                if len(points_within_epsilon_to_close_point) >= self.min_points:
                    points_within_epsilon.extend(
                        points_within_epsilon_to_close_point)
            if not close_point.is_member:
                cluster.add_point(close_point)

    def get_points_within_epsilon(self, cur_point):
        points_within_epsilon = []
        for point in self.data:
            if point.distance_from(cur_point) <= self.epsilon:
                points_within_epsilon.append(point)
        return points_within_epsilon


class Cluster:
    def __init__(self, points):
        self.points = points

    def __repr__(self):
        return f'CLUSTER: {[str(point) for point in self.points]}'

    def add_point(self, point):
        self.points.append(point)
        point.update_member(True)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.is_member = False

    def __repr__(self):
        return f'{round(self.x, 2)}, {round(self.y, 2)}'

    def distance_from(self, point):
        delta_x = self.x - point.x
        delta_y = self.y - point.y
        distance = (delta_x ** 2 + delta_y ** 2) ** 0.5
        return distance

    def update_visited(self, new_visited_val):
        self.visited = new_visited_val

    def update_member(self, new_member_val):
        self.is_member = new_member_val


def load_data(path):
    return [[float(val) for val in line] for line in csv.reader(open(path))]


def initialize_data(data):
    return [Point(line[0], line[1]) for line in data]


if __name__ == '__main__':
    data = load_data('./Test_Data_2D.csv')
    initialized_data = initialize_data(data)

    dbscan_obj = DBSCAN_Algo(data=initialized_data, epsilon=2, min_points=2)
    dbscan_obj.run()
    dbscan_obj.print_clusters()
    dbscan_obj.draw_with_matplotlib()
