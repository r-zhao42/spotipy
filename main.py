if __name__ == '__main__':
    import tkinter as tk
    from song_tkinter import UserPlaylistEntry, NewPlaylistOutput

    input_window_root = tk.Tk()
    input_window = UserPlaylistEntry(input_window_root)
    input_window.run_window()
    input_window_root.mainloop()
    
    print(input_window.new_playlist_name)

    # output_playlist_link = 'https://open.spotify.com/playlist/1zKz3iMcIOHicoacBa24jo?si=M4S5RXJQQ5CsjjYPLGWkRw'
    # output_playlist_summary = {'Acousticness': 80,
    #                            'Danceability': 50,
    #                            'Energy': 30,
    #                            'Instrumentalness': 10,
    #                            'Valence': 55,
    #                            'Tempo': 40,
    #                            'Liveness': 95,
    #                            'Loudness': 60,
    #                            'Speechiness': 99}
    # output_window_root = tk.Tk()
    # output_window = NewPlaylistOutput(output_window_root,
    #                                   output_playlist_link,
    #                                   output_playlist_summary)
    # output_window.run_window()
    # output_window_root.mainloop()
