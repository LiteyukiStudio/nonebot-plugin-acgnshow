<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/LiteyukiStudio/nonebot-plugin-acgnshow/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/LiteyukiStudio/nonebot-plugin-acgnshow/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-acgnshow

_✨ 从哔哩哔哩会员购获取展览简易信息 ✨_

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/LiteyukiStudio/nonebot-plugin-acgnshow.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-acgnshow">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-acgnshow.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

## 📖 介绍

一个简单的 Nonebot2 插件，可以从哔哩哔哩会员购 API 获取展览（漫展等）的时间，地点，票价等信息。

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-acgnshow

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-acgnshow

</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-acgnshow

</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-acgnshow

</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-acgnshow

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_acgnshow"]

</details>

## 🎉 使用

发送`展览`指令可以获取使用说明

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的配置

|      配置项       | 必填 | 默认值 |                             说明                             |
| :---------------: | :--: | :----: | :----------------------------------------------------------: |
| ACGNSHOW_PAGESIZE |  否  |   8    | 单个图片的条目数，最大为 20，条目数过大可能导致 Bot 无法发送 |
| ACGNSHOW_BGIMAGE_PATH | 否 | 插件内置背景图 | 插件返回图片的背景图目录路径 |
| ACGNSHOW_SEND_SHOW_DETAILS_HTML | 否 | false | 是否发送展览的 HTML 详情信息图片（会员购的“活动介绍”栏目），实验性功能 |
| ACGNSHOW_SHOW_DETAILS_HTML_SCALE | 否 | 0.6 | HTML 详情信息图片的缩放比例，过大可能导致 Bot 无法发送 |
| ACGNSHOW_SHOW_DETAILS_HTML_IMG_COUNT | 否 | 2 | 每一张 HTML 详情信息图片中包含的图片个数，过大可能导致 Bot 无法发送 |
