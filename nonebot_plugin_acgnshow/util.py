from .config import BGIMAGE_PATH
import random
from pathlib import Path
def choose_random_bgimage():
    randomfile = random.choice(list(BGIMAGE_PATH.iterdir()))
    return str(randomfile)