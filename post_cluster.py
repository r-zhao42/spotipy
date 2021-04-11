import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Point:
    def __init__(self, pos, point_id):
        self.pos = pos
        self.id = point_id
        self.neighbours = dict()    # distance to Point

    def __repr__(self):
        return str(self.id)

    def become_neighbour(self, point):
        distance = self.distance_from(point)
        self.neighbours[distance] = point
        point.neighbours[distance] = self

    def is_neighbour_with(self, point):
        return point in self.neighbours.values()

    def distance_from(self, point):
        dimension = len(self.pos)
        accumulator = 0
        for i in range(dimension):
            delta = self.pos[i] - point.pos[i]
            accumulator += delta ** 2
        return accumulator ** 0.5


class Graph:
    def __init__(self, points, epsilon):
        self.points = points
        self.epsilon = epsilon

    def draw_with_matplotlib(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        dimension = len(self.points[0].pos)
        xs, ys, zs = [], [], []

        if dimension >= 3:
            for point in self.points:
                x, y, z = point.pos[:3]
                xs.append(x)
                ys.append(y)
                zs.append(z)
                for neighbour in point.neighbours.values():
                    neighbour_x, neighbour_y, neighbour_z = neighbour.pos[:3]
                    ax.plot(xs=[x, neighbour_x], ys=[y, neighbour_y], zs=[z, neighbour_z],
                            color='blue')
        elif dimension == 2:
            zs = [0] * len(self.points)
            for point in self.points:
                x, y = point.pos[:2]
                xs.append(x)
                ys.append(y)
                for neighbour in point.neighbours.values():
                    neighbour_x, neighbour_y = neighbour.pos[:2]
                    ax.plot(xs=[x, neighbour_x], ys=[y, neighbour_y], zs=[0, 0],
                            color='blue')

        ax.scatter(xs=xs, ys=ys, zs=zs, color='deeppink')
        plt.show()

    def create_edges(self):
        noise = []
        progress = 0
        for point in self.points:
            close_points = self.points_within_epsilon(point)
            if len(close_points) == 0:
                noise.append(point)
            else:
                for close_point in close_points:
                    if not point.is_neighbour_with(close_point):
                        point.become_neighbour(close_point)
                progress += 1
                print(f'Progress: {progress} / {len(self.points)} => {round(progress * 100 / len(self.points), 2)}%',
                      end='\r')
        for far_point in noise:
            closest_point = self.points[self.closest_point_index(far_point)]
            far_point.become_neighbour(closest_point)
            progress += 1
            print(f'Progress: {progress} / {len(self.points)} => {round(progress * 100 / len(self.points), 2)}%',
                  end='\r')

    def points_within_epsilon(self, point):
        close_points = []
        for a_point in self.points:
            if a_point is point:
                continue
            if point.distance_from(a_point) <= self.epsilon:
                close_points.append(a_point)
        return close_points

    def closest_point_index(self, point):
        closest_point_index = -1
        closest_point_distance = -1
        for i in range(len(self.points)):
            if self.points[i] is point:
                continue
            cur_distance = point.distance_from(self.points[i])
            if cur_distance > closest_point_distance:
                closest_point_index = i
                closest_point_distance = cur_distance
        return closest_point_index


def generate_id(size=10, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz-'):
    return ''.join(random.choice(alphabet) for i in range(size))


def generate_random_points(dimension, num):
    return [Point([random.uniform(-10.0, 10.0) for j in range(dimension)], generate_id()) for i in range(num)]


# To be substituted by real cluster data from kmeans branch:
c = generate_random_points(3, 100)
g = Graph(c, 5)
g.create_edges()
g.draw_with_matplotlib()
