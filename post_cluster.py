import random
from collections import deque
import pickle
# import sys
from argparse import ArgumentParser
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import spotipy
from Point import Point
from preprocess import Data
from Spotify.song_features import get_features
from k_means import KMeansAlgo
from typing import Any

# Fallback if pickling to / unpickling from custom Graph_Save object doesn't work
# sys.setrecursionlimit(100000)

DATA = Data()
CLIENT_CREDENTIALS_MANAGER = spotipy.oauth2.SpotifyClientCredentials(
    'daf1fbca87e94c9db377c98570e32ece', '1a674398d1bb44859ccaa4488df1aaa9')
SPOTIPY = spotipy.Spotify(client_credentials_manager=CLIENT_CREDENTIALS_MANAGER)


class Graph:
    """
    Represents the an individual graph of song vertices

    Instance Attributes:
         - points: ...
         - epsilon: ...
         - id_point_mapping: ...
         - song_ids: ...


    """

    points: ...
    epsilon: int
    id_point_mapping: ...
    song_ids: ...

    def __init__(self, points=[], epsilon=-1) -> None:
        """Initializes Graph class"""
        self.points = points
        self.epsilon = epsilon
        self.id_point_mapping = {point.id: point for point in self.points}
        self.song_ids = list(self.id_point_mapping.keys())

    def draw_with_matplotlib(self) -> None:
        """Draws and opens a window to display the graph with matplotlib"""
        # Better way to plot lines would be to actually keep the edges as attribute
        # so each edge only gets rendered once.
        # Will fix if time allows.
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

    def draw_with_matplotlib_3d(self, attr_1: str, attr_2: str, attr_3: str) -> None:
        """ Draws and opens a window to display the graph with matplotlib but in 3D"""
        # Map input str to associated index in pos
        attr_1, attr_2, attr_3 = list(map(str.lower, [attr_1, attr_2, attr_3]))
        attribute_to_index = {'acousticness': 0, 'danceability': 1, 'energy': 2, 'duration(ms)': 3,
                              'instrumentalness': 4, 'valence': 5, 'tempo': 6, 'liveness': 7,
                              'loudness': 8, 'speechiness': 10, 'key': 11}

        x_i = attribute_to_index[attr_1]
        y_i = attribute_to_index[attr_2]
        z_i = attribute_to_index[attr_3]

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        dimension = len(self.points[0].pos)
        xs, ys, zs = [], [], []

        if dimension >= 3:
            for point in self.points:
                x, y, z = point.pos[x_i], point.pos[y_i], point.pos[z_i]
                xs.append(x)
                ys.append(y)
                zs.append(z)
                for neighbour in point.neighbours.values():
                    neighbour_x, neighbour_y, neighbour_z = neighbour.pos[:3]
                    ax.plot(xs=[x, neighbour_x], ys=[y, neighbour_y], zs=[z, neighbour_z],
                            color='blue')

        ax.scatter(xs=xs, ys=ys, zs=zs, color='deeppink')
        plt.show()

    def save_state(self, file_name) -> None:
        """
        Saves the current state into a pickle file
        """
        pickle_file = open(f'{file_name}.pickle', 'wb')
        to_save = Graph_Save()
        to_save.save(self)
        pickle.dump(obj=to_save, file=pickle_file, protocol=pickle.HIGHEST_PROTOCOL)
        # Fallback:
        # pickle.dump(obj=self, file=pickle_file, protocol=pickle.HIGHEST_PROTOCOL)
        pickle_file.close()

    def restore_from_state(self, file_name) -> None:
        """
        Restores previously saved state from a pickle file

        """
        pickle_file = open(f'{file_name}.pickle', 'rb')
        restored = pickle.load(file=pickle_file)
        restored_graph = restored.restore()
        # Fallback:
        # restored_graph = pickle.load(file=pickle_file)
        pickle_file.close()
        self.points = restored_graph.points
        self.epsilon = restored_graph.epsilon
        self.id_point_mapping = {point.id: point for point in self.points}
        self.song_ids = list(self.id_point_mapping.keys())
        # Fallback:
        # self.id_point_mapping = restored_graph.id_point_mapping
        # self.song_ids = restored_graph.song_ids

    def init_edges(self) -> None:
        """Initializes edges within the graph class"""
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
                print(f'Progress: {progress} / {len(self.points)} => '
                      f'{round(progress * 100 / len(self.points), 2)}%',
                      end='\r')
        for far_point in noise:
            closest_point = self.points[self.closest_point_index(far_point)]
            far_point.become_neighbour(closest_point)
            progress += 1
            print(f'Progress: {progress} / {len(self.points)} => '
                  f'{round(progress * 100 / len(self.points), 2)}%',
                  end='\r')
        print('\r')

    def points_within_epsilon(self, point: ...) -> ...:
        """Returns the close points, which are within the self.epsilon"""
        close_points = []
        for a_point in self.points:
            if a_point is point:
                continue
            if point.distance_from(a_point) <= self.epsilon:
                close_points.append(a_point)
        return close_points

    def closest_point_index(self, point) -> ...:
        """
        Returns the index of the closest points

        """
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

    def recommend(self, input_song_ids: ..., adventure: ...) -> ...:
        """
        This is the function responsible for recommendations...

        """
        recommendations = []
        fails = 0      # too many fails means cluster too small and/or adventure too big
        for input_song_id in input_song_ids:
            if input_song_id in self.song_ids:
                blacklist = recommendations + input_song_ids
                res = self.bfs(input_song_id, adventure, blacklist)
                if res['success']:
                    recommendations.append(res['data'])
                else:
                    fails += 1
                    continue
            else:
                # Handle song not in graph
                pos = self.get_new_song_pos(input_song_id)
                new_song = Point(pos, input_song_id)
                self.init_new_point(new_song)

                blacklist = recommendations + input_song_ids
                res = self.bfs(input_song_id, adventure, blacklist)
                if res['success']:
                    recommendations.append(res['data'])
                else:
                    fails += 1
                    continue

        # Handle fails: Find random song in graph
        # Will still be good results overall because graph is a cluster from kmeans,
        # songs in a given cluster share explicable/inexplicable resemblance
        if fails:
            shuffled_songs = random.sample(self.song_ids, len(self.song_ids))
            counter = 0
            for i in range(fails):
                random_song = shuffled_songs[counter]
                blacklist = recommendations + input_song_ids
                while random_song in blacklist:
                    random_song = shuffled_songs[counter]
                    counter += 1
                    if counter > len(self.song_ids):
                        raise Exception('Cluster too small / Asking for too many songs')
                recommendations.append(random_song)

        return recommendations, fails

    def bfs(self, root_song_id: ..., adventure: ..., blacklist: ...) -> ...:
        """
        ...
        """
        queue = deque()
        visited = set()
        visited.add(root_song_id)
        queue.append((root_song_id, 0))
        depth = 0
        while queue:
            cur_song_id, cur_depth = queue.popleft()

            # Criteria
            not_root = cur_song_id != root_song_id
            adventure_ok = cur_depth == adventure
            not_blacklisted = cur_song_id not in blacklist
            if not_root and adventure_ok and not_blacklisted:
                return {'success': True, 'data': cur_song_id}

            if cur_depth > depth:
                depth += 1

            cur_song = self.id_point_mapping[cur_song_id]
            neighbour_keys = sorted(list(cur_song.neighbours.keys()))   # This is distances
            for neighbour_key in neighbour_keys:
                neighbour = cur_song.get_neighbour(neighbour_key)
                if neighbour.id not in visited:
                    visited.add(neighbour.id)
                    queue.append((neighbour.id, depth + 1))

        return {'success': False}

    def get_new_song_pos(self, song_id: str) -> ...:
        """Returns the new position/features/attributes of a new song"""
        spotify_pos = get_features(song_id, SPOTIPY)
        normalized_pos = DATA.normalize_value(spotify_pos)
        return normalized_pos

    def init_new_point(self, new_point: ...) -> None:
        """
        Initializes the new songs with their new positions
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # MAKE SURE THE NEW POINT ACTUALLY BELONGS IN THIS CLUSTER. I.E. CLOSEST TO
        # THE CENTROID OF THIS CLUSTER! NEED TO IMPLEMENT FROM KMEANS!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        assert new_point.id not in self.song_ids, "New song's id already in self.song_ids"
        print('Initializing new point...', end='\r')
        self.points.append(new_point)
        self.id_point_mapping[new_point.id] = new_point
        self.song_ids.append(new_point.id)
        close_points = self.points_within_epsilon(new_point)
        if len(close_points) == 0:
            closest_point = self.points[self.closest_point_index(new_point)]
            new_point.become_neighbour(closest_point)
        else:
            for close_point in close_points:
                new_point.become_neighbour(close_point)
        num_edges = len(close_points) if len(close_points) != 0 else 1
        print(f'Initialized new point with {num_edges} edges!')


class Graph_Save:
    """This is a class, made custom, to minimize the recursion of pickling because our dataset
    is too big and we have done this to avoid recursion error

    Instance Attributes:
        - points: ...
        - edges: ...
        - epsilon: ...

    """

    points: ...
    edges: ...
    epsilon: ...

    # To minimize .pickle file size and avoid pickle recursion error
    def __init__(self) -> None:
        """Initializes the Graph_Save class"""
        self.points = set()
        self.edges = set()
        self.epsilon = -1

    def save(self, graph: Graph) -> None:
        """A method designed to save the graph"""
        points = set()
        edges = set()
        for point in graph.points:
            points.add((tuple(point.pos), point.id))
            for neighbour_distance in point.neighbours:
                neighbour = point.neighbours[neighbour_distance]
                edges.add(tuple(sorted([point.id, neighbour.id])))
        self.points = points
        self.edges = edges
        self.epsilon = graph.epsilon

    def restore(self) -> Graph:
        """A method designed to restore the graph"""
        points = []
        id_point_mapping = dict()
        for point in self.points:
            point_pos, point_id = point
            point_obj = Point(point_pos, point_id)
            points.append(point_obj)
            id_point_mapping[point_id] = point_obj
        for edge in self.edges:
            point_id, neighbour_id = edge
            point_obj = id_point_mapping[point_id]
            neighbour_obj = id_point_mapping[neighbour_id]
            point_obj.become_neighbour(neighbour_obj)
        return Graph(points=points, epsilon=self.epsilon)


def generate_id(size=16,
                alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz-') -> Any:
    """
    Generated ids for testing
    """
    return ''.join(random.choice(alphabet) for i in range(size))


def generate_random_points(dimension, num) -> Any:
    """Generates random points for testing"""
    return [Point([random.uniform(-10.0, 10.0)
                   for j in range(dimension)], generate_id()) for i in range(num)]


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['pickle', 'tkinter', 'PIL', 'urllib', 'webbrowser',
                          'Recommendation', 'Spotify.Spotify_client', 'Spotify.song_features',
                          'k_means', 'spotipy', 'argparse', 'song_tkinter', 'preprocess',
                          'post_cluster'],
        'allowed-io': [],
        # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })

    """
    Given kmeans clusters:
    - Make each cluster into Graph object
    - Initialize edges for each Graph
    - Save all clusters (mapping of Graph centroid to Graph_Save)
    """
    # Parse args
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--epsilon', type=float)
    arg_parser.add_argument('--input-kmeans-clusters-file-name', type=str)
    arg_parser.add_argument('--output-graphs-file-name', type=str)
    args = arg_parser.parse_args()

    # Restore kmeans
    kmeans_cluster_file = open(args.input_kmeans_clusters_file_name, 'rb')
    centroid_to_cluster = pickle.load(file=kmeans_cluster_file)

    # Create Graphs from clusters
    # Initialize edges for each Graph
    # Map centroid to Graph_Save
    centroid_to_graph_save = dict()
    for centroid in centroid_to_cluster:
        cur_cluster = centroid_to_cluster[centroid]
        cur_graph = Graph(points=cur_cluster, epsilon=args.epsilon)
        cur_graph.init_edges()
        cur_graph_save = Graph_Save()
        cur_graph_save.save(cur_graph)
        centroid_to_graph_save[centroid] = cur_graph_save

    # Pickle centroid_to_graph_save
    save_file = open(args.output_graphs_file_name, 'wb')
    pickle.dump(obj=centroid_to_graph_save, file=save_file, protocol=pickle.HIGHEST_PROTOCOL)
    save_file.close()

    # Dev only
    """
    # Get a cluster (From kmeans or randomly generate)
    pickle_file = open(f'Cluster_Final.pickle', 'rb')
    centroid_to_clusters = pickle.load(file=pickle_file)
    clusters = list(centroid_to_clusters.values())
    smallest_cluster = None
    for cluster in clusters:
        if smallest_cluster == None or len(cluster) < len(smallest_cluster):
            smallest_cluster = cluster
    c = smallest_cluster
    # c = generate_random_points(3, 100)

    # Make graph
    g = Graph(points=c, epsilon=0.4)
    # g = Graph(points=c, epsilon=7)    # For randomly generated cluster
    g.init_edges()
    # g.draw_with_matplotlib()

    # Save 
    g.save_state(file_name='Graph_Test')

    # Take first ten songs from cluster and use as input to recommend songs
    input_songs = [song.id for song in c[:10]]
    recommendations, fails = g.recommend(input_song_ids=input_songs, adventure=5)
    print('Recommendations:', recommendations)
    print('Fails:', fails)

    # Assert: Input is not found in recommendation
    input_in_recommendation = set(input_songs).intersection(set(recommendations)) != set()
    assert not input_in_recommendation

    # Test unpickling
    g_copy = Graph()
    g_copy.restore_from_state(file_name='Graph_Test')

    # Assert: Graph restores properly
    points_restored = set(map(str, g.points)) == set(map(str, g_copy.points))
    assert points_restored
    epsilon_restored = g.epsilon == g_copy.epsilon
    assert epsilon_restored
    id_point_mapping_restored = all(str(g.id_point_mapping[song_id]) == str(
        g_copy.id_point_mapping[song_id]) for song_id in g.id_point_mapping)
    assert id_point_mapping_restored
    song_ids_restored = set(g.song_ids) == set(g_copy.song_ids)
    assert song_ids_restored
    """


