import os
import re
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

    :param timestamp: unix 时间戳
    :return: yyyy-mm-dd hh:mm:ss时间
    """
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def extract_banner_url(value) -> str:
    a = json.loads(value)
    url = "https:"+a["banner"]["url"]
    return url

def add_https_to_urls(html_content):
    """
    为 HTML 内容中的缺失 https: 前缀的 URL 添加 https: 前缀

    :param html_content: 包含 HTML 的字符串
    :return: 修正后的 HTML 字符串
    """
    # 使用正则表达式查找所有以 "//" 开头的 URL
    updated_html_content = re.sub(r'(?<=src=["\'])//', 'https://', html_content)
    return updated_html_content

def split_html_into_fragments(html_content):
    """
    将 HTML 内容按照元素分割成多个片段，并存储在列表中

    :param html_content: 包含 HTML 的字符串
    :return: 存储 HTML 片段的列表
    """
    # 使用正则表达式匹配 HTML 标签及其内容
    pattern = re.compile(r'(<[^>]+>[^<]*<\/[^>]+>|<[^>]+\/>|<[^>]+>)')
    fragments = pattern.findall(html_content)
    return fragments

def join_fragments_in_groups(fragments, image_count=2):
    """

    :param fragments: 存储 HTML 片段的列表
    :param image_count: 每个组包含的图片数量，默认为2
    :return: 拼接后的 HTML 列表
    """
    grouped_html = []
    count = 0
    buffer = ""
    for group in fragments:
        buffer += group
        if "img" in group:
            count += 1 # 发现图片则计数器+1
        if count >= image_count:
            grouped_html.append(buffer)
            count = 0
            buffer = "" # 初始化计数器和缓冲区
    grouped_html.append(buffer)# 把缓冲区剩余内容一起添加
    return grouped_html