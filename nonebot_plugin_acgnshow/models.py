# -*- coding: utf-8 -*-
"""
Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved 

@Time    : 2024/8/15 下午5:50
@Author  : snowykami
@Email   : snowykami@outlook.com
@File    : models.py
@Software: PyCharm
"""
from typing import List

from pydantic import BaseModel


class City(BaseModel):
    """
    热门城市
    """

    id: int
    type: int
    first_letter: str
    name: str
    fullname: str
    num: int
    parent_id: int
    booked: bool


class CityDataList(BaseModel):
    """
    城市首字母
    """

    letter: str
    city_list: List[City]


class CityData(BaseModel):
    """
    城市数据
    """

    hot: List[City]
    list: List[CityDataList]
    located_id: int


class CityResp(BaseModel):
    """
    城市数据
    """

    errno: int
    errtag: int
    msg: str
    data: CityData
