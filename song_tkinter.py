"""
This file is responsible to create a user-interface for our Song Recommendation program using
Tkinter.

"""

import pickle
from typing import Any, List, Dict, Optional
import tkinter as tk
from tkinter import ttk as ttk
from PIL import ImageTk, Image
import urllib
import webbrowser
from Recommendation import Recommendation
from Spotify.Spotify_client import SpotifyClient
from Spotify.song_features import get_features
from k_means import KMeansAlgo


class UserPlaylistEntry:
    """
    This is a class responsible for creating a Tkinter window, and get a the playlist link
    from the user, which is later stored and used within the program to generate another playlist.

    Instance Attributes:
        - root: This instance attribute is used for storing the root of the Tkinter window

    """

    root: Any

    def __init__(self, root: Any, core: dict) -> None:
        # We first initialize the root of our tkinter window
        self.root = root

        # Initialize data needed to recommend
        self.data_obj = core['data_obj']
        self.sp = core['sp']
        self.centroid_to_graph = core['centroid_to_graph']
        self.ordered_centroids = list(self.centroid_to_graph.keys())

        # Here we initialize the rest of the class attributes that are user inputs to empty strings
        self.playlist_entry = ''
        self.scale_entry = ''
        # self.playlist_length_entry = ''
        self.new_playlist_name = ''
        self.visualization = ''
        self.att_1 = ''
        self.att_2 = ''
        self.att_3 = ''
        self.graph_int = 0

        self._image = Image.open('Spotify-Logo.png').resize((140, 100))

        self._link_entry = tk.Entry(self.root, borderwidth=10, selectbackground='#1DB954')

        self._slider = tk.Scale(self.root, from_=1, to=10, tickinterval=1, orient='horizontal',
                                bg="#1DB954",
                                fg="BLACK", sliderlength=20, length=200)

        self._new_playlist_name_entry = tk.Entry(self.root, borderwidth=10,
                                                 selectbackground='#1DB954')

        # self.length_entry = tk.Entry(self.root, borderwidth=10, selectbackground='#1DB954')

        self._inner_string = tk.StringVar(self.root)
        self._inner_string.set('Choose Visualization')
        dimension_options = ["K-means", "Individual Graph"]
        self._dimension_menu = tk.OptionMenu(self.root, self._inner_string, *dimension_options)

        self._dimension_menu.config(bg='#1DB954')

        attribute_options = ['Acousticness', 'Danceability', 'Energy', 'Duration(ms)',
                             'Instrumentalness', 'Valence', 'Tempo', 'Liveness', 'Loudness',
                             'Speechness', 'Key']
        self._inner_string_att1 = tk.StringVar(self.root)
        self._inner_string_att1.set('Attribute 1')
        self._attribute1_menu = tk.OptionMenu(self.root, self._inner_string_att1,
                                              *attribute_options)
        self._attribute1_menu.config(bg='#1DB954')

        self._inner_string_att2 = tk.StringVar(self.root)
        self._inner_string_att2.set('Attribute 2')
        self._attribute2_menu = tk.OptionMenu(self.root, self._inner_string_att2,
                                              *attribute_options)

        self._attribute2_menu.config(bg='#1DB954')

        self._inner_string_att3 = tk.StringVar(self.root)
        self._inner_string_att3.set('Attribute 3')
        self._attribute3_menu = tk.OptionMenu(
            self.root, self._inner_string_att3, *attribute_options)

        self._attribute3_menu.config(bg='#1DB954')

        self._graph_int_entry = tk.Entry(self.root, borderwidth=10, selectbackground='#1DB954')

    def run_window(self) -> None:
        """Runs a new Tkinter window"""

        self.root.title('Spotify Recommender')

        sp_logo = ImageTk.PhotoImage(self._image)
        label = tk.Label(self.root, image=sp_logo)

        # We need to save the reference to the image
        label.image = sp_logo
        label.grid()

        # tk.Label(self.root, image=tkimage, font='center').grid()

        tk.Label(self.root, text='Enter the link of your Spotify playlist below : ',
                 font=("Proxima nova", "9", "bold")).grid()

        self._link_entry.grid(ipadx=30)

        tk.Label(self.root, text="How adventurous are you feeling today?",
                 font=("Proxima nova", "9", "bold")).grid()

        self._slider.grid()

        # tk.Label(self.root,
        #          text='Enter the desired length of your new playlist (MAX 100) : ',
        #          font=("Proxima nova", "9", "bold")).grid()

        # self.length_entry.grid(ipadx=30)

        tk.Label(self.root, text='What do you want to name your new playlist? ',
                 font=("Proxima nova", "9", "bold")).grid()

        self._new_playlist_name_entry.grid(ipadx=30)

        tk.Button(self.root, text='ENTER', command=self.get_user_input, padx=5,
                  pady=5, bg='#1DB954').grid()

        tk.Label(self.root, text='FOR VISUALIZATION \n Please choose a dimension.',
                 font=("Proxima nova", "9", "bold")).grid(pady=30)

        self._dimension_menu.grid()

        tk.Label(self.root, text='Please choose your first attribute',
                 font=("Proxima nova", "9", "bold")).grid()
        self._attribute1_menu.grid()

        tk.Label(self.root, text='Please choose your second different attribute',
                 font=("Proxima nova", "9", "bold")).grid()
        self._attribute2_menu.grid()

        tk.Label(self.root, text='IF APPLICABLE, choose your third different attribute',
                 font=("Proxima nova", "9", "bold")).grid()
        self._attribute3_menu.grid()

        tk.Label(self.root, text='IF CHOSEN GRAPH: Enter an integer 1-100',
                 font=("Proxima nova", "9", "bold")).grid()
        self._graph_int_entry.grid()

        tk.Button(self.root, text='VISUALIZE', command=self.visualize, padx=5,
                  pady=5, bg='#1DB954').grid(pady=15)

    def get_user_input(self) -> None:
        """Responsible for storing the link inputted by the user

        It also quits the window if all three user inputs are entered
        """

        # Here we update the playlist entry attribute
        self.playlist_entry = self._link_entry.get()

        # Here we update the scale entry attribute
        self.scale_entry = self._slider.get()

        # Update the desired new playlists name
        self.new_playlist_name = self._new_playlist_name_entry.get()

        # Omitting regex checks
        if self.playlist_entry != '' and self.scale_entry != '' \
                and self.new_playlist_name != '':

            tk.Label(self.root, text='YOUR *PLAYLIST* INFORMATION HAS BEEN RECORDED. \n THANK YOU!',
                     font=("Proxima nova", "9", "bold"), fg='white', bg='black').grid()

            recommended_song_ids = Recommendation(self.playlist_entry,
                                                  self.scale_entry,
                                                  self.data_obj,
                                                  self.sp,
                                                  self.centroid_to_graph).action()

            new_playlist_link = SpotifyClient(recommended_song_ids, self.new_playlist_name)._url

            aves = [0] * 9      # 9 features
            num_songs = 0
            for song_id in recommended_song_ids:
                num_songs += 1
                features = self.data_obj.normalize_value(get_features(song_id, self.sp))
                # Removing duration(ms) and key
                cols_removed_features = features[:3] + features[4:10]
                for i in range(len(aves)):
                    aves[i] += cols_removed_features[i]

            aves = list(map(lambda ave: round(ave / num_songs * 100), aves))

            output_playlist_summary = {'Acousticness': aves[0],
                                       'Danceability': aves[1],
                                       'Energy': aves[2],
                                       'Instrumentalness': aves[3],
                                       'Valence': aves[4],
                                       'Tempo': aves[5],
                                       'Liveness': aves[6],
                                       'Loudness': aves[7],
                                       'Speechiness': aves[8]}

            output_root = tk.Toplevel()
            output_window = NewPlaylistOutput(output_root,
                                              new_playlist_link,
                                              output_playlist_summary)
            output_window.run_window()
            output_root.mainloop()

    def visualize(self) -> None:
        """A method that is designed to be used as a button command for the visualize button at the
        bottom of the Tkinter window"""

        self.visualization = self._inner_string.get()
        self.att_1 = self._inner_string_att1.get()
        self.att_2 = self._inner_string_att2.get()
        self.att_3 = self._inner_string_att3.get()
        self.graph_int = self._graph_int_entry.get()

        # This is the case where we did not select Graph Visualization, in this case I am doing this
        # in order not to receive type error when checking if self.graph > 100 on line 200
        if self.graph_int == '':
            self.graph_int = 0
        elif int(self.graph_int) > 100:
            # If the input is higher than 100, automatically set to the highest (100)
            self.graph_int = 100
        else:
            # graph_int is valid
            self.graph_int = int(self.graph_int)

        if (self.visualization != 'Choose Visualization' and self.visualization != '') and \
                (self.att_1 != '' and self.att_1 != 'Attribute 1') and \
                (self.att_2 != '' and self.att_2 != 'Attribute 2') and \
                (self.att_3 != '' and self.att_3 != 'Attribute 3'):

            if self.visualization == 'K-means':
                clusters_file = open('Cluster_Final.pickle', 'rb')
                centroid_to_clusters = pickle.load(file=clusters_file)
                k_means = KMeansAlgo(path="Data/normalized_data_final.csv", k=1)
                k_means.clusters = centroid_to_clusters
                k_means.centroids = list(k_means.clusters)
                k_means.graph_3d(self.att_1, self.att_2, self.att_3, n=5)

            else:   # self.visualization == 'Individual Graph'
                centroid = self.ordered_centroids[self.graph_int - 1]
                graph = self.centroid_to_graph[centroid]
                graph.draw_with_matplotlib_3D(self.att_1, self.att_2, self.att_3)
        else:
            print('Invalid visualization options input.\nPlease select all options.')


class NewPlaylistOutput:
    """
    This class is responsible for outputting the link to the final generated playlist, for the user
    to open and listen to.

    Instance Attributes:
        - root: This instance attribute is used for storing the root of the Tkinter window

        - link: This is the link to the newly generated playlist
    """
    root: Any
    link: str
    old_averages: Dict[str, float]

    def __init__(self, root: Any, link: str, old_average: Dict[str, float]) -> None:
        """Initialize the class and its attributes"""

        self.root = root
        self.link = link
        self.old_averages = old_average

        self._image = Image.open('Spotify-Logo.png').resize((140, 100))

        self._link_button = tk.Button(self.root, text='OPEN LINK!', command=self.open_link, padx=5,
                                      pady=5, bg='#1DB954')

        style_acoustic = ttk.Style()
        style_acoustic.theme_use('alt')
        style_acoustic.configure("orange.Horizontal.TProgressbar", foreground='orange',
                                 background='orange')

        self._acoustic_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300,
                                                      style='orange.Horizontal.TProgressbar')

        style_dance = ttk.Style()
        style_dance.theme_use('alt')
        style_dance.configure("red.Horizontal.TProgressbar", foreground='red',
                              background='red')

        self._dance_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300,
                                                   style='red.Horizontal.TProgressbar')

        style_energy = ttk.Style()
        style_energy.theme_use('alt')
        style_energy.configure("blue.Horizontal.TProgressbar", foreground='blue',
                               background='blue')

        self._energy_progress_bar = ttk.Progressbar(self.root, style='blue.Horizontal.TProgressbar',
                                                    length=300, orient='horizontal')

        style_instrument = ttk.Style()
        style_instrument.theme_use('alt')
        style_instrument.configure("yellow.Horizontal.TProgressbar", foreground='yellow',
                                   background='yellow')

        self._instrument_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300,
                                                        style="yellow.Horizontal.TProgressbar")

        style_valence = ttk.Style()
        style_valence.theme_use('alt')
        style_valence.configure("violet.Horizontal.TProgressbar", foreground='violet',
                                background='violet')

        self._valence_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300,
                                                     style="violet.Horizontal.TProgressbar")

        style_tempo = ttk.Style()
        style_tempo.theme_use('alt')
        style_tempo.configure("turquoise.Horizontal.TProgressbar", foreground='turquoise',
                              background='turquoise')

        self._tempo_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300,
                                                   style="turquoise.Horizontal.TProgressbar")

        style_liveness = ttk.Style()
        style_liveness.theme_use('alt')
        style_liveness.configure("pink.Horizontal.TProgressbar", foreground='pink',
                                 background='pink')

        self._liveness_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300,
                                                      style="pink.Horizontal.TProgressbar")

        style_loud = ttk.Style()
        style_loud.theme_use('alt')
        style_loud.configure("lavender.Horizontal.TProgressbar", foreground='lavender',
                             background='lavender')

        self._loud_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300,
                                                  style="lavender.Horizontal.TProgressbar")

        style_loud = ttk.Style()
        style_loud.theme_use('alt')
        style_loud.configure("green.Horizontal.TProgressbar", foreground='green',
                             background='green')

        self._speech_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300,
                                                    style="green.Horizontal.TProgressbar")

    def run_window(self) -> None:
        """
        Runs the tkinter window which displays the link to the generated playlist

        """

        self.root.title('Spotify Recommender')

        sp_logo = ImageTk.PhotoImage(self._image)
        label = tk.Label(self.root, image=sp_logo)

        # We need to save the reference to the image
        label.image = sp_logo
        label.grid()

        tk.Label(self.root, text='Here is the link to your new playlist!',
                 font=("Proxima nova", "9", "bold")).grid()
        tk.Label(self.root, text=self.link, bd=20, font=("Proxima nova", "9", "bold")).grid()

        self._link_button.grid()

        tk.Label(self.root, text="DID YOU KNOW?! \n These are your old playlist's stats:",
                 font=("Proxima nova", "9", "bold")).grid(pady=25)

        tk.Label(self.root, text=f"Avr. Acousticness: {self.old_averages['Acousticness']}",
                 font=("Proxima nova", "9", "bold")).grid(pady=5)
        self._acoustic_progress_bar['value'] = self.old_averages['Acousticness']
        self._acoustic_progress_bar.grid(pady=5)

        tk.Label(self.root, text=f"Avr. Danceability: {self.old_averages['Danceability']}",
                 font=("Proxima nova", "9", "bold")).grid(pady=5)
        self._dance_progress_bar['value'] = self.old_averages['Danceability']
        self._dance_progress_bar.grid(pady=5)

        tk.Label(self.root, text=f"Avr. Energy: {self.old_averages['Energy']}",
                 font=("Proxima nova", "9", "bold")).grid(pady=5)
        self._energy_progress_bar['value'] = self.old_averages['Energy']
        self._energy_progress_bar.grid(pady=5)

        tk.Label(self.root, text=f"Avr. Instrumentalness: {self.old_averages['Instrumentalness']}",
                 font=("Proxima nova", "9", "bold")).grid(pady=5)
        self._instrument_progress_bar['value'] = self.old_averages['Instrumentalness']
        self._instrument_progress_bar.grid(pady=5)

        tk.Label(self.root, text=f"Avr. Valence: {self.old_averages['Valence']}",
                 font=("Proxima nova", "9", "bold")).grid(pady=5)
        self._valence_progress_bar['value'] = self.old_averages['Valence']
        self._valence_progress_bar.grid(pady=5)

        tk.Label(self.root, text=f"Avr. Tempo: {self.old_averages['Tempo']}",
                 font=("Proxima nova", "9", "bold")).grid(pady=5)
        self._tempo_progress_bar['value'] = self.old_averages['Tempo']
        self._tempo_progress_bar.grid(pady=5)

        tk.Label(self.root, text=f"Avr. Liveness: {self.old_averages['Liveness']}",
                 font=("Proxima nova", "9", "bold")).grid(pady=5)
        self._liveness_progress_bar['value'] = self.old_averages['Liveness']
        self._liveness_progress_bar.grid(pady=5)

        tk.Label(self.root, text=f"Avr. Loudness: {self.old_averages['Loudness']}",
                 font=("Proxima nova", "9", "bold")).grid(pady=5)
        self._loud_progress_bar['value'] = self.old_averages['Loudness']
        self._loud_progress_bar.grid(pady=5)

        tk.Label(self.root, text=f"Avr. Speechiness: {self.old_averages['Speechiness']}",
                 font=("Proxima nova", "9", "bold")).grid(pady=5)
        self._speech_progress_bar['value'] = self.old_averages['Speechiness']
        self._speech_progress_bar.grid(pady=5)

    def open_link(self) -> None:
        """Function that is used to be the command for the button of the tkinter window to go
        to the link of the new playlist"""

        webbrowser.open_new(self.link)


def calc_diff_btwn_playlists(old_playlist: List[list], new_playlist: List[list]) -> list[float]:
    """Calculates the difference between the old playlist inputted by the user and the
    new playlist provided by our algorithm

    Preconditions:
        - len(old_playlist) == len(new_playlist)
        - all([len(old_playlist[i]) == len(old_playlist[i + 1]) for i in range(len(old_playlist))])
        - _all_same_number([len(x) for x in old_playlist + new_playlist])


    >>> list1 = [[1.0, 1.0, 1.0, 1.0], [0.8, 0.8, 0.8, 0.8]]
    >>> list2 = [[1.1, 1.1, 1.2, 1.2], [0.5, 0.5, 0.7, 0.8]]
    >>> calc_diff_btwn_playlists(list1, list2)
    [0.2, 0.2, 0.15, 0.1]


    """
    columns = []

    # generate an empty list of lists to be used by the algorithm
    for _ in range(len(old_playlist[0])):
        columns.append([])

    # print(columns)
    index = 0

    for i in range(len(old_playlist)):
        for j in range(len(old_playlist[i])):
            diff = abs(old_playlist[i][j] - new_playlist[i][j])
            # print(diff)
            # print(columns)
            columns[j].append(diff)

            index += 0

    averages = []
    for z in range(len(columns)):
        avr = sum(columns[z]) / len(columns[z])
        averages.append(avr)

    return averages


def _all_same_number(lst: list) -> bool:
    """Returns whether all the elements in the list are the same number or not

    >>> my_lst = [1, 2, 3, 4, 5]
    >>> _all_same_number(my_lst)
    False
    >>> my_lst2 = [1, 1, 1, 1, 1, 1]
    >>> _all_same_number(my_lst2)
    True
    """

    for i in range(len(lst) - 1):
        if lst[i] != lst[i + 1]:
            return False

    return True


def get_input_playlist_averages() -> list[float]:
    """Get the averages of the columns for the user input"""

    pass


if __name__ == "__main__":
    root = tk.Tk()
    BE = UserPlaylistEntry(root)
    BE.run_window()
    root.mainloop()

    root2 = tk.Tk()
    # window = NewPlaylistOutput(root2, 'https://open.spotify.com/playlist/1zKz3iMcIOHicoacBa24jo?si=M4S5RXJQQ5CsjjYPLGWkRw', {'Acousticness': 80,
    #                                                                                                                          'Danceability': 50,
    #                                                                                                                          'Energy': 30,
    #                                                                                                                          'Instrumentalness': 10,
    #                                                                                                                          'Valence' : 55,
    #                                                                                                                          'Tempo': 40,
    #                                                                                                                          'Liveness': 95,
    #                                                                                                                          'Loudness': 60,
    #                                                                                                                          'Speechiness': 99})
    # window.run_window()
    # root2.mainloop()

    # import doctest
    # doctest.testmod()

    dict1 = {
        '6ya8ejoKgw906Y8LWclqrp': [0.0825, 0.671, 0.833, 233278, 0, 0.702, 79.351, 0.0726, -5.152,
                                   0.395, 5],
        '62vpWI1CHwFy7tMIcSStl8': [0.301, 0.692, 0.521, 292987, 0, 0.463, 100.45,
                                   0.0565, -8.465, 0.33, 10],
        '3wwo0bJvDSorOpNfzEkfXx': [0.172, 0.635, 0.537, 215381, 0, 0.383, 125.028, 0.418, -7.895,
                                   0.0832, 7], '40jxatV29fk82SAziDsPqN': [0.426, 0.594, 0.762,
                                                                          277813, 0, 0.588, 139.932,
                                                                          0.085, -7.951, 0.0899, 9],
        '1cZlBZwnwGPtYeRIeQcoFh': [0.0737, 0.769, 0.569, 216946, 0, 0.612, 146.062, 0.0571, -5.591,
                                   0.0786, 1],
        '4rgwri7LajWVZvdj2N81SS': [0.165, 0.943, 0.677, 145760, 0, 0.616, 112.001, 0.327, -6.033,
                                   0.246, 7],
        '4iVD0fTHGxV9JWloujsL3s': [0.0544, 0.604, 0.436, 361280, 0.000242, 0.239, 107.978, 0.162,
                                   -8.32, 0.188, 2],
        '3R9j8urSPiBbapNbyuSYkE': [0.0491, 0.6, 0.716, 175040, 0, 0.246, 180.165, 0.109, -5.554,
                                   0.384, 3],
        '0Fpen1PTuEnCmOJtUU9Iud': [0.0367, 0.85, 0.785, 343099, 0, 0.718, 145.063, 0.155, -4.963,
                                   0.345, 8],
        '7wBJfHzpfI3032CSD7CE2m': [0.00947, 0.487, 0.789, 270715, 4.05e-06, 0.0564, 150.007, 0.189,
                                   -3.69, 0.044, 8],
        '6NMtzpDQBTOfJwMzgMX0zl': [0.00146, 0.46, 0.686, 145588, 0, 0.252, 148.054, 0.375, -5.948,
                                   0.0367, 0],
        '27GmP9AWRs744SzKcpJsTZ': [0.0559, 0.852, 0.553, 205879, 0, 0.656, 142.079, 0.332, -7.286,
                                   0.187, 1],
        '50a8bKqlwDEqeiEknrzkTO': [0.0467, 0.892, 0.633, 195047, 0.000189, 0.459, 137.994, 0.139,
                                   -7.471, 0.0902, 8],
        '6LyAwkJsHlW7RQ8S1cYAtM': [0.733, 0.638, 0.4, 166093, 0.000133, 0.495, 150.133, 0.334,
                                   -11.212, 0.0425, 11],
        '49zD0wr2S3d0lZPib0K4e1': [0.0698, 0.874, 0.568, 237400, 1.38e-05, 0.46, 139.995, 0.149,
                                   -5.896, 0.224, 11],
        '6gBFPUFcJLzWGx4lenP6h2': [0.0847, 0.841, 0.728, 243837, 0, 0.43, 130.049, 0.149, -3.37,
                                   0.0484, 7],
        '577YBGuskWkVDCxZrLRB4v': [0.00127, 0.964, 0.487, 154024, 6.57e-06, 0.107, 127.05, 0.115,
                                   -6.071, 0.421, 10],
        '2FUNBaa5DwItJtYEBgAblU': [0.158, 0.89, 0.607, 233040, 0.000228, 0.224, 134.022, 0.118,
                                   -6.916, 0.124, 9],
        '3nAq2hCr1oWsIU54tS98pL': [0.0528, 0.557, 0.586, 181573, 7.33e-06, 0.0681, 96.091, 0.339,
                                   -4.57, 0.0382, 10],
        '39Yp9wwQiSRIDOvrVg7mbk': [0.233, 0.716, 0.537, 165978, 0, 0.28, 129.979, 0.157, -7.648,
                                   0.0514, 0],
        '4EWCNWgDS8707fNSZ1oaA5': [0.0515, 0.79, 0.647, 211000, 0, 0.654, 87.999, 0.248, -5.983,
                                   0.136, 10],
        '3s4mrPrEFFPF0LmAfutW0n': [0.0249, 0.784, 0.517, 200187, 1.44e-06, 0.206, 97.991, 0.155,
                                   -8.981, 0.209, 4],
        '7lAK3oHbfEnvUQWosrMMpR': [0.283, 0.785, 0.554, 150043, 3.4e-06, 0.144, 128.047, 0.116,
                                   -6.571, 0.0409, 0],
        '1ThmUihH9dF8EV08ku5AXN': [0.111, 0.935, 0.552, 145627, 0, 0.615, 99.993, 0.0952, -9.373,
                                   0.335, 10],
        '3ODXRUPL44f04cCacwiCLC': [0.708, 0.541, 0.809, 336013, 0, 0.753, 120.094, 0.72, -4.286,
                                   0.324, 8],
        '6PoKfDY78ih5OveWirggRX': [0.105, 0.859, 0.506, 187465, 0, 0.153, 140.973, 0.113, -8.115,
                                   0.418, 10],
        '7sO5G9EABYOXQKNPNiE9NR': [0.149, 0.88, 0.428, 172800, 5.07e-05, 0.333, 100.007, 0.114,
                                   -8.28, 0.206, 9],
        '5yY9lUy8nbvjM1Uyo1Uqoc': [0.0706, 0.676, 0.609, 237735, 0, 0.508, 142.037, 0.152, -5.831,
                                   0.481, 2],
        '7ycWLEP1GsNjVvcjawXz3z': [0.0609, 0.854, 0.569, 205040, 0.0816, 0.294, 80.015, 0.1, -8.151,
                                   0.106, 5],
        '598yNsG1JFrGd4n2kMoz7F': [0.0177, 0.882, 0.602, 183011, 0, 0.43, 142.959, 0.178, -5.554,
                                   0.245, 11],
        '2xLMifQCjDGFmkHkpNLD9h': [0.00513, 0.834, 0.73, 312820,
                                   0, 0.446, 155.008, 0.124, -3.714, 0.222, 8],
        '74lnM5V6ecvoTPV0fvptx9': [0.113, 0.808, 0.617, 166400, 0, 0.632, 149.962, 0.734, -9.32,
                                   0.442, 10],
        '7pas6O1LYbaeChEFQBhPFU': [0.105, 0.688, 0.658, 226397, 1.89e-06, 0.28, 75.615, 0.335,
                                   -4.155, 0.0695, 1],
        '3JAeYOjyJodI4PRs44lx2l': [0.00207, 0.836, 0.579, 213358, 0, 0.431, 85.486, 0.11, -6.164,
                                   0.243, 9],
        '3YeJXuRSNS5FYwOsDu44kD': [0.167, 0.28, 0.821, 256163, 0, 0.254, 181.444, 0.139, -2.864,
                                   0.111, 8],
        '0tdCy39PgWN8LFWu34ORn3': [0.00525, 0.845, 0.399, 257600, 0.74, 0.148, 143.049, 0.102,
                                   -7.509, 0.309, 1],
        '40oKW22ZNNkEdZLJTScaQI': [0.0306, 0.747, 0.524, 213132, 0, 0.363, 140.053, 0.2, -6.807,
                                   0.245, 10],
        '5NFYuqu8V6QXc6mzcLImd6': [0.0253, 0.787, 0.635, 209413, 0, 0.237, 130.018, 0.357, -8.271,
                                   0.155, 4],
        '2durxb17bXcmQJHSt8JAdO': [0.543, 0.823, 0.467, 310933, 1.06e-06, 0.618, 95.026, 0.135,
                                   -10.394, 0.301, 0],
        '51EC3I1nQXpec4gDk0mQyP': [0.113, 0.402, 0.526, 339067, 8.33e-06, 0.312, 81.404, 0.105,
                                   -6.741, 0.0904, 9],
        '7rC5Pl8rQSX4myONQHYPBK': [0.045, 0.754, 0.575, 205147, 0.00131, 0.491, 86.009, 0.276,
                                   -8.393, 0.0682, 4],
        '6hkQ6OQ6nhe7QCckH91aGa': [0.0423, 0.597, 0.755, 238333, 0, 0.0467, 89.146, 0.582, -2.209,
                                   0.052, 4],
        '4dVpf9jZjcORqGTLUaeYj9': [0.0651, 0.797, 0.844, 173600, 0, 0.52, 170.142, 0.087, -5.482,
                                   0.275, 11],
        '7KXjTSCq5nL1LoYtL7XAwS': [0.000282, 0.908, 0.621, 177000, 5.39e-05, 0.421, 150.011, 0.0958,
                                   -6.638, 0.102, 1],
        '0TlLq3lA83rQOYtrqBqSct': [0.0165, 0.912, 0.412, 238614, 0.0126, 0.423, 154.983, 0.104,
                                   -8.074, 0.123, 7],
        '6Ozh9Ok6h4Oi1wUSLtBseN': [0.189, 0.769, 0.787, 159715, 0, 0.836, 126.77, 0.129, -3.909,
                                   0.367, 11],
        '07KXEDMj78x68D884wgVEm': [0.269, 0.831, 0.499, 220487, 0, 0.511, 97.956, 0.3, -8.442,
                                   0.114, 11],
        '1KIQ0RscHwxXPJUvhuO5Bl': [0.414, 0.681, 0.473, 193200, 0, 0.766, 194.826, 0.0794, -5.733,
                                   0.449, 11],
        '2DQ1ITjI0YoLFzuADN1ZBW': [0.0117, 0.838, 0.771, 245387, 0, 0.405, 175.957, 0.0853, -3.791,
                                   0.244, 1],
        '6Yqmv7XJLCrQEauMbPGZSw': [0.377, 0.648, 0.631, 349933, 0, 0.142, 105.989, 0.12, -5.662,
                                   0.103, 4],
        '0ESJlaM8CE1jRWaNtwSNj8': [0.24, 0.743, 0.571, 213863, 0, 0.495, 119.054, 0.291, -6.054,
                                   0.145, 7],
        '3eekarcy7kvN4yt5ZFzltW': [0.0546, 0.598, 0.427, 175721, 5.83e-06, 0.0605, 76.469, 0.21,
                                   -8.764, 0.0317, 7],
        '32xx0fAv3CIeGmNaWTHvEF': [0.423, 0.765, 0.5, 220160, 0, 0.495, 107.043, 0.108, -7.626,
                                   0.152, 1],
        '2gwkD6igEhQbDQegRCcdoB': [0.0608, 0.876, 0.662, 163320, 0, 0.844, 75.445, 0.127, -6.482,
                                   0.426, 2],
        '1jQsKN68yE94tMYml0wHMd': [0.136, 0.747, 0.704, 213693, 0, 0.494, 136.936, 0.131, -6.743,
                                   0.0986, 1],
        '2d8JP84HNLKhmd6IYOoupQ': [0.0244, 0.746, 0.873, 222093, 0, 0.817, 148.075, 0.354, -3.803,
                                   0.128, 7],
        '1e1JKLEDKP7hEQzJfNAgPl': [0.0114, 0.791, 0.582, 181812, 0, 0.443, 162.991, 0.35, -7.323,
                                   0.286, 11],
        '2IRZnDFmlqMuOrYOLnZZyc': [0.259, 0.889, 0.496, 180522, 0, 0.544, 86.003, 0.252, -6.365,
                                   0.0905, 4],
        '2u7mxWSeoqTXndK5e08jMp': [0.157, 0.745, 0.646, 203908, 0, 0.46, 79.993, 0.338, -6.987,
                                   0.17, 6],
        '0AluA5RNsa4Cx6XRhf2hWZ': [0.588, 0.81, 0.353, 208293, 0, 0.0727, 88.031, 0.102, -9.931,
                                   0.31, 6],
        '5MPPttjfGap2C6j6eKcO6J': [0.0957, 0.97, 0.463, 142417, 0, 0.46, 108.003, 0.151, -7.259,
                                   0.366, 10],
        '6fwdbPMwP1zVStm8FybmkO': [0.373, 0.835, 0.413, 258880, 0.00133, 0.111, 149.004, 0.101,
                                   -9.81, 0.396, 1],
        '6gi6y1xwmVszDWkUqab1qw': [0.0104, 0.802, 0.591, 157712, 0, 0.309, 139.864, 0.196, -4.895,
                                   0.225, 8], '1dUHF4RyMmMTveJ0Rby6Xm':
        [0.126, 0.761, 0.598, 163974, 0, 0.446, 173.897, 0.0839, -7.249, 0.182, 10]}

    dict2 = {
        '7Djpvy4lZJNI8rTOVLf1H7': [0.0603, 0.75, 0.831, 319853, 0, 0.731, 76.439, 0.0576, -2.601,
                                   0.397, 4],
        '241vjXeYFDwQDG5ZdgvZqs': [0.301, 0.692, 0.521, 292987, 0, 0.463, 100.45, 0.0565, -8.465,
                                   0.33, 10],
        '64B98qTPN7DLorGZPf2EP6': [0.0472, 0.938, 0.623, 202571, 0, 0.402, 127.976, 0.0976, -5.905,
                                   0.0578, 8],
        '02RCbjb9czvQKNGBmEmWob': [0.0177, 0.883, 0.599, 183011, 0, 0.413, 142.976, 0.179, -5.551,
                                   0.248, 11],
        '3FDhfKLu9mV5RoRQXR5Fj3': [0.0338, 0.919, 0.446, 226187, 0, 0.181, 95.203, 0.077, -8.761,
                                   0.407, 10],
        '5lehoWkVPujeOAwb8BO0uK': [0.208, 0.868, 0.654, 225440, 0, 0.299, 138.02, 0.187, -4.832,
                                   0.0766, 9],
        '5i0eJv1DzuyhaYnro4wTKg': [0.00999, 0.833, 0.496, 146752, 1.99e-05, 0.148, 156.932, 0.126,
                                   -8.827, 0.436, 11],
        '41a7dZcq30Ss5kPMayWRV0': [0.117, 0.85, 0.473, 157605, 0.0103, 0.38, 85.454, 0.108, -5.747,
                                   0.209, 10],
        '1XRgIKC5TPwo7nWGyKqgG0': [0.0232, 0.89, 0.633, 233087, 0.000343, 0.425, 139.948, 0.0993,
                                   -5.475, 0.168, 11],
        '59J5nzL1KniFHnU120dQzt': [0.0138, 0.785, 0.62, 235535, 0, 0.478, 78.477, 0.15, -6.667,
                                   0.254, 8],
        '5nayhWICkQGMTkisxVMbRw': [0.0967, 0.755, 0.552, 193973, 0, 0.402, 153.157, 0.158, -5.604,
                                   0.288, 9],
        '1Xunvmk47Mju6oZlgzm2Ty': [0.000862, 0.925, 0.453, 249933, 5.99e-05, 0.392, 138.002, 0.124,
                                   -5.921,
                                   0.109, 7],
        '5qDlo2g8QwkA36PNqWpDCz': [0.297, 0.768, 0.604, 225133, 0.000274, 0.537, 96.948, 0.189,
                                   -9.589, 0.1, 11],
        '22mhfCPBE5YzXWYekGJUdS': [0.13, 0.733, 0.531, 332627, 0, 0.378, 171.632, 0.354, -11.217,
                                   0.326, 11],
        '2nKYHpmwjLaEOXS3o7QMiz': [0.0957, 0.97, 0.463, 142417, 0, 0.46, 108.003, 0.151, -7.259,
                                   0.366, 10],
        '3cWmqvMwVQKDigWLSZ3w9h': [0.0398, 0.773, 0.612, 193575, 0, 0.381, 149.999, 0.142, -5.73,
                                   0.232, 8],
        '47vzQk78oRe1g9vpT5663T': [0.0895, 0.702, 0.619, 220400, 0, 0.509, 168.926, 0.101, -8.332,
                                   0.222, 10],
        '4sudugmLvBQasfnRPGUoIy': [0.192, 0.621, 0.594, 138507, 0, 0.368, 101.532, 0.378, -8.064,
                                   0.0458, 7],
        '3ieLey98V9mIIh3W9gBlPF': [0.32, 0.629, 0.572, 188960, 0.000853, 0.182, 93.997, 0.109,
                                   -9.332, 0.0307, 5],
        '70LcF31zb1H0PyJoS1Sx1r': [0.0097, 0.515, 0.43, 238640, 0.000133, 0.104, 91.844, 0.129,
                                   -9.935, 0.0372, 7],
        '20RHWjtCLr7ODGQEItdZXg': [0.345, 0.643, 0.765, 268747, 1.54e-06, 0.602, 130.582, 0.126,
                                   -7.385, 0.0317, 9],
        '1OjmlSFuzYflWjSMTCyTJv': [0.0183, 0.725, 0.571, 200880, 0, 0.61, 146.035, 0.0519, -6.007,
                                   0.102, 1],
        '4CvWeXMo3PJdpTy6btPwkn': [0.0391, 0.827, 0.643, 252720, 0, 0.612, 132.026, 0.349, -7.777,
                                   0.151, 1],
        '1K5KBOgreBi5fkEHvg5ap3': [0.067, 0.795, 0.574, 237918, 0, 0.537, 142.053, 0.15, -6.903,
                                   0.487, 2],
        '5uEcJOBx1Wz3MvFZ7XTKR0': [0.0425, 0.877, 0.622, 222693, 1.05e-06, 0.481, 132.949, 0.0858,
                                   -5.072, 0.0566, 1],
        '3gTK8TzE4on9Xe05QlVIFI': [0.0308, 0.826, 0.767, 128995, 0, 0.436, 159.973, 0.113, -3.892,
                                   0.215, 1],
        '3a8r3EYOFZB7cT1OkK4zXF': [0.067, 0.891, 0.69, 378533, 0, 0.835, 96.561, 0.234, -8.649,
                                   0.378, 1],
        '4bvqOj9QiH6qKecLiefKst': [0.0954, 0.94, 0.662, 233027, 0, 0.657, 101.403, 0.376, -8.786,
                                   0.292, 7],
        '59JWp4PjZ9TRM8cmtaDYB1': [0.0183, 0.895, 0.739, 219340, 7.61e-06, 0.763, 140.007, 0.102,
                                   -6.633, 0.283, 8],
        '5NQdweL8O7nGdM7e4IS1lf': [0.0554, 0.9, 0.593, 172933, 0, 0.633, 92.946, 0.0304, -6.629,
                                   0.333, 10],
        '465hVdgg75kPgRdpJfEFFT': [0.0492, 0.641, 0.531, 225413, 0, 0.194, 135.564, 0.118, -7.243,
                                   0.157, 2],
        '6DWdTk7UaZ6LIYYCFvmgX7': [0.0764, 0.6, 0.664, 226027, 0, 0.323, 174.22, 0.0922, -6.734,
                                   0.334, 1],
        '7la8N6YLMUDAXl2iAEe9Sy': [0.195, 0.693, 0.562, 197947, 0, 0.183, 123.979, 0.123, -7.323,
                                   0.0379, 0],
        '7DcvwMAiqKJQD1rrdfxSDx': [0.0247, 0.796, 0.586, 200107, 0, 0.179, 97.981, 0.132, -6.946,
                                   0.147, 4],
        '5u64RlrnvvbtNh6R0EMh6o': [0.229, 0.781, 0.548, 214255, 0, 0.175, 106.996, 0.127, -4.997,
                                   0.0764, 0],
        '7pnBwXmQuffahj74xsGvRL': [0.0347, 0.627, 0.62, 277333, 1.06e-05, 0.252, 79.992, 0.283,
                                   -6.637, 0.0659, 1],
        '4S99rQA9ixLlvaHK1fJn6n': [0.0589, 0.776, 0.575, 216187, 0, 0.34, 144.15, 0.349, -10.613,
                                   0.117, 4],
        '4MO2Rtx0FGgOukZO7gw1qB': [0.363, 0.779, 0.494, 204875, 0, 0.149, 150.033, 0.105, -9.503,
                                   0.38, 2],
        '2G2ptmdyAhWEIb53U93fZa': [0.000953, 0.519, 0.82, 298075, 0.000113, 0.0751, 127.954, 0.166,
                                   -4.813, 0.0515, 9],
        '4apiNNK0jp9uqn3JDG9My1': [0.167, 0.28, 0.821, 256163, 0, 0.254, 181.444, 0.139, -2.864,
                                   0.111, 8],
        '4aZirFFDJlUUuvhpjY5cAH': [0.0157, 0.466, 0.653, 208907, 0, 0.205, 143.034, 0.263, -4.583,
                                   0.0298, 0],
        '1egFecJPKqG7IcsE3sjZCr': [0.809, 0.571, 0.355, 238933, 0, 0.503, 124.692, 0.306, -11.497,
                                   0.115, 11],
        '3BtuIIrQlkujKPuWF2B85z': [0.0489, 0.794, 0.653, 263373, 4.88e-05, 0.397, 117.996, 0.1,
                                   -7.839, 0.104, 7],
        '4MBxX1P21a0yEZJEHA7zw1': [0.104, 0.883, 0.567, 172852, 0, 0.241, 99.962, 0.136, -8.394,
                                   0.0902, 5],
        '7huo2wvrCgRucUsjdSDLQV': [0.00376, 0.862, 0.742, 228907, 0.00855, 0.511, 127.91, 0.103,
                                   -4.722, 0.222, 7],
        '0ndVtaoJarSoK9SBCRkaJt': [0.0131, 0.725, 0.557, 266760, 7.79e-06, 0.404, 91.064, 0.218,
                                   -7.697, 0.0559, 4],
        '3cL9ivTyGpd7XMpB4Img2I': [0.222, 0.674, 0.59, 327640, 0, 0.58, 98.728, 0.293, -10.296,
                                   0.157, 7],
        '03sEEzFv7vnD54KRwU47Ue': [0.0573, 0.716, 0.656, 282680, 0, 0.496, 81.101, 0.329,
                                   -7.291, 0.167, 6],
        '3feDdjOYqdMd8BCJOZ36P1': [0.0806, 0.504, 0.643, 186890, 0.000697, 0.186, 93.221, 0.31,
                                   -4.474, 0.0247, 11],
        '0JFOXqd9N6RlMaAFlaaqFw': [0.169, 0.457, 0.541, 226813, 8.5e-06, 0.264, 77.349, 0.0825,
                                   -8.658, 0.033, 9],
        '3nqnWEZnYoetfO2ksMZZVK': [0.0611, 0.865, 0.641, 263533, 0.000107, 0.762, 95.307, 0.218,
                                   -6.652, 0.162, 10],
        '6KkAC41nNRiWA6w3ZD9cJ8': [0.676, 0.601, 0.8, 224733, 0, 0.868, 113.612, 0.611, -9.509,
                                   0.322, 9],
        '1i0kVfX5LdEdo52St39QM0': [0.0134, 0.767, 0.765, 292779, 0, 0.738, 180.527, 0.804, -6.895,
                                   0.386, 11],
        '1I0FXGm889xuUAFqcx9bCp': [0.0998, 0.901, 0.369, 357224, 0.753, 0.296, 128.998, 0.0939,
                                   -12.538, 0.293, 1],
        '0zUb5MPkQCcDxqTkXiEIud': [0.559, 0.812, 0.427, 188360, 3.72e-05, 0.573, 97.436, 0.161,
                                   -10.935, 0.0824, 0],
        '4u4mSxeOuRZHqC9gn1imoJ': [0.0221, 0.442, 0.739, 180000, 0, 0.156, 127.749, 0.561, -5.341,
                                   0.0502, 4],
        '0lTGv9B3KeHGv9yqOMleZX': [0.0442, 0.704, 0.836, 309587, 0, 0.606, 183.465, 0.0744, -5.254,
                                   0.326, 11],
        '3CuKcfH8BJ5The5G3llaKD': [0.195, 0.732, 0.817, 305720, 2.98e-06, 0.804, 115.19, 0.0824,
                                   -6.571, 0.286, 11],
        '56sNhTYp0mGC1cXaagTNv1': [0.425, 0.729, 0.394, 197000, 0.000936, 0.795, 203.028, 0.133,
                                   -17.876, 0.407, 10],
        '4a6q8CR2hzLk2plDkSxkfD': [0.379, 0.812, 0.519, 165714, 0, 0.554, 104.954, 0.13, -4.823,
                                   0.0385, 2],
        '4awnQTwynhz0j6Rk2ZwM6A': [0.106, 0.676, 0.662, 245027, 0, 0.464, 127.999, 0.122, -6.438,
                                   0.0442, 1],
        '07RXBKfyCYIYRMLCvlGWXU': [0.0476, 0.79, 0.875, 247013, 0, 0.759, 139.985, 0.312, -6.55,
                                   0.091, 7],
        '5ri4zqtWhG07hIuNNDWP76': [0.217, 0.806, 0.513, 178157, 0, 0.503, 124.988, 0.217, -6.208,
                                   0.0685, 4],
        '05nbZ1xxVNwUTcGwLbp7CN': [0.648, 0.749, 0.398, 226040, 1.26e-06, 0.0859, 80.032, 0.115,
                                   -7.44, 0.171, 5]}

    dict3 = {
        '0hPLZrnDgtKxrym1BHjDhd': [0.111, 0.872, 0.591, 205352, 0, 0.696, 131.982, 0.144, -6.952,
                                   0.359, 6],
        '7KUb9G3NNqbQ8NPb2ccU3s': [0.0526, 0.789, 0.777, 182535, 0, 0.935, 142.109, 0.453, -5.69,
                                   0.132, 11],
        '2ZccygxtuXd0hu8zF7GQbO': [0.449, 0.84, 0.704, 184793, 0, 0.381, 103.998, 0.145, -5.986,
                                   0.199, 6],
        '20Yz5dzjdTCVjXte9KrJbi': [0.177, 0.681, 0.414, 155832, 0, 0.0734, 148.03, 0.178, -6.944,
                                   0.223, 1],
        '6bnF93Rx87YqUBLSgjiMU8': [0.0236, 0.537, 0.746, 198267, 1.01e-06, 0.252, 170.062, 0.156,
                                   -5.507, 0.15, 10],
        '6kiIVIbmwEw6JvIZc7UG0E': [0.171, 0.577, 0.734, 142710, 0, 0.254, 94.122, 0.12, -8.484,
                                   0.432, 8],
        '2hc5T3WphxOr3VbiuqmuiC': [0.00881, 0.631, 0.527, 167660, 1.06e-05, 0.299, 184.033, 0.221,
                                   -7.426, 0.376, 11],
        '0uIFsRx5caF13RunwkgLYt': [0.0815, 0.852, 0.554, 160059, 0, 0.33, 155.961, 0.118, -8.254,
                                   0.389, 11],
        '6m6Oy3F6GG0zRwH03rWmTv': [0.413, 0.926, 0.544, 231787, 9.54e-05, 0.656, 115.951, 0.112,
                                   -6.827, 0.0727, 5],
        '1I55Ea0zVoSKs6MqW7DQ3i': [0.292, 0.749, 0.792, 180000, 0, 0.239, 144.064, 0.109, -4.151,
                                   0.0826, 10],
        '0oVxGuRMnawFgA8aduocfc': [0.000159, 0.805, 0.776, 172245, 0, 0.172, 146.997, 0.0502,
                                   -6.006, 0.139, 1],
        '14S2Y85NiZoU4AFGOn56uV': [0.0488, 0.739, 0.585, 244573, 0, 0.382, 129.854, 0.198, -9.776,
                                   0.0633, 9],
        '4mDrvj0dNff0WPUTFuyTKK': [0.00829, 0.698, 0.598, 277551, 0, 0.22, 147.521, 0.0945, -9.319,
                                   0.386, 0],
        '0cGPqSBtm0UJLo1HCziww9': [0.222, 0.747, 0.606, 173419, 0, 0.2, 155.055, 0.281, -5.286,
                                   0.172, 4],
        '2oHDJHNondITqbl8xZ9vPn': [0.325, 0.776, 0.752, 192705, 0, 0.716, 140.013, 0.33, -4.711,
                                   0.193, 8],
        '3PSUg0M68bXMb8vQJIPMZO': [0.0365, 0.642, 0.372, 181341, 0, 0.119, 160.009, 0.149, -10.201,
                                   0.582, 10],
        '2MySOfFfkzKx917ds6EwKK': [0.483, 0.755, 0.874, 153626, 0, 0.817, 100.047, 0.22, -4.991,
                                   0.256, 2],
        '2aTapPD0yEGaiunNqMy9Ld': [0.157, 0.84, 0.683, 242453, 0, 0.48, 137.022, 0.321, -6.924,
                                   0.219, 5],
        '7qKsAYVqMCatvJ4s7SQf8c': [0.0361, 0.883, 0.565, 189475, 0, 0.355, 129.96, 0.112, -8.565,
                                   0.378, 8],
        '33NoCir8q4WA4HNmyrD3fu': [0.0178, 0.779, 0.58, 167851, 0, 0.299, 160.243, 0.15, -7.594,
                                   0.284, 1],
        '4b6JWEZfAz9UPQBQaFkCPQ': [0.0684, 0.907, 0.683, 159833, 7.18e-06, 0.342, 89.983, 0.0834,
                                   -8.079, 0.349, 5],
        '5Ddn2hwpLVq343P90XRnNA': [0.824, 0.753, 0.614, 220240, 0, 0.331, 97.062, 0.0917, -7.924,
                                   0.139, 7],
        '7uDTc1eJwsD7iMZLhdp8LH': [0.0462, 0.76, 0.674, 173870, 0, 0.431, 101.987, 0.22, -7.043,
                                   0.129, 7],
        '1uULQtJ8rbsX5TwjPpPc9Q': [0.000897, 0.879, 0.41, 288364, 2.09e-05, 0.0703, 80.011, 0.108,
                                   -9.233, 0.551, 8],
        '0U6CynbrbmZsXiL4bD2J8A': [0.0637, 0.635, 0.726, 188835, 0, 0.389, 87.244, 0.109, -6.414,
                                   0.315, 7],
        '02mYw61RoS1vXvkD9Q5dpN': [0.0562, 0.889, 0.507, 154667, 0, 0.219, 111.994, 0.116, -8.74,
                                   0.162, 2],
        '5AL4chhuQBsENEAS1YtV38': [0.00153, 0.775, 0.551, 198229, 0, 0.514, 77.537, 0.348, -9.87,
                                   0.201, 10],
        '3hYBu3LRhapDItoL2R5aK2': [0.233, 0.453, 0.72, 193952, 0, 0.518, 80.788, 0.156, -5.839,
                                   0.255, 0],
        '7n0lXKEOaFxrAU0R93fIQh': [0.0337, 0.67, 0.634, 144098, 0, 0.375, 204.113, 0.0714, -6.682,
                                   0.294, 8],
        '2oBkmnpTEwSNGfWdJOhXJb': [0.154, 0.737, 0.708, 150000, 0, 0.272, 127.995, 0.219, -7.738,
                                   0.0896, 11],
        '6heRfvHrUIIPx9TqRg8SCq': [0.17, 0.554, 0.614, 191583, 0, 0.372, 80.028, 0.267, -5.715,
                                   0.44, 5],
        '3DqFP5KDbNeOWLxiDJqJRk': [0.00977, 0.713, 0.661, 156560, 0, 0.241, 105.873, 0.13, -5.74,
                                   0.148, 1],
        '1RrQK0BIyxZaOooNDVSEaZ': [0.0471, 0.849, 0.64, 137826, 0, 0.36, 126.005, 0.321, -5.15,
                                   0.196, 5],
        '6kBt9rhDCAdcejUi3UKBJ8': [0.156, 0.851, 0.654, 226983, 0, 0.645, 126.989, 0.113, -8.013,
                                   0.0421, 8],
        '6EBrsshL06rKyB33oUKZ7P': [0.0585, 0.786, 0.675, 202839, 0,
                                   0.548, 155.065, 0.104, -6.585, 0.104, 6],
        '0UPBidRYcgJ2mjZlk08V8x': [0.323, 0.562, 0.502, 224000, 0, 0.322, 120.104, 0.0757, -10.269,
                                   0.255, 6],
        '1ZRjLZcNTm1vUgrexBp3px': [0.0716, 0.836, 0.649, 156032, 0, 0.294, 95.084, 0.0943, -6.442,
                                   0.332, 11],
        '7rTzrRdc5UbvLr0gwI1J3E': [0.102, 0.732, 0.654, 153597, 0, 0.369, 138.049, 0.215, -6.136,
                                   0.045, 7],
        '1hoQHAz0Rpf2CGC89fE1TR': [0.159, 0.643, 0.593, 283944, 0, 0.212, 141.704, 0.112, -7.533,
                                   0.284, 1],
        '2hYN1IVp5LGIsi5MpzcjVz': [0.195, 0.641, 0.76, 221827, 0, 0.59, 141.82, 0.0768, -4.442,
                                   0.179, 6],
        '1bZra45d8JQuOm3BiVXn0v': [0.1, 0.807, 0.673, 175200, 5.86e-05, 0.193, 100.098, 0.116,
                                   -7.861, 0.285, 1],
        '3UyjIh2AKIz5mzjzcwDfP2': [0.0342, 0.559, 0.684, 167916, 0, 0.249, 150.059, 0.162, -6.009,
                                   0.232, 6],
        '5r7WvQtyPfy1xch5zMgGRp': [0.769, 0.854, 0.554, 163121, 1.84e-06, 0.272, 142.069, 0.0749,
                                   -4.684, 0.172, 8],
        '2dfqS3MRtbLZSZA1IL8xY5': [0.0103, 0.745, 0.822, 143214, 4.2e-06, 0.415, 86.733, 0.155,
                                   -6.354, 0.252, 7],
        '0j2CNrgtalXRGIvHMO2vzh': [0.264, 0.744, 0.702, 167845, 0, 0.338, 91.885, 0.12, -6.255,
                                   0.288, 7],
        '3o0nkjyy6eZL5lZcEpvJec': [0.452, 0.48, 0.679, 148676, 0, 0.29, 81.186, 0.152, -6.776,
                                   0.264, 4]}

    dict4 = {
        '5uZm7EFtP5aoTJvx5gv9Xf': [0.308, 0.538, 0.52, 174192, 0, 0.551, 180.274, 0.214, -11.063,
                                   0.737, 7],
        '30eLJakNQuTeyAQCVQTFMX': [0.379, 0.697, 0.329, 95355, 0, 0.139, 110.351, 0.153, -17.313,
                                   0.93, 8],
        '1NPdwcEoPXbVO6W3Y2oJgv': [0.196, 0.626, 0.252, 135533, 0, 0.538, 176.36, 0.179, -16.238,
                                   0.942, 7],
        '7vylqfcwlHa8k0JmyUVFBj': [0.243, 0.631, 0.252, 104500, 0, 0.561, 170.417, 0.224, -21.124,
                                   0.884, 7],
        '7gdN2q9kuKAdICPTaYLwEx': [0.55, 0.649, 0.226, 126656, 0, 0.572, 71.34, 0.167, -19.121,
                                   0.964, 10], '1UIGTjooANVp0MkxS9oXPX':
        [0.304, 0.63, 0.184, 139300, 0, 0.515, 164.91, 0.127, -19.804, 0.859, 7],
        '6Dlpszcxh5Gd2HEfAqTtRj': [0.596, 0.75, 0.22, 123756, 0, 0.628, 78.124, 0.178, -18.853,
                                   0.956, 10],
        '5pZTqEAK59vyJLv1KM0y2s': [0.581, 0.735, 0.201, 125820, 0, 0.567, 81.353, 0.17, -20.882,
                                   0.96, 10],
        '3vInsCLqcZSGjXYAwFTfmS': [0.522, 0.654, 0.236, 140396, 0, 0.584, 86.743, 0.14,
                                   -16.964, 0.962, 9],
        '2xrEKfRe0oS73vxZ7cpZeJ': [0.0231, 0.657, 0.311, 99400, 0, 0.501, 90.675, 0.142, -15.392,
                                   0.951, 5],
        '1IMHJkQ61yfLAho9LwurLM': [0.148, 0.636, 0.243, 105200,
                                   0, 0.365, 167.588, 0.184, -17.604, 0.967, 5],
        '6dr7ekfhlbquvsVY8D7gyk': [0.272, 0.646, 0.439, 156631, 0, 0.528, 160.387, 0.0945, -10.837,
                                   0.818, 7],
        '0ykQtZ84NGXhHIVFQgbxyj': [0.572, 0.701, 0.206, 140417, 0, 0.578, 80.883, 0.13, -13.235,
                                   0.944, 10],
        '3AIbe7I4cAvwiGcDxvzhb6': [0.607, 0.69, 0.221, 116834, 0, 0.65, 87.873, 0.217, -17.81,
                                   0.953, 10],
        '48CqJIyYIsZ6iqW6TYz7aH': [0.56, 0.721, 0.208, 141728, 0, 0.578, 73.363, 0.101, -19.393,
                                   0.966, 11],
        '2rTU0hNv7Ya3X4DtBCyoDK': [0.505, 0.703, 0.26, 123234, 0, 0.492, 80.489, 0.18, -16.653,
                                   0.964, 10],
        '30zIH0dkxaBfK0qapYCtuT': [0.403, 0.648, 0.211, 134400, 1.25e-06, 0.538, 148.724, 0.261,
                                   -22.174, 0.963, 10],
        '0h3X3ZpoEboBRca0FplyD0': [0.22, 0.729, 0.136, 95200, 0, 0.663, 115.968, 0.416, -15.451,
                                   0.897, 7],
        '3iig6zmFYMV0CUNziHi0sG': [0.121, 0.739, 0.19, 98700, 2.17e-05, 0.463, 93.957, 0.234,
                                   -20.126, 0.873, 5],
        '6IyLlsJr2KpLH98SoqiWIQ': [0.498, 0.67, 0.139, 125504, 0, 0.564, 133.801, 0.162, -25.62,
                                   0.954, 11],
        '7rva4PU32ZJedT4fsCLOs3': [0.157, 0.651, 0.133, 120900, 0, 0.302, 117.808, 0.0991, -22.114,
                                   0.918, 7],
        '7gGa1r1DDMBjwRl3CEXVD7': [0.469, 0.797, 0.187, 147266, 0, 0.334, 54.99, 0.21, -21.289,
                                   0.95, 7],
        '2LkLJhskz3IJZFQHAbmgmt': [0.406, 0.624, 0.322, 329507, 0, 0.341, 79.988, 0.103, -11.794,
                                   0.679, 9],
        '4t49zUlDIprtcL5twoSbEU': [0.291, 0.645, 0.322, 128800, 3.05e-06, 0.51, 88.527, 0.272,
                                   -22.711, 0.957, 6],
        '17qVDp8STcC6UajNQOeMgH': [0.468, 0.717, 0.158, 133369, 0, 0.376, 129.074, 0.34, -21.553,
                                   0.945, 6],
        '0fzar7IQJbTUHnPCx04uIl': [0.494, 0.704, 0.22, 150500, 0, 0.671, 107.76, 0.163, -21.511,
                                   0.932, 6],
        '56cSqNamfuOjl2gX8iVF28': [0.61, 0.626, 0.199, 132501, 0, 0.521, 76.182, 0.148, -24.658,
                                   0.966, 11],
        '1NXxlYnpd6Pxzs2GwInBFy': [0.538, 0.628, 0.186, 102100, 0, 0.346, 172.121, 0.545, -16.65,
                                   0.96, 9],
        '1xqgz0Hp1DK2nEPujBay1F': [0.412, 0.697, 0.196, 95100, 0, 0.741, 97.988, 0.216, -15.553,
                                   0.881, 11],
        '5PBhgpdypZCsd86fQryuzc': [0.0246, 0.754, 0.159, 103200, 0.000617, 0.552, 125.113, 0.229,
                                   -23.059, 0.908, 11],
        '5odgkeMbGjTy4Lvk7GAumo': [0.163, 0.767, 0.127, 96500, 0, 0.619, 73.496, 0.125, -18.144,
                                   0.93, 11], '2TXYIFZ202G0dNhbhbB0G3': [0.341,
                                                                         0.631, 0.215, 126368, 0,
                                                                         0.337, 172.927, 0.282,
                                                                         -20.33, 0.937, 11],
        '6uu4db7cF32izBFJhLYqjt': [0.364, 0.705, 0.149, 127413, 0, 0.36, 106.638, 0.114, -20.961,
                                   0.92, 9],
        '6So7cXNWQt7I1cvMtdkz5k': [0.488, 0.605, 0.168, 125400, 0, 0.628, 80.401, 0.101, -24.14,
                                   0.959, 10],
        '3vGdME5bSONaFgvKYjXIi0': [0.164, 0.687, 0.334, 304573, 4.79e-06, 0.595, 101.033, 0.476,
                                   -16.939, 0.935, 10],
        '2ZBaNbhXdWB9yTEU10CK03': [0.262, 0.666, 0.349, 416267, 0, 0.679, 95.34, 0.253, -18.056,
                                   0.949, 10],
        '6TQbRDNMYajOXQsTPktsIW': [0.445, 0.718, 0.169, 119472, 0, 0.227, 127.691, 0.226, -22.049,
                                   0.93, 8],
        '5tdqgm9gjCruJes96tizca': [0.57, 0.713, 0.132, 141500, 0, 0.631, 114.132, 0.15, -24.667,
                                   0.954, 6],
        '1kGBa3JBk7QVDdzw6JMLNr': [0.0174, 0.723, 0.134, 109700, 0, 0.688, 124.642, 0.088, -20.532,
                                   0.935, 6],
        '4IKr3NTgrGAiUX28lWhCAn': [0.189, 0.714, 0.356, 941240, 1.03e-05, 0.655, 125.435, 0.159,
                                   -17.637, 0.937, 10],
        '3hq3CcS3ahjNpFaXDJxOKA': [0.273, 0.709, 0.227, 131800, 0, 0.513, 134.319, 0.178, -22.234,
                                   0.95, 9],
        '4Wto4H25HpMgJpQ7kpQ8yX': [0.987, 0.618, 0.511, 119902, 5.65e-05, 0.126, 171.707, 0.896,
                                   -15.049, 0.962, 0],
        '4FZqRi5EvjdMooumrDukbk': [0.973, 0.148, 0.316, 280467, 0.751, 0.0592, 83.875, 0.184,
                                   -11.847, 0.0364, 5],
        '4zqo0H4ChH4J1cnusuuqTl': [0.88, 0.155, 0.283, 162760, 0.789, 0.0392, 73.664, 0.125,
                                   -14.773, 0.0378, 5],
        '1qmIIxSmZy1dEWTAn9P2QX': [0.957, 0.138, 0.357, 708307, 0.875, 0.0814, 79.905, 0.101,
                                   -11.562, 0.0372, 4],
        '17aJpoagVRY4kGdoGEpNYy': [0.969, 0.169, 0.0755, 67333, 0.0263, 0.0325, 170.98, 0.582,
                                   -19.024, 0.0435, 7]}

    input_in = list(dict1.values())
    output_in = list(dict2.values())

    input_not = list(dict3.values())
    output_not = list(dict4.values())

    calc_diff_btwn_playlists(input_in, output_in)
    calc_diff_btwn_playlists(input_not, output_not)
