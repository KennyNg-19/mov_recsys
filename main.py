#-*- coding: utf-8 -*-
'''
Author: Yuhao_Wu wuyuhao2019@126.com
Date: 2022-08-02 16:27:04
LastEditors: Yuhao_Wu
LastEditTime: 2022-08-04 18:14:14
Description: The file for building Fastapi.
'''

# Python standard/ 3rd-party / local modules
from typing import Union

from fastapi import FastAPI, Path, Query
from pprint import pprint

from user_cf import *

# build fastapi
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello MovieLens-small RecSys"}


@app.get("/rec/{user_id}")
# async def read_item(user_id: int, k:int):
# declare additional information and validation for input parameters.
async def read_item(user_id: int = Path(title="The ID of target user"),
                    k: Union[int, None] = 10):
    """given a user, output top K predicted movies as recommendations

    Args:
        user_id (int): target user id
        k (Union[int, None], optional): top K recommended movies. Defaults to 10.

    Returns:
        a list of tuple: movie recommendations with scores
    """
    try:
        user_id = int(user_id)
    except ValueError:
        print("Not an integer! Try again.")
    else:
        movies_rec = rec_mov(user_id, k)

        return {f"top{k}_recmmond_movs": movies_rec}
        # return json.dumps(movies_rec)
