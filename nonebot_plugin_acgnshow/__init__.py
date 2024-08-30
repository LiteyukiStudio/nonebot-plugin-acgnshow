from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_htmlrender")
require("nonebot_plugin_alconna")
from .acgnshower import *
from nonebot import get_driver
from .config import ConfigModel

usage = """命令格式：
展览 <地区> [页码]
或
<地区>展览 [页码]
获取指定地区的展览列表
其中地区为省级行政区或地级行政区（不包含后缀）
（如北京，福建，平顶山，绍兴，香港...，或海外/全国）

展览详情 <ID>
获取指定展览ID的详细信息
其中ID为展览列表处返回的ID

示例：
展览 福建 2
福建展览 2
全国展览
海外展览
展览详情 86827

※数据来源于哔哩哔哩会员购，由于API返回结果与实际存在差异，数据可能不准确。"""
__author__ = "Asankilp"
__plugin_meta__ = PluginMetadata(
    name="漫展/展览查询",
    description="从哔哩哔哩会员购获取简易展览数据",
    usage=usage,
    type="application",
    config=ConfigModel,
    homepage="https://github.com/LiteyukiStudio/nonebot-plugin-acgnshow",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    # extra={"License":"MIT","Author":"Swankily"} snowykami的奇妙纠错（
    extra={"License": "MIT", "Author": "Asankilp"},
)
driver = get_driver()


@driver.on_startup
async def _():
    pass
