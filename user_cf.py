'''
Author: Yuhao_Wu
Date: 2022-08-03 18:28:36
LastEditors: Yuhao_Wu
LastEditTime: 2022-08-04 00:12:55
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
# each col is ONE movie's ratings from ALL users

# transpose: then,  each col is ONE user's ratings to ALl movies
# corr(): Compute pairwise Pearson correlation of COLUMNs, excluding NA/null
user_sim_mat = ratings_matrix.T.corr()  # (n_u, n_u)


def usercf_predict(uid, iid, ratings_matrix, user_sim_mat):
    '''
    Predicting the rating value of a given user for a given item
    :param uid: user ID
    :param iid: item ID
    :param ratings_matrix: user-item rating matrix
    :param user_similar: user-user sim matrix
    :return: output prediction of rating
    '''
    # print("Start predicting user <%d> rating on mov <%d>: "%(uid, iid))
    # 1. Find all similar users of this uid user
    # get non-nan corr: # drop himself & nan-simimlar user
    nonna_sim_users = user_sim_mat[uid].drop([uid]).dropna()

    # Similar user filtering rules: positively related users, where corr > 0
    similar_users = nonna_sim_users.where(
        nonna_sim_users > 0).dropna()  # series a col
    if similar_users.empty is True:
        # early end func
        raise Exception("user <%d> doesn't have similar users, early END..." %
                        uid)

    # 2. From the similar users of uid (corr > 0),
    #    filter out the similar users who have ratings on iid items
    ids = set(ratings_matrix[iid].dropna().index) & set(similar_users.index)
    finally_similar_users = similar_users.loc[list(ids)]  # series, a col

    # 3. Combining the similarity of uid users and their similar users,
    #   predicting the ratings of iid items by uid users - take into formula
    numerator = 0
    denominator = 0
    for sim_uid, sim_score in finally_similar_users.iteritems():
        # user ratings for items
        sim_user_rated_movies = ratings_matrix.loc[sim_uid].dropna()
        # sim user ratings for this iid item
        sim_user_rating_for_item = sim_user_rated_movies[iid]

        numerator += sim_score * sim_user_rating_for_item
        denominator += sim_score

    # Calculate the predicted score value and return
    # try:
    ## may throw Exception, catched by called function
    predict_rating = numerator / denominator
    # except ZeroDivisionError as e:
    #     print(e)
    #     raise Exception("No similarity")

    # print("Predict users <%d> rating on the movie <%d>：%0.2f" % (uid, iid, predict_rating))
    return round(predict_rating, 3)


# Predict all movie ratings for a particular user
def usercf_predict_all_mov(uid, ratings_matrix, user_similar):
    '''
    predict all movie ratings for this user uid, BEFORE ranking them
    :param uid: user id
    :param ratings_matrix: user-matix ratings matrix
    :param user_similar: user pairwise similarity matrix
    :return: a generator, with predicted ratings
    '''
    # 准备要预测的物品的id列表
    item_ids = ratings_matrix.columns
    # 逐个预测
    for iid in item_ids:
        '''
        catch Exception from predict function
        '''
        try:
            rating = usercf_predict(uid, iid, ratings_matrix, user_similar)
        except Exception as e:
            # print('error', e)
            pass
        else:  # no Exception then print
            yield uid, iid, rating


def top_k_rs_result(k, uid):
    results = usercf_predict_all_mov(uid, ratings_matrix, user_sim_mat)
    return sorted(results, key=lambda x: x[2], reverse=True)[:k]


def get_mov_by_id(mov_id, mov_df=movie_df):
    return mov_df.loc[mov_df['movieId'] == mov_id,
                      'title'].iloc[0]  # just 1 cell


def rec_mov(user_id, k, mov_df=movie_df):
    result = top_k_rs_result(k, user_id)
    movies_rec = [{
        'mov_id': mov_id,
        'predicted rating': rating,
        'movie': get_mov_by_id(mov_id, mov_df),
    } for _, mov_id, rating in result]

    return movies_rec


if __name__ == '__main__':

    k = 20
    uid = 1
    # result = top_k_rs_result(k, uid=uid)  # list of tuple, no movie name
    # print(result)

    movies_rec = rec_mov(uid, k)
    # y = json.dumps(x)
    # pprint(f'top {k} movies to recmmond to user <{user_id}>:')
    # pprint(movies_rec)
    pprint(f'top {k} movies to recmmond:')
    pprint(movies_rec)