
import re
import sys
import io
import requests
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
from map import gen_map, get_map_data

# #pandas写入excel
# def pd_toExcel(data, fileName):  # pandas库储存数据到excel
#     ids = []
#     titles = []
#     totals = []
#     medians = []
#
#     for i in range(len(data)):
#         ids.append(data[i]["id"])
#         titles.append(data[i]["title"])
#         totals.append(data[i]["total"])
#         medians.append(data[i]["median"])
#
#     dfData = {  # 用字典设置DataFrame所需数据
#         'id' : ids,
#         'title': titles,
#         'total' : totals,
#         'median' : medians,
#     }
#     df = pd.DataFrame(dfData)  # 创建DataFrame
#     df.to_excel(fileName, index=False)  # 存表，去除原始索引列（0,1,2...）

# 获取链接
def getLinks(ID):
    url = "https://manbow.nothing.sh/event/event.cgi?action=More_def&num=" + str(ID) + "&event=137"
    req = requests.get(url)
    req.encoding = "shift-jis"
    bsObj = BeautifulSoup(req.text)
    return bsObj

# 生成包含作品全部信息的字典
def gen_dict(ID, work):
    try:
        title = work.find("h2").get_text().strip()
        artist = work.find("h3", {"style": "margin-bottom:20px;"}).get_text().strip()
        total = work.find("div", {"id": "score_total"}).get_text()
        med = work.find("div", {"id": "score_med"}).get_text()
        ave = work.find("div", {"id": "score_ave"}).get_text()

        countries = work.findAll("img", {"class": "flag"})
        countries_dict = {}
        impre_count = 0
        for country in countries:
            impre_count = impre_count + 1
            country = country.attrs['title']
            if country not in countries_dict.keys():
                countries_dict[country] = 1
            else:
                countries_dict[country] = countries_dict[country] + 1

        countries_sorted = sorted(countries_dict.items(), key=lambda x:x[0])
        countries_sorted = dict(countries_sorted)

        work_list = {'ID': ID, 'Title': title, 'Artist': artist, 'Total': total, 'Median': med, 'Average': ave, 'Total Impre': impre_count, 'Countries': countries_sorted}
        return work_list
    except AttributeError:
        return None

ID_count = 1
while ID_count <= 482:
    listx = []
    work = getLinks(ID_count)
    work_list = gen_dict(ID_count, work)
    if work_list:
        listx.append(work_list)
        print(work_list)
        data = get_map_data(work_list)
        gen_map(ID_count, work_list['Title'], data)
    ID_count = ID_count + 1

