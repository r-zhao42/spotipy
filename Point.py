class Point:
    def __init__(self, pos, point_id='NA'):
        self.pos = pos
        self.id = point_id
        self.neighbours = dict()  # distance to Point

    def __repr__(self):
        return str(self.id)

    def become_neighbour(self, point):
        distance = self.distance_from(point)
        while distance in self.neighbours:
            distance += 10 ** -300
        self.neighbours[distance] = point
        point.neighbours[distance] = self

    def is_neighbour_with(self, point):
        return point in self.neighbours.values()

    def get_neighbour(self, distance):
        return self.neighbours[distance]

    def distance_from(self, point):
        dimension = len(self.pos)
        accumulator = 0
        for i in range(dimension):
            delta = self.pos[i] - point.pos[i]
            accumulator += delta ** 2
        return accumulator ** 0.5
