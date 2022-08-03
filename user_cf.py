'''
Author: Yuhao_Wu
Date: 2022-08-03 18:28:36
LastEditors: Yuhao_Wu
LastEditTime: 2022-08-03 23:31:26
Description: A runnable script contains all data process and user-based CF functions
'''

import numpy as np
import pandas as pd
from pprint import pprint

rating_path = "ml-latest-small/ratings.csv"
dtype = {"userId": np.int32, "movieId": np.int32, "rating": np.float32}
# load the data, we only use the first three columns of data,
# which are the user ID, the movie ID, and the corresponding rating of the movie by that user
rating_df = pd.read_csv(rating_path, dtype=dtype, usecols=range(3))

movie_path = "ml-latest-small/movies.csv"
movie_df = pd.read_csv(movie_path)

# Pivot table, converting movie IDs to column names, into a User-Movie rating matrix in DF
ratings_matrix = rating_df.pivot_table(index=["userId"],
                                       columns=["movieId"],
                                       values="rating")  # Data frame
n_u, n_mov = ratings_matrix.shape
print(f'Reading data, ml-latest-small:\nno. user: {n_u}\nno. mov: {n_mov}')