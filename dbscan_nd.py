import argparse
import csv
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class DBSCAN_Algo:
    def __init__(self, data, epsilon, min_points):
        self.data = data
        self.dimension = len(data[0].pos)
        self.epsilon = epsilon
        self.min_points = min_points
        self.clusters = []
        self.points_not_alone = 0

    def print_summary(self):
        print('SUMMARY:')
        print(f'# OF POINTS: {len(self.data)}')
        print(f'# OF CLUSTERS: {len(self.clusters)}')
        print('\n'.join([str(cluster) for cluster in self.clusters]))

    def draw_with_matplotlib(self):
        def cycle_color(num):
            colors = ['darkkhaki', 'turquoise', 'mediumorchid', 'teal', 'deepskyblue', 'olivedrab', 'lightgray',
                      'black', 'maroon', 'rosybrown', 'darkseagreen', 'deeppink', 'darkorange', 'slateblue', 'chocolate']
            num = num % len(colors)
            return colors[num]

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        for cluster_id, cluster in enumerate(self.clusters):
            xs = [point.pos[0]
                  for point in cluster.points] if self.dimension >= 1 else [0] * len(cluster.points)
            ys = [point.pos[1]
                  for point in cluster.points] if self.dimension >= 2 else [0] * len(cluster.points)
            zs = [point.pos[2]
                  for point in cluster.points] if self.dimension >= 3 else [0] * len(cluster.points)
            ax.scatter(xs=xs, ys=ys, zs=zs, color=cycle_color(cluster_id), marker='.')

        plt.show()

    def run(self):
        start_time = time.time()
        print(f'Start time: {time.ctime(start_time)}')

        noise = Cluster([])
        self.clusters.append(noise)

        for point in self.data:
            if not point.visited:
                assert len(point.pos) == self.dimension, 'Points have different dimensions'
                point.update_visited(True)
                points_within_epsilon = self.get_points_within_epsilon(point)
                if len(points_within_epsilon) < self.min_points:
                    noise.add_point(point)
                    self.update_progress()
                else:
                    expanded_cluster = Cluster([])
                    self.expand_cluster(expanded_cluster, point, points_within_epsilon)
                    if expanded_cluster not in self.clusters:
                        self.clusters.append(expanded_cluster)

        end_time = time.time()
        elapsed_s = end_time - start_time
        elapsed_m = elapsed_s / 60
        elapsed_h = elapsed_m / 60
        print('\r')
        print(f'End time: {time.ctime(end_time)}')
        print(f'Seconds elapsed: {elapsed_s:.{2}f}')
        print(f'Minutes elapsed: {elapsed_m:.{2}f}')
        print(f'Hours elapsed: {elapsed_h:.{2}f}')

    def expand_cluster(self, cluster, cur_point, points_within_epsilon):
        cluster.add_point(cur_point)
        self.update_progress()
        for close_point in points_within_epsilon:
            if not close_point.visited:
                close_point.update_visited(True)
                points_within_epsilon_to_close_point = self.get_points_within_epsilon(close_point)
                if len(points_within_epsilon_to_close_point) >= self.min_points:
                    points_within_epsilon.extend(points_within_epsilon_to_close_point)
            if not close_point.is_member:
                cluster.add_point(close_point)
                self.update_progress()

    def get_points_within_epsilon(self, cur_point):
        points_within_epsilon = []
        for point in self.data:
            if point.distance_from(cur_point) <= self.epsilon:
                points_within_epsilon.append(point)
        return points_within_epsilon

    def update_progress(self):
        self.points_not_alone += 1
        cur = self.points_not_alone
        total = len(self.data)
        print(f'Progress: {cur} / {total} => {round(cur * 100 / total, 2)}%', end='\r')


class Cluster:
    def __init__(self, points):
        self.points = points

    def __repr__(self):
        # return f'CLUSTER: {[str(point) for point in self.points]}'
        return f'CLUSTER: {len(self.points)} Points'

    def add_point(self, point):
        self.points.append(point)
        point.update_member(True)


class Point:
    def __init__(self, pos):
        self.pos = pos
        self.visited = False
        self.is_member = False

    def __repr__(self):
        coords = list(map(lambda coord: str(round(coord, 2)), self.pos))
        return ', '.join(coords)

    def distance_from(self, point):
        dimension = len(self.pos)
        accumulator = 0
        for i in range(dimension):
            delta = self.pos[i] - point.pos[i]
            accumulator += delta ** 2
        return accumulator ** 0.5

    def update_visited(self, new_visited_val):
        self.visited = new_visited_val

    def update_member(self, new_member_val):
        self.is_member = new_member_val


def load_data(path):
    return [[float(val) for val in line] for line in csv.reader(open(path))]


def initialize_data(data):
    return [Point(line) for line in data]


if __name__ == '__main__':
    # Good results:
    # --csv-path=Test_Data_2D.csv --epsilon=2 --min-points=2
    # --csv-path=Spotify_Data_Columns_Removed_1000.csv --epsilon=1500 --min-points=15
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv-path', type=str)
    parser.add_argument('--epsilon', type=float)
    parser.add_argument('--min-points', type=float)
    args = parser.parse_args()

    data = load_data(args.csv_path)
    initialized_data = initialize_data(data)

    dbscan_obj = DBSCAN_Algo(data=initialized_data, epsilon=args.epsilon,
                             min_points=args.min_points)
    dbscan_obj.run()
    dbscan_obj.print_summary()
    dbscan_obj.draw_with_matplotlib()
