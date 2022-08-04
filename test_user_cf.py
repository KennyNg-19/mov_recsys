'''
Author: Yuhao_Wu
Date: 2022-08-04 01:38:04
LastEditors: Yuhao_Wu
LastEditTime: 2022-08-04 12:41:41
Description: 
'''
import numpy as np
import pandas as pd

from user_cf import *


def test_get_mov_by_id():
    movie_path = "ml-latest-small/movies.csv"
    movie_df = pd.read_csv(movie_path)
    assert get_mov_by_id(1) == movie_df.loc[0]["title"]  # get 1st line


# test on
def test_predict_item_score():
    d = {
        1: [2, 1, 1, 5, 1],
        2: [4, np.nan, 0, 1, 5],
        3: [5, 4, 4, 2, 3],
        4: [0, 0, 3, 0, 0],
        5: [1, 2, 0, 5, 3]
    }
    ratings_matrix = pd.DataFrame(data=d, index=[1, 2, 3, 4, 5])
    user_sim_mat = ratings_matrix.T.corr()

    # to predict the nan value in (2,2)
    uid, iid = 2, 2
    nonna_user_simscores = user_sim_mat[uid].drop([uid]).dropna()
    users_pos_simscores = nonna_user_simscores.where(
        nonna_user_simscores > 0).dropna()  # series, a col
    if users_pos_simscores.empty is True:
        # early end func
        raise Exception("user <%d> doesn't have similar users, early END..." %
                        uid)

    # 2. get ratings from other users on same iid item
    ids = set(ratings_matrix[iid].dropna().index) & set(
        users_pos_simscores.index)
    users_sim_rated_items = users_pos_simscores.loc[list(ids)]  # series, a col

    assert round(predict_item_score(iid, ratings_matrix, users_sim_rated_items), 1) == 3.6
