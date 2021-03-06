from argparse import ArgumentParser
import pickle

# from Spotify.song_ids import get_song_ids
# from Spotify.song_features import get_features
from spotify_client import Spotify_Client
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
    spotify_instance = Spotify_Client()
    song_ids = spotify_instance.get_song_ids(args.playlist_link)
    # song_ids = get_song_ids(args.playlist_link, sp)
    song_id_to_features = []
    for song_id in song_ids:
        # features = get_features(song_id, sp)
        features = spotify_instance.get_song_features(song_id)
        normalized_features = data.normalize_value(features)
        song_id_to_features.append([song_id, normalized_features])
    print('Done getting song ids, features; and normalizing features!\n', end='\r')

    # Match each song with a graph
    # - If the song can be found in Graph_Final.pickle / Graph_Final_Evolve.pickle:
    #       Match song with graph
    # - If the song cannot be found:
    #       Match song with closest graph (by checking distance to graph centroid)
    #       And mutate Graph (to be saved)
    print('Matching songs with graphs...', end='\r')
    song_to_centroid = dict()
    graph_mutate = False
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
            graph_mutate = True     # Here graph_mutate means: Graph will mutate
            closest_centroid = None
            closest_centroid_distance = None
            cur_point = Point(pos=cur_song_features, point_id=cur_song_id)
            for centroid in centroid_to_graph:
                distance_to_centroid = cur_point.distance_from(centroid)
                if closest_centroid_distance == None or distance_to_centroid < closest_centroid_distance:
                    closest_centroid = centroid
                    closest_centroid_distance = distance_to_centroid
            song_to_centroid[cur_song_id] = closest_centroid
    # Before making recommendations:
    # Convert song_to_centroid => centroid_to_songs
    # to avoid duplicate recommendations
    centroid_to_songs = dict()
    for song in song_to_centroid:
        corresponding_centroid = song_to_centroid[song]
        if corresponding_centroid in centroid_to_songs:
            centroid_to_songs[corresponding_centroid].extend([song])
        else:
            centroid_to_songs[corresponding_centroid] = [song]
    print('Done matching songs with graphs!\n', end='\r')

    # For each centroid in centroid_to_songs:
    # - g = centroid_to_graph[centroid]
    # - songs = centroid_to_songs[centroid]
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
    print('Done making recommendations!\n', end='\r')

    # Write recommendations to file
    print('Writing to Recommendations.txt...', end='\r')
    out_file = open('Recommendations.txt', 'w')
    for recommendation in all_recommendations:
        out_file.write(f'{recommendation}\n')
    print('Done Writing to Recommendations.txt!\n', end='\r')

    # If graph(s) mutated: Save to Graph_Final_Evolve.pickle
    # Unlike before, here graph_mutate means: Graph mutated
    if graph_mutate:
        print('Graph(s) were mutated during the recommendation process,', end=' ')
        print('because the input playlist included song(s) that were not found in the graph file.\n', end='\r')
        print('Saving mutated Graphs to Graph_Final_Evolve.pickle...')
        centroid_to_graph_save = dict()
        for centroid in centroid_to_graph:
            cur_graph = centroid_to_graph[centroid]
            cur_graph_save = Graph_Save()
            cur_graph_save.save(cur_graph)
            centroid_to_graph_save[centroid] = cur_graph_save
        save_file = open('Graph_Final_Evolve.pickle', 'wb')
        pickle.dump(obj=centroid_to_graph_save, file=save_file, protocol=pickle.HIGHEST_PROTOCOL)
        save_file.close()
        print('Done saving mutated Graphs to Graph_Final_Evolve.pickle!')
    else:
        print('Graph(s) were not mutated during the recommendation process,', end=' ')
        print('because all songs in the input playlist were found in the graph file.\n', end='\r')

    print("Process is exiting...")
