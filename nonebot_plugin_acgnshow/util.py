import os
import random
import datetime
import json
from pathlib import Path
from .config import config


def choose_random_bgimage() -> str:
    """
    从背景图片文件夹中随机选择一张图片，返回图片的uri地址
    """
    bgpath = Path(config.acgnshow_bgimage_path)
    randomfile = random.choice(os.listdir(bgpath))
    randomurl = (bgpath / randomfile).as_uri()
    return randomurl


def convert_timestamp(timestamp) -> str:
    """
    将时间戳转换为日期格式
    """
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def extract_banner_url(value) -> str:
    a = json.loads(value)
    url = "https:"+a["banner"]["url"]
    return url