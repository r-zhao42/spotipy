"""
This file is responsible to create a user-interface for our Song Recommendation program using
Tkinter.

"""

from typing import Any, List, Dict
import tkinter as tk
from tkinter import ttk as ttk
from PIL import ImageTk, Image
import urllib
import webbrowser


class UserPlaylistEntry:
    """
    This is a class responsible for creating a Tkinter window, and get a the playlist link
    from the user, which is later stored and used within the program to generate another playlist.

    Instance Attributes:
        - root: This instance attribute is used for storing the root of the Tkinter window

    """

    root: Any

    def __init__(self, root: Any) -> None:
        # We first initialize the root of our tkinter window
        self.root = root

        # Here we initialize the rest of the class attributes that are user inputs to empty strings
        self.playlist_entry = ''
        self.scale_entry = ''
        # self.playlist_length_entry = ''
        self.new_playlist_name = ''
        self.dimension = ''
        self.att_1 = ''
        self.att_2 = ''
        self.att_3 = ''

        self._image = Image.open('Spotify-Logo.png').resize((140, 100))

        self._link_entry = tk.Entry(self.root, borderwidth=10, selectbackground='#1DB954')

        self._slider = tk.Scale(self.root, from_=1, to=10, tickinterval=1, orient='horizontal',
                                bg="#1DB954",
                                fg="BLACK", sliderlength=20, length=200)

        self._new_playlist_name_entry = tk.Entry(self.root, borderwidth=10,
                                                 selectbackground='#1DB954')

        # self.length_entry = tk.Entry(self.root, borderwidth=10, selectbackground='#1DB954')

        self._inner_string = tk.StringVar(self.root)
        self._inner_string.set('Choose Dimension')
        dimension_options = ["2D", "3D"]
        self._dimension_menu = tk.OptionMenu(self.root, self._inner_string, *dimension_options)

        self._dimension_menu.config(bg='#1DB954')

        attribute_options = ['Acousticness', 'Danceability', 'Energy', 'Duration(ms)',
                             'Instrumentalness', 'Valence', 'Tempo', 'Liveness', 'Loudness',
                             'Speechness', 'Key']
        self._inner_string_att1 = tk.StringVar(self.root)
        self._inner_string_att1.set('Attribute 1 ')
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
        self._attribute3_menu = tk.OptionMenu(self.root, self._inner_string_att3, *attribute_options)

        self._attribute3_menu.config(bg='#1DB954')

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

        tk.Label(self.root, text='FOR VISUALIZATION \n Please choose a dimension.',
                 font=("Proxima nova", "9", "bold")).grid()

        self._dimension_menu.grid()

        tk.Label(self.root, text='Please choose your first attribute',
                 font=("Proxima nova", "9", "bold")).grid()
        self._attribute1_menu.grid()

        tk.Label(self.root, text='Please choose your second attribute',
                 font=("Proxima nova", "9", "bold")).grid()
        self._attribute2_menu.grid()

        tk.Label(self.root, text='IF APPLICABLE, choose your third attribute',
                 font=("Proxima nova", "9", "bold")).grid()
        self._attribute3_menu.grid()

        tk.Button(self.root, text='ENTER', command=self.get_user_input, padx=5,
                  pady=5, bg='#1DB954').grid()

        # We need to quit out of the window when the user has inputted all of the entries.
        # if self.playlist_entry != '' and self.scale_entry != '' \
        #         and self.playlist_length_entry != '':
        #
        #     self.root.destroy()

    def get_user_input(self) -> None:
        """Responsible for storing the link inputted by the user

        It also quits the window if all three user inputs are entered
        """

        # Here we update the playlist entry attribute
        self.playlist_entry = self._link_entry.get()

        # Here we update the scale entry attribute
        self.scale_entry = self._slider.get()

        # Here we update the desired new playlist
        # self.playlist_length_entry = self.length_entry.get()

        # Update the desired new playlists name
        self.new_playlist_name = self._new_playlist_name_entry.get()

        self.dimension = self._inner_string.get()
        self.att_1 = self._inner_string_att1.get()
        self.att_2 = self._inner_string_att2.get()
        self.att_3 = self._inner_string_att3.get()

        # if int(self.playlist_length_entry) > 100:
        #     print('Enter a number between 0 - 100')

        # We need to quit out of the window when the user has inputted all of the entries.
        if self.playlist_entry != '' and self.scale_entry != '' \
                and self.new_playlist_name != '' and (self.dimension != '' or
                                                      self.dimension != 'Choose Dimension'):
                # and int(self.playlist_length_entry) <= 100:
            # Since now we know all inputs are recorded, we can automatically quit the window

            self.root.destroy()
            print('YOUR INFORMATION HAS BEEN RECORDED.')
            print('THANK YOU!')

        # print(self.playlist_entry)
        # print(self.scale_entry)
        # print(self.playlist_length_entry)
        # print(self.new_playlist_name)
        print(self.dimension)
        print(self.att_1)
        print(self.att_2)
        print(self.att_3)


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

    def __init__(self, root: Any, link: str) -> None:
        """Initialize the class and its attributes"""

        self.root = root
        self.link = link

        self._image = Image.open('Spotify-Logo.png').resize((140, 100))

        self._link_button = tk.Button(self.root, text='OPEN LINK!', command=self.open_link, padx=5,
                                      pady=5, bg='#1DB954')
        self._acoustic_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300)
        self._dance_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300)
        self._energy_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300)
        self._instrument_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300)
        self._valence_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300)
        self._tempo_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300)
        self._liveness_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300)
        self._loud_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300)
        self._speech_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300)

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

        self._acoustic_progress_bar['value'] = 80
        self._acoustic_progress_bar.grid(pady=30)

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
    # >>> calc_diff_btwn_playlists(list1, list2)
    # [0.2, 0.2, 0.15, 0.1]


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
    # root = tk.Tk()
    # BE = UserPlaylistEntry(root)
    # BE.run_window()
    # root.mainloop()
    #
    root2 = tk.Tk()
    window = NewPlaylistOutput(root2, 'https://open.spotify.com/playlist/1zKz3iMcIOHicoacBa24jo?si=M4S5RXJQQ5CsjjYPLGWkRw')
    window.run_window()
    root2.mainloop()

    import doctest
    doctest.testmod()

    list1 = [[1, 1, 1, 1], [0.8, 0.8, 0.8, 0.8]]
    list2 = [[1.1, 1.1, 1.2, 1.2], [0.5, 0.5, 0.7, 0.8]]
    calc_diff_btwn_playlists(list1, list2)
