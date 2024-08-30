from pathlib import Path
from pydantic import BaseModel
from nonebot import get_plugin_config

RES_PATH = Path(__file__).parent / "res"
LIST_TEMPLATE_NAME = "template.html"
DETAILS_TEMPLATE_NAME = "details.html"
BGIMAGE_PATH = RES_PATH / "bgimage"


class ConfigModel(BaseModel):
    acgnshow_pagesize: int = 8
    acgnshow_bgimage_path: str = BGIMAGE_PATH
    acgnshow_send_show_details_html: bool = False
    acgnshow_show_details_html_scale: float = 0.6
    acgnshow_show_details_html_img_count: int = 2

config: ConfigModel = get_plugin_config(ConfigModel)
