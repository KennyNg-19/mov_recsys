#-*- coding: utf-8 -*-
'''
Author: Yuhao_Wu wuyuhao2019@126.com
Date: 2022-08-02 16:27:04
LastEditors: Yuhao_Wu
LastEditTime: 2022-08-04 14:47:41
Description: The file for building Fastapi.
'''

# Python standard/ 3rd-party / local modules
from typing import Union

from fastapi import FastAPI
from pprint import pprint

from user_cf import *

# build fastapi
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello MovieLens-small RecSys"}


@app.get("/rec/{user_id}")
# async def read_item(user_id: int, k:int):
async def read_item(user_id: int, k: Union[int, None] = 10):
    """given a user, output top K predicted movies as recommendations

    Args:
        user_id (int): target user id
        k (Union[int, None], optional): top K recommended movies. Defaults to 10.

    Returns:
        a list of tuple: movie recommendations with scores
    """
    movies_rec = rec_mov(user_id, k)

    return {f"top{k}_recmmond_movs": movies_rec}
    # return json.dumps(movies_rec)
