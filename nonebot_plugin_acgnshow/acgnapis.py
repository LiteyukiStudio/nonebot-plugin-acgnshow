import json
import requests
CITY_API_ROOT="https://show.bilibili.com/api/ticket/city/list?channel=3"
SHOWS_API_ROOT="https://show.bilibili.com/api/ticket/project/listV2"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Linux; Android 14; 114514YAJU Build/UKQ1.114514.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/125.0.6422.165 Mobile Safari/537.36 BiliApp/7810200 mobi_app/android isNotchWindow/0 NotchHeight=34 mallVersion/7810200 mVersion/242 disable_rcmd/0 7.81.0 os/android model/114514YAJU mobi_app/android build/7810200 channel/bilih5 innerVer/7810210 osVer/14 network/2"
    }
def get_regions_data():
    '''
    返回支持的地区数据
    '''
    regions_data = json.loads(requests.get(CITY_API_ROOT, headers=HEADERS).text)
    return regions_data
def get_regions_dict():
    '''
    返回支持的地区，键名为地区名，键值为地区id
    '''
    dicts = {}
    cityjson = get_regions_data()
    for i in cityjson["data"]["list"]:
        for j in i["city_list"]:
            name = j["name"]
            id = j["id"]
            dicts.update({name: id})
    dicts.update({"全国": -1,"海外": 900000}) #添加api中未返回的结果
    #print(dicts)
    return dicts
def get_shows_data(region_id: int, page=1, pagesize=20):
    '''
    返回举办中/即将举办/取消举办的展览数据
    Args:
        region_id: 地区id
        page: 页码
        pagesize: 一页最大条目数，最大20
    '''
    param = {
        "version": 133,
        "area": region_id,
        "page": page,
        "pagesize": pagesize,
        "platform": "web",
        "p_type": "展览",
        "style": 1
    }
    shows_data = json.loads(requests.get(SHOWS_API_ROOT, headers=HEADERS,params=param).text)
    return shows_data
def process_shows_data_to_text(shows_data: dict):
    showlist = []
    data = shows_data["data"]
    total_pages = data["numPages"]
    result = data["result"]
    for i in result:
        name = i["project_name"]
        venue_name = i["venue_name"]
        project_id = i["project_id"]
        sale_flag = i["sale_flag"]
        start_time = i["start_time"]
        end_time = i["end_time"]
        price_low = i["price_low"] / 100
        price_high = i["price_high"] / 100
        district_name = i["district_name"]
        text = f"名称：{name}\n举办地:{venue_name}\nid:{project_id}\nflag:{sale_flag}\n开始时间:{start_time}\n结束时间:{end_time}\n最低票价:{price_low}\n最高票价:{price_high}\n区名:{district_name}\n\n"
        showlist.append(text)
    return showlist

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
        start_time = i["start_time"]
        end_time = i["end_time"]
        price_low = i["price_low"] / 100
        price_high = i["price_high"] / 100
        district_name = i["district_name"]
        wish = i["wish"]
        cover = "https:" + i["cover"]
        if district_name == None : district_name = ""
        item_dict = {
            "name": name,
            "location": district_name + venue_name,
            "sale_flag": sale_flag,
            "id": project_id,
            "price": price_low,
            "start_time": start_time, 
            "end_time": end_time, 
            "wish": wish,
            "image_url": cover,
            "page": page,
            "total_pages": total_pages
            }
        showlist.append(item_dict)
    global_data_dict = {
        "page": page,
        "total_pages": total_pages,
        "total_results": total_results
    }
    return [showlist, global_data_dict]