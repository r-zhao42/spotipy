"""
This file is responsible to create a user-interface for our Song Recommendation program using
Tkinter.

"""

from typing import Any
import tkinter as tk
from tkinter import PhotoImage
from PIL import ImageTk, Image


# from tkinter import filedialog, Text
#
# name_of_program = 'Spotify Recommender'
#
# root = tk.Tk()
# root.title(name_of_program)
#
# label = tk.Label(root, text="Hello, please enter your playlist link!")
# label.pack()
#
# user_entry = tk.Entry().pack(pady=30)
#
# tk.Button(
#     root,
#     text="Register Player",
#     padx=10,
#     pady=5, command=print('hello')).pack()
#
# canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
#
# canvas.pack()
#
# # user_entry = tk.Entry().pack()
#
# # link = tk.askstring()
#
#
#
# root.mainloop()
#
# if __name__ == '__main__':
#
#     print('hello')

class PlaylistEntry():
    """
    This is a class responsible for creating a Tkinter window, and get a the playlist link
    from the user, which is later stored and used within the program to generate another playlist.
    """

    root: Any

    def __init__(self, root: Any) -> None:
        # Here we initialize the playlist entry initially as an empty string
        self.playlist_entry = ""
        self.root = root

        # We set the title of the Tkinter window as the name of the program
        root.title('Spotify Recommender')

        # This is the label for the user to understand what to input
        tk.Label(root, text="Enter your Spotify playlist below : ").pack()

        self.link_entry = tk.Entry(root)
        self.link_entry.pack()

        # Do I need this or no????????
        # self.link_entry.focus_set()

        # Creates a button for the user to click to enter their input
        tk.Button(root, text="plot", command=self.get_link).pack()

        # Creates a canvas below to add other visuals
        canvas = tk.Canvas(root, height=400, width=400)
        canvas.pack()

        img = ImageTk.PhotoImage(Image.open("spotify2.png"))
        canvas.create_image(20, 20, anchor='nw', image=img)

    def get_link(self) -> None:
        """Responsible for storing the link inputted by the user"""

        self.playlist_entry = self.link_entry.get()
        print("inside class", self.playlist_entry)


if __name__ == "__main__":
    root = tk.Tk()
    BE = PlaylistEntry(root)
    root.mainloop()

    print(BE.playlist_entry)

