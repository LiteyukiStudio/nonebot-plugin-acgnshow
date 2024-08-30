import traceback

from typing import Optional
from .acgnapis import *
from nonebot_plugin_htmlrender import template_to_pic, html_to_pic
from nonebot_plugin_alconna import on_alconna
from nonebot_plugin_alconna.uniseg import UniMessage
from arclet.alconna import Alconna, Args
from .config import RES_PATH, LIST_TEMPLATE_NAME, DETAILS_TEMPLATE_NAME, config
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
    },
)
showcmd_details = on_alconna(
    Alconna(
        "展览详情",
        Args["id?", int],  # 这里定义了一个必需的 int 参数 "id"
    )
)
showcmd_details.shortcut(
    r"展览详情\s*(?P<id>\d+)",  # 正则表达式匹配 "展览详情" 后跟一个整数 ID
    {
        "prefix": True,
        "command": "展览详情",
        "args": ["{id}"],  # 将 ID 参数传递给命令
    },
)

@showcmd_details.handle()
async def get_show_details_cmd(
    id: Optional[int] = None
):
    show_details = await get_show_details(id)
    if show_details["errno"] != 0: await UniMessage("发生错误").send() ; return
    try:
        show_details_data = process_show_details_data_to_template(show_details)
        #print(show_details_data)
        template = {
            "show": show_details_data[0],
            "bgimage": choose_random_bgimage(),
        }
        pic = await template_to_pic(str(RES_PATH), DETAILS_TEMPLATE_NAME, template)
    except Exception as e:
        await UniMessage(f"图片生成时产生错误:\n{str(e)}").send()
        traceback.print_exc()
        return
    await UniMessage.image(raw=pic).send()
    if config.acgnshow_send_show_details_html:
        details_html_fragments = split_html_into_fragments(add_https_to_urls(show_details_data[1]))
        details_html_groups = join_fragments_in_groups(details_html_fragments, config.acgnshow_show_details_html_img_count)
        #print(details_html_groups)
        #print(details_html)
        for html in details_html_groups:
            html_pic = await html_to_pic(html=html, device_scale_factor=config.acgnshow_show_details_html_scale)
            #print(html_pic)
            await UniMessage.image(raw=html_pic).send()

@showcmd.handle()
async def find_shows_cmd(
    region: Optional[str] = None,
    page: Optional[int] = None,
    date: Optional[str] = None,
):
    if not region:
        await UniMessage(__plugin_meta__.usage).send()
        return
    if len(region) > 5:
        return
    if not page:
        page = 1
    if not date:
        date = ""
    regions_dict = await get_regions_dict()
    regionid = regions_dict.get(region, None)
    if regionid == None:
        await UniMessage("地区未寻得或输入格式错误").send()
        return
    # await showcmd.send("日期："+ date)
    shows = await get_shows_data(regionid, page=page, pagesize=config.acgnshow_pagesize)
    # print(shows)
    try:
        shows_data = process_shows_data_to_template(shows)
        template = {
            "shows": shows_data[0],
            "bgimage": choose_random_bgimage(),
            "global_data": shows_data[1],
        }
        pic = await template_to_pic(str(RES_PATH), LIST_TEMPLATE_NAME, template)
    except Exception as e:
        await UniMessage(f"图片生成时产生错误:\n{str(e)}").send()
        traceback.print_exc()
        return

    await UniMessage.image(raw=pic).send()
