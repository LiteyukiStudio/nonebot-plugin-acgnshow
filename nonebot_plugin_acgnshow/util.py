import os
import random
import datetime

from .config import BGIMAGE_PATH


def choose_random_bgimage() -> str:
    """
    从背景图片文件夹中随机选择一张图片，返回图片的uri地址
    """
    randomfile = random.choice(os.listdir(BGIMAGE_PATH))
    randomurl = (BGIMAGE_PATH / randomfile).as_uri()
    return randomurl


def convert_timestamp(timestamp) -> str:
    """
    将时间戳转换为日期格式
    """
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
