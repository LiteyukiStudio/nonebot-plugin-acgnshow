from nonebot import require, on_endswith
from nonebot.adapters import satori
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.typing import T_State
from typing import Optional
from .acgnapis import *
from nonebot_plugin_htmlrender import text_to_pic, template_to_pic
from nonebot_plugin_alconna import on_alconna
from arclet.alconna import Alconna, Args
from .config import RES_PATH, TEMPLATE_NAME, config
from .util import *
from .__init__ import __plugin_meta__
showcmd = on_alconna(
    Alconna(
        "展览",
        Args["region?", str]["page?", int]["date?", str],
    )
)
showcmd.shortcut(
    r"(?P<region>.+?)展览\s*(?P<page>\d+)?\s*(?P<date>.+)?",
    {
        "prefix": True,
        "command": "展览",
        "args": ["{region}", "{page}", "{date}"],
    }
)

@showcmd.handle()
async def find_show(
    state: T_State, region: Optional[str] = None, page: Optional[int] = None, date: Optional[str] = None,
):
    if not region: await showcmd.finish(__plugin_meta__.usage)
    if not page: page = 1
    if not date: date = ""
    regions_dict = get_regions_dict()
    regionid = regions_dict.get(region,None)
    if regionid == None: await showcmd.finish("未找到此地区") ; return
    #await showcmd.send("日期："+ date)
    shows = get_shows_data(regionid,page=page,pagesize=config.acgnshow_pagesize)
    # print(shows)
    template = {
        "shows":process_shows_data_to_template(shows),
        "bgimage": choose_random_bgimage()
        }
    pic = await template_to_pic(RES_PATH,TEMPLATE_NAME,template)
    # print(pic)
    # a = Image.open(io.BytesIO(pic))
    # a.save("template2pic.png", format="PNG")
    await showcmd.finish(MessageSegment.image(pic))