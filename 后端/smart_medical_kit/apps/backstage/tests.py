import requests
import json
from pyecharts.charts import Map, Geo
from pyecharts import options as opts
from pyecharts.globals import GeoType, RenderType
from django.test import TestCase


# Create your tests here.
class ChinaMap():
    def __init__(self):
        pass

    def main(self):
        # 1.目标网址
        url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
        # 2.模拟浏览器是先访问url,获取数据，由于数据是json形式，因此将其转化为字典形式，
        data = json.loads(requests.get(url).json()['data'])
        # 3.从网页源代码中提取数据
        china = data['areaTree'][0]['children']
        china_total = "确诊:" + str(data['chinaTotal']['confirm']) + \
                      " 疑似:" + str(data['chinaTotal']['suspect']) + \
                      " 死亡:" + str(data['chinaTotal']['dead']) + \
                      " 治愈:" + str(data['chinaTotal']['heal']) + \
                      " 更新日期:" + data['lastUpdateTime']
        # 4.将中国累计确诊，今日疑似，累计死亡，累计治愈，更新日期保存在数据中，显示在地图中上方
        excel0 = [data['chinaTotal']['confirm'], data['chinaTotal']['suspect'], data['chinaTotal']['dead'],
                  data['chinaTotal']['heal'], data['lastUpdateTime']]
        # 5.将中国各省市名称和对应的确诊人数存放在列表中
        data = []
        for i in range(len(china)):
            data.append([china[i]['name'], china[i]['total']['confirm']])
        # 6.将数据保存在另外,因为在下面会将data赋值为空
        excel1 = data
        # 7.对确诊人数进行从大到小的排序,使用冒泡排序
        for i in range(len(china) - 1):
            for j in range(len(china) - 1 - i):
                if excel1[j][1] < excel1[j + 1][1]:
                    excel1[j], excel1[j + 1] = excel1[j + 1], excel1[j]
        # 8.调用pyecharts中的Geo中国地图，并进行一些属性的设置，将各个国家的数据赋值到地图中
        geo = Geo(init_opts=opts.InitOpts(width="1750px", height="800px", bg_color="#404a59", page_title="全国疫情时事报告",
                                          renderer=RenderType.SVG, theme="white"))  # 设置绘图尺寸，背景色
        geo.add_schema(maptype="china", itemstyle_opts=opts.ItemStyleOpts(color="rgb(49,60,72)",
                                                                          border_color="rgb(0,0,0)"))  # 中国地图，地图区域颜色，区域边界颜色
        geo.add(series_name="china", data_pair=data, type_=GeoType.EFFECT_SCATTER)  # 设置地图数据，动画方式位涟漪特效 effect scatter
        geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False), effect_opts=opts.EffectOpts(scale=6))
        geo.set_global_opts(visualmap_opts=opts.VisualMapOpts(min_=0, max_=349),
                            title_opts=opts.TitleOpts(title="全国疫情地图", subtitle=china_total, pos_right="10px",
                                                      pos_left="center",
                                                      pos_top="50px"))
        geo.render("../../temlates/map.html")


if __name__ == '__main__':
    a = ChinaMap()
    a.main()
