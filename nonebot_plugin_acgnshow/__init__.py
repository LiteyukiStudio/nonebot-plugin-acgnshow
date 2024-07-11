from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require
require("nonebot_plugin_htmlrender")
require("nonebot_plugin_alconna")
from .acgnshower import *
from nonebot import get_driver
from .config import ConfigModel
__author__ = "Asankilp"
__plugin_meta__ = PluginMetadata(
    name="漫展/展览查询",
    description="从哔哩哔哩会员购获取简易展览数据",
    usage="application",
    config=ConfigModel,
    homepage="https://github.com/LiteyukiStudio/nonebot-plugin-acgnshow",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna")
)
driver = get_driver()


@driver.on_startup
async def _():
    pass

