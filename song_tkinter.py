"""
This file is responsible to create a user-interface for our Song Recommendation program using
Tkinter.

"""

from typing import Any
import tkinter as tk
from tkinter import PhotoImage
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
        self.playlist_length_entry = ''
        self.new_playlist_name = ''

        self.image = Image.open('Spotify-Logo.png').resize((140, 100))

        self.link_entry = tk.Entry(self.root, borderwidth=10, selectbackground='#1DB954')

        self.slider = tk.Scale(self.root, from_=1, to=10, tickinterval=1, orient='horizontal',
                               bg="#1DB954",
                               fg="BLACK", sliderlength=20, length=200)

        self.new_playlist_name_entry = tk.Entry(self.root, borderwidth=10,
                                                selectbackground='#1DB954')

        self.length_entry = tk.Entry(self.root, borderwidth=10, selectbackground='#1DB954')

    def run_window(self) -> None:
        """Runs a new Tkinter window"""

        self.root.title('Spotify Recommender')

        sp_logo = ImageTk.PhotoImage(self.image)
        label = tk.Label(self.root, image=sp_logo)

        # We need to save the reference to the image
        label.image = sp_logo
        label.grid()

        # tk.Label(self.root, image=tkimage, font='center').grid()

        tk.Label(self.root, text='Enter the link of your Spotify playlist below : ',
                 font=("Proxima nova", "9", "bold")).grid()

        self.link_entry.grid(ipadx=30)

        tk.Label(self.root, text="How adventurous are you feeling today?",
                 font=("Proxima nova", "9", "bold")).grid()

        self.slider.grid()

        tk.Label(self.root,
                 text='Enter the desired length of your new playlist (MAX 100) : ',
                 font=("Proxima nova", "9", "bold")).grid()

        self.length_entry.grid(ipadx=30)

        tk.Label(self.root, text='What do you want to name your new playlist? ',
                 font=("Proxima nova", "9", "bold")).grid()

        self.new_playlist_name_entry.grid(ipadx=30)

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
        self.playlist_entry = self.link_entry.get()

        # Here we update the scale entry attribute
        self.scale_entry = self.slider.get()

        # Here we update the desired new playlist
        self.playlist_length_entry = self.length_entry.get()

        # Update the desired new playlists name
        self.new_playlist_name = self.new_playlist_name_entry.get()

        if int(self.playlist_length_entry) > 100:
            print('Enter a number between 0 - 100')

        # We need to quit out of the window when the user has inputted all of the entries.
        if self.playlist_entry != '' and self.scale_entry != '' \
                and self.new_playlist_name != '' and int(self.playlist_length_entry) <= 100:
            # Since now we know all inputs are recorded, we can automatically quit the window

            self.root.destroy()
            print('YOUR INFORMATION HAS BEEN RECORDED.')
            print('THANK YOU!')

        # print(self.playlist_entry)
        # print(self.scale_entry)
        # print(self.playlist_length_entry)
        # print(self.new_playlist_name)


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

    def __init__(self, root: Any, link: str) -> None:
        """Initialize the class and its attributes"""

        self.root = root
        self.link = link

        self.image = Image.open('Spotify-Logo.png').resize((140, 100))

        self.link_button = tk.Button(self.root, text='OPEN LINK!', command=self.open_link, padx=5,
                                     pady=5, bg='#1DB954')

    def run_window(self) -> None:
        """
        Runs the tkinter window which displays the link to the generated playlist

        """

        self.root.title('Spotify Recommender')

        sp_logo = ImageTk.PhotoImage(self.image)
        label = tk.Label(self.root, image=sp_logo)

        # We need to save the reference to the image
        label.image = sp_logo
        label.grid()

        tk.Label(self.root, text='Here is the link to your new playlist!',
                 font=("Proxima nova", "9", "bold")).grid()
        tk.Label(self.root, text=self.link, bd=20, font=("Proxima nova", "9", "bold")).grid()

        self.link_button.grid()

    def open_link(self) -> None:
        """Function that is used to be the command for the button of the tkinter window to go
        to the link of the new playlist"""

        webbrowser.open_new(self.link)


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


