from typing import Dict

from aiohttp import ClientSession

from .models import *
from .util import *

CITY_API_ROOT = "https://show.bilibili.com/api/ticket/city/list?channel=3"
SHOWS_API_ROOT = "https://show.bilibili.com/api/ticket/project/listV2"
SHOW_DETAILS_API_ROOT = "https://show.bilibili.com/api/ticket/project/getV2"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Linux; Android 14; 114514YAJU Build/UKQ1.114514.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/125.0.6422.165 Mobile Safari/537.36 BiliApp/7810200 mobi_app/android isNotchWindow/0 NotchHeight=34 mallVersion/7810200 mVersion/242 disable_rcmd/0 7.81.0 os/android model/114514YAJU mobi_app/android build/7810200 channel/bilih5 innerVer/7810210 osVer/14 network/2"
}


async def get_cities_data() -> CityResp:
    """
    返回支持的城市数据
    """
    async with ClientSession() as session:
        async with session.get(CITY_API_ROOT, headers=HEADERS) as resp:
            regions_data = await resp.json()
    return CityResp.model_validate(regions_data)


async def get_regions_dict() -> Dict[str, int]:
    """
    返回支持的地区，键名为地区名，键值为地区id
    """
    data = {}
    city_data = await get_cities_data()
    for i in city_data.data.list:
        for j in i.city_list:
            data.update({j.name: j.id})
    data.update({"全国": -1, "海外": 900000})
    return data


async def get_shows_data(region_id: int, page=1, pagesize=20):
    """
    返回举办中/即将举办/取消举办的展览数据
    Args:
        region_id: 地区id
        page: 页码
        pagesize: 一页最大条目数，最大20
    """
    param = {
        "version": 133,
        "area": region_id,
        "page": page,
        "pagesize": pagesize,
        "platform": "web",
        "p_type": "展览",
        "style": 1,
    }
    async with ClientSession() as session:
        async with session.get(SHOWS_API_ROOT, headers=HEADERS, params=param) as resp:
            shows_data = await resp.json()
    return shows_data

async def get_show_details(show_id: int):
    param = {
        "id": show_id,
        "project_id": show_id,
        "requestSource": "neul-next"
    }
    async with ClientSession() as session:
        async with session.get(SHOW_DETAILS_API_ROOT, headers=HEADERS, params=param) as resp:
            show_details_data = await resp.json()
    return show_details_data

def process_show_details_data_to_template(show_details_data: dict):
    data = show_details_data["data"]
    
    banner_url = "https:"+data["banner"]
    # banner_url = extract_banner_url(data["performance_image"])
    
    # 提取事件基本信息
    name = data["name"]
    start_time = convert_timestamp(data["start_time"])
    end_time = convert_timestamp(data["end_time"])
    
    # 提取场馆信息
    venue_name = data["venue_info"]["name"]
    venue_detail = data["venue_info"]["address_detail"]
    
    # 提取主办方信息
    organizer = data["merchant"]["company"]
    
    # 提取实名制，退票等信息
    is_refund = data["is_refund"]
    id_bind = data["id_bind"]
    has_eticket = data["has_eticket"]

    # 提取票务信息
    ticket_info = []
    for screen in data.get("screen_list", []):
        for ticket in screen.get("ticket_list", []):
            ticket_info.append({
                "description": ticket.get("desc", ""),
                "price": ticket.get("price", 0),
                "sale_start": convert_timestamp(ticket.get("saleStart", 0)),
                "sale_end": convert_timestamp(ticket.get("saleEnd", 0)),
                "status": ticket.get("sale_flag", {}).get("display_name", ""),
                "screen_name": ticket.get("screen_name")
            })
    guests_list = data["guests"]
    if guests_list != None:
        guests = "、".join(n["name"] for n in guests_list)
    else:
        guests = ""
    
    desc = data["performance_desc"]["list"]
    for item in desc:
        if item.get("module") == "activity_content":
            details_html = item.get("details", "")

    # 构建返回的字典
    item_dict = {
        "banner_url": banner_url,
        "name": name,
        "start_time": start_time,
        "end_time": end_time,
        "venue_name": venue_name,
        "venue_detail": venue_detail,
        "organizer": organizer,
        "ticket_info": ticket_info,
        "guests": guests,
        "is_refund": is_refund,
        "id_bind": id_bind,
        "has_eticket": has_eticket,
        "details_html": details_html
    }
    
    return [item_dict, details_html]

def process_shows_data_to_template(shows_data: dict):
    showlist = []
    data = shows_data["data"]
    page = data["page"]
    total_pages = data["numPages"]
    total_results = data["total"]
    result = data["result"]
    # show_template = read_template_file('/home/asankilp/LiteyukiBot/src/plugins/acgnshow/res/template.html')
    for i in result:
        name = i["project_name"]
        venue_name = i["venue_name"]
        project_id = i["project_id"]
        sale_flag = i["sale_flag"]
        # start_time = i["start_time"]
        start_unix = i["start_unix"]
        start_time = convert_timestamp(start_unix)
        end_time = i["end_time"]
        price_low = i["price_low"] / 100
        price_high = i["price_high"] / 100
        district_name = i["district_name"]
        wish = i["wish"]
        cover = "https:" + i["cover"]
        if district_name == None:
            district_name = ""
        guests_list = i["guests"]
        if guests_list != None:
            guests = "、".join(n["name"] for n in guests_list)
        else:
            guests = ""
        item_dict = {
            "name": name,
            "location": district_name + venue_name,
            "sale_flag": sale_flag,
            "id": project_id,
            "price_low": price_low,
            "price_high": price_high,
            "start_time": start_time,
            "end_time": end_time,
            "wish": wish,
            "image_url": cover,
            "guests": guests,
            "page": page,
            "total_pages": total_pages,
        }
        showlist.append(item_dict)
    global_data_dict = {
        "page": page,
        "total_pages": total_pages,
        "total_results": total_results,
    }
    return [showlist, global_data_dict]
