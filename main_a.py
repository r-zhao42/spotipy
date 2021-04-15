from argparse import ArgumentParser
import pickle

from Spotify.song_ids import get_song_ids
from Spotify.song_features import get_features
from post_cluster import Graph_Save
from preprocess import Data
from Point import Point

import spotipy

if __name__ == '__main__':
    """
    Given input playlist of size n, adventure, and existing graphs,
    recommend n songs
    """
    print('Parsing args...', end='\r')
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--playlist-link', type=str)
    arg_parser.add_argument('--adventure', type=int)
    arg_parser.add_argument('--graphs-file-name', type=str)
    args = arg_parser.parse_args()
    print('Done parsing args!\n', end='\r')

    # Preprocessed data
    print('Restoring preprocessed data...', end='\r')
    data = Data()
    print('Done restoring preprocessed data!\n', end='\r')

    # Spotify
    print('Initializing Spotipy client...', end='\r')
    credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
        'daf1fbca87e94c9db377c98570e32ece', '1a674398d1bb44859ccaa4488df1aaa9')
    sp = spotipy.Spotify(client_credentials_manager=credentials_manager)
    print('Done initializing Spotipy client!\n', end='\r')

    # Restore centroid_to_graph
    print('Restoring Graphs...', end='\r')
    graphs_file = open(args.graphs_file_name, 'rb')
    centroid_to_graph_save = pickle.load(file=graphs_file)
    centroid_to_graph = dict()
    for centroid in centroid_to_graph_save:
        cur_graph_save = centroid_to_graph_save[centroid]
        restored_graph = cur_graph_save.restore()
        centroid_to_graph[centroid] = restored_graph
    print('Done restoring Graphs!\n', end='\r')

    # Get song ids from input playlist link
    # Get normalized features for each song id
    print('Getting song ids, features; and normalizing features...', end='\r')
    song_ids = get_song_ids(args.playlist_link, sp)
    song_id_to_features = []
    for song_id in song_ids:
        features = get_features(song_id, sp)
        normalized_features = data.normalize_value(features)
        song_id_to_features.append([song_id, normalized_features])
    print('Done getting song ids, features; and normalizing features!\n', end='\r')

    # ======================================
    # ABOVE IS OK
    # ======================================

    # ++++++++++++++++++++++++++++++++++++++
    # NEW: song_to_centroid
    # ++++++++++++++++++++++++++++++++++++++
    song_to_centroid = dict()
    for song in song_id_to_features:
        cur_song_id, cur_song_features = song
        is_in_dataset = False
        corresponding_centroid = None
        for centroid in centroid_to_graph:
            if not is_in_dataset:
                cur_graph = centroid_to_graph[centroid]
                cur_graph_point_ids = [point.id for point in cur_graph.points]
                if cur_song_id in cur_graph_point_ids:
                    is_in_dataset = True
                    corresponding_centroid = centroid
        if is_in_dataset:
            # If song in dataset:
            song_to_centroid[cur_song_id] = corresponding_centroid
        else:
            # If song not in dataset, find closest centroid
            closest_centroid = None
            closest_centroid_distance = None
            cur_point = Point(pos=cur_song_features, point_id=cur_song_id)
            for centroid in centroid_to_graph:
                distance_to_centroid = cur_point.distance_from(centroid)
                if closest_centroid_distance == None or distance_to_centroid < closest_centroid_distance:
                    closest_centroid = centroid
                    closest_centroid_distance = distance_to_centroid
            song_to_centroid[cur_song_id] = closest_centroid

    # ++++++++++++++++++++++++++++++++++++++
    # NEW: Make recommendations based on song_to_centroid
    # Convert to centroid_to_songs first to avoid duplicate recommendations
    # ++++++++++++++++++++++++++++++++++++++
    centroid_to_songs = dict()
    for song in song_to_centroid:
        corresponding_centroid = song_to_centroid[song]
        if corresponding_centroid in centroid_to_songs:
            centroid_to_songs[corresponding_centroid].extend([song])
        else:
            centroid_to_songs[corresponding_centroid] = [song]

    # --------------------------------------
    # DEPRECATED
    # --------------------------------------
    # For each song in song_id_to_features,
    # find out which Graph centroid the song is closest to
    """
    print('Finding the closest Graph centroid for each song...', end='\r')
    centroid_to_songs = dict()      # Centroid (Point) mapping to list of song ids
    for song in song_id_to_features:
        closest_centroid = None
        closest_centroid_distance = None
        # Represent current song as a point to use
        cur_song_id, cur_song_features = song
        cur_point = Point(pos=cur_song_features, point_id=cur_song_id)
        for centroid in centroid_to_graph:
            distance_to_centroid = cur_point.distance_from(centroid)
            if closest_centroid_distance == None or distance_to_centroid < closest_centroid_distance:
                closest_centroid = centroid
                closest_centroid_distance = distance_to_centroid
        if closest_centroid in centroid_to_songs:
            centroid_to_songs[closest_centroid].append(cur_point.id)
        else:
            centroid_to_songs[closest_centroid] = [cur_point.id]
    print('Done finding the closest Graph centroid for each song!\n', end='\r')
    """

    # For each centroid in centroid_to_songs:
    # - g = centroid_to_graph[centroid]
    # - songs centroid_to_songs[centroid]
    # - Use songs as input to g to make recommendations
    # Combine all recommendations
    print('Making recommendations...', end='\r')
    all_recommendations = []
    for centroid in centroid_to_songs:
        cur_input_songs = centroid_to_songs[centroid]
        cur_graph = centroid_to_graph[centroid]
        recommendations, fails = cur_graph.recommend(
            input_song_ids=cur_input_songs, adventure=args.adventure)
        all_recommendations.extend(recommendations)
    print('Done making recommendations!')

    out_file = open('Recommendations.txt', 'w')
    for recommendation in all_recommendations:
        out_file.write(f'{recommendation}\n')
    # print(f'{len(all_recommendations)}Recommendations: ', all_recommendations)
