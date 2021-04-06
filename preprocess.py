"""
Script for preprocessing the input data from kaggle.
The raw data can be found at:
https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks?select=data.csv


This file will normalize all the values in the graph to be a float ranging from 0 to 1.
Generally, this will be done by finding a min and a max value for each category and then
refactoring every other value to be a percent float based on those value

This file will also reorganize the columns of the data so that it is easier to access
the required data and remove the release_date column.

Specifically, from left to right, the columns will be organized as follows:

Categorical
    1. id
    2. name
    3. artist
    4. year
    5. explicit
    6. mode
Numerical/Music
    6. acousticness (Ranges from 0 to 1)
    7. danceability (Ranges from 0 to 1)
    8. energy (Ranges from 0 to 1)
    9. duration_ms (Integer typically ranging from 200k to 300k)
    10. instrumentalness (Ranges from 0 to 1)
    11. valence (Ranges from 0 to 1)
    12. popularity (Ranges from 0 to 100)
    13. tempo (Float typically ranging from 50 to 150)
    14. liveness (Ranges from 0 to 1)
    15. loudness (Float typically ranging from -60 to 0)
    16. speechiness (Ranges from 0 to 1)
    17. key
"""
import pandas as pd

def normalize_df(df: pd.DataFrame, column_name: str):
    """Normalizes every value in the specified column in the dataframe.

    The normalization is done by finding the min and max value in the column and
    then subtracting every value in by min and dividing by max-min.

    Preconditions:
        - column_name in df.keys()
        - columns only have numerical values stored in them
    """
    min_val = df[column_name].min()
    max_val = df[column_name].max() - min_val

    df[column_name] -= min_val
    df[column_name] /= max_val


def preprocess_data(file_name: str, columns_to_reorder: list, columns_to_normalize: list, processed_name: str):
    """Reads the .csv file stored a Data/file_name and then reorders and normalizes the
    columns according to the docstring at the top of this file. A new .csv file is generated
    named normalized_file_name in the Data folder.

    Preconditions:
        - file_name is a .csv file in the Data folder
        - file_name is formatted as specified on the database website at top of file
    """
    file_path = 'Data/'+file_name
    music_df = pd.read_csv(file_path)
    df_reorder = music_df.reindex(columns=columns_to_reorder)
    for column in columns_to_normalize:
        normalize_df(df_reorder, column)

    df_reorder.to_csv('Data/normalized_' + processed_name, index=False)


if __name__ == "__main__":
    file = "music_data.csv"
    columns_titles = ["id", "name", "artists", "year", "explicit", "mode", "acousticness", "danceability",
                      "energy", "duration_ms", "instrumentalness", "valence", "popularity", "tempo",
                      "liveness", "loudness", "speechiness", "key"]
    columns_dropped_titles = ["year", "acousticness",
                      "danceability",
                      "energy", "duration_ms", "instrumentalness", "valence", "popularity", "tempo",
                      "liveness", "loudness", "speechiness", "key"]

    columns_more_dropped_titles = ['id', "acousticness", "danceability", "energy", "duration_ms", "instrumentalness", "valence", "tempo","liveness", "loudness", "speechiness", "key"]

    columns_to_normalize = ['duration_ms', 'tempo', 'loudness', 'key']
    # Call the following function to process data:
    preprocess_data(file, columns_more_dropped_titles, columns_to_normalize, 'Hayks data with id.csv')
