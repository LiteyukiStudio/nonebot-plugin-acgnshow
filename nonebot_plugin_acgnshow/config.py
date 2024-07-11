from pathlib import Path
from pydantic import BaseModel
from nonebot import get_plugin_config
RES_PATH = Path(__file__).parent / "res"
TEMPLATE_NAME = "template.html"
BGIMAGE_PATH = RES_PATH / "bgimage"

class ConfigModel(BaseModel):
    acgnshow_pagesize: int = 8

config: ConfigModel = get_plugin_config(ConfigModel)