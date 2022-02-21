
from pyecharts import options as opts
from pyecharts.charts import Map
from country_conv import list_convert

import re

# 处理作品的国家数据
def get_map_data(work_list):
    country_list = work_list["Countries"]
    countries = list_convert(list(country_list.keys()))
    countries_new = []
    for country in countries:
        if country == 'South Korea':
            countries_new.append('Korea')
        else:
            countries_new.append(country)
    votes_list = list(country_list.values())
    data = list(zip(countries_new, votes_list))

    return data

# 用pyecharts生成交互式地图（.html形式）
def gen_map(ID, title, data):

    _map = (
        Map()
        .add("Votes", data, "world")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Votes"),
            legend_opts=opts.LegendOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(max_=100, is_piecewise=True),
        )
        .set_series_opts(label_opts=opts.LegendOpts(is_show=False))
    )

    # 利用正则表达式去除不能用于文件命名的特殊字符
    title = re.findall(r'[^\*"/:?\\|<>]', title, re.S)
    title = "".join(title)

    _map.render(path = "output\\" + str(ID) + '.' + title + ".html")