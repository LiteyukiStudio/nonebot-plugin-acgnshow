from .config import BGIMAGE_PATH
import random
import datetime


def choose_random_bgimage():
    randomfile = random.choice(list(BGIMAGE_PATH.iterdir()))
    randomurl = randomfile.as_uri()
    return randomurl


def convert_timestamp(timestamp):
    obj = datetime.datetime.fromtimestamp(timestamp)
    formatted_time = obj.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time
