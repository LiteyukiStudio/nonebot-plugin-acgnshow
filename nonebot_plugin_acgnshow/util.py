from .config import BGIMAGE_PATH
import random
def choose_random_bgimage():
    randomfile = random.choice(list(BGIMAGE_PATH.iterdir()))
    randomurl = randomfile.as_uri()
    return randomurl