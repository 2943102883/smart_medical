import json
import logging

from django import http
from django.shortcuts import render
import requests
import json
from pyecharts.charts import Map, Geo
from pyecharts import options as opts
from pyecharts.globals import GeoType, RenderType
# Create your views here.
from django.views import View

from apps.medicine.models import Medicine_user
from apps.user.models import Users
from utils.response_code import RETCODE

logger = logging.getLogger('django')


class RegisterUser(View):
    """
    注册人数
    """

    def get(self, request):
        user = Users.objects.filter()
        num = len(user)
        return http.JsonResponse({'code': RETCODE.OK, 'num': num})


class MessageView(View):
    """
    获取所有注册用户的信息
    废弃了
    """

    def get(self, request):
        user = Users.objects.all()
        num = len(user)
        data_dict = {}
        for n in range(num):
            dict_in = {}
            sex = user[n].sex
            age = user[n].age
            weigth = user[n].weight
            height = user[n].height
            health = user[n].health
            contacts = user[n].contacts
            creat_data = user[n].creat_data
            name = user[n].name
            birthday = user[n].birthday
            phone = user[n].phone

            dict_in['sex'] = sex
            dict_in['age'] = age
            dict_in['weigth'] = weigth
            dict_in['height'] = height
            dict_in['health'] = health
            dict_in['contacts'] = contacts
            dict_in['creat_data'] = creat_data
            dict_in['name'] = name
            dict_in['birthday'] = birthday
            dict_in['phone'] = phone

            data_dict[n + 1] = dict_in

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'data': data_dict})


class UserView(View):
    def post(self, request):
        """
        增加会员用户
        微信小程序是用户自行创建的，需要绑定微信的token，所以管理页面无法添加用户
        """
        pass

    def delete(self, request):
        """
        删除会员用户
        删除用户后，后台是逻辑删除。当下一次创建的时候，如果后天检测到这个账号曾经注册过，则将原来的数据加载
        需请求体中传入token
        """
        data = json.loads(request.body.decode())
        token = data.get('token')
        try:
            Users.objects.filter(token=token).delete()
        except Exception as e:
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '数据库错误，删除失败'})

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '删除成功'})

    def put(self, request):
        """
        修改会员用户信息
        需请求体中传入token
        """
        try:
            data = json.loads(request.body.decode())
        except Exception as e:
            return http.JsonResponse({'code': RETCODE.PARAMERR, 'errmsg': '请以json格式传入'})
        token = data.get('token')
        name = data.get('name')
        sex = data.get('sex')
        age = data.get('age')
        weight = data.get('weight')
        height = data.get('height')
        health = data.get('health')
        contacts = data.get('contacts')
        phone = data.get('phone')
        birthday = data.get('birthday')

        if not token:
            return http.JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '未传递token'})
        else:
            try:
                Users.objects.filter(token=token).update(
                    name=name,
                    sex=sex,
                    age=age,
                    weight=weight,
                    height=height,
                    health=health,
                    contacts=contacts,
                    phone=phone,
                    birthday=birthday
                )
                return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '修改成功'})
            except Exception as e:
                logger.error(e)
                return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '修改失败'})

    def get(self, request):
        """
        查询会员用户信息
        """
        token = request.GET.get('token')
        if token is None:
            # 如果没有传token的话，默认返回所有用户数据
            user = Users.objects.all()
            num = len(user)
            data_dict = {}
            for n in range(num):
                dict_in = {}
                sex = user[n].sex
                age = user[n].age
                weigth = user[n].weight
                height = user[n].height
                health = user[n].health
                contacts = user[n].contacts
                creat_data = user[n].creat_data
                name = user[n].name
                birthday = user[n].birthday
                phone = user[n].phone

                dict_in['sex'] = sex
                dict_in['age'] = age
                dict_in['weigth'] = weigth
                dict_in['height'] = height
                dict_in['health'] = health
                dict_in['contacts'] = contacts
                dict_in['creat_data'] = creat_data
                dict_in['name'] = name
                dict_in['birthday'] = birthday
                dict_in['phone'] = phone

                data_dict[n + 1] = dict_in

            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'data': data_dict})
        else:
            try:

                user = Users.objects.get(token=token)
                data_dict = {}
                sex = user.sex
                age = user.age
                weigth = user.weight
                height = user.height
                health = user.health
                contacts = user.contacts
                creat_data = user.creat_data
                name = user.name
                birthday = user.birthday
                phone = user.phone

                data_dict['sex'] = sex
                data_dict['age'] = age
                data_dict['weigth'] = weigth
                data_dict['height'] = height
                data_dict['health'] = health
                data_dict['contacts'] = contacts
                data_dict['creat_data'] = creat_data
                data_dict['name'] = name
                data_dict['birthday'] = birthday
                data_dict['phone'] = phone

                return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'data': data_dict})
            except Exception as e:
                return http.JsonResponse({'code': RETCODE.NODATAERR, 'errmsg': '错误的token'})


class UserCollectView(View):
    """
    用户收藏的药品信息
    有BUG
    """

    def get(self, request):
        token = request.GET.get('token')
        if token is None:
            return http.JsonResponse({'code': RETCODE.PARAMERR, 'errmsg': '未传入token'})
        user = Users.objects.get(token=token)
        medical = user.medicine.all()
        data_dict = {}
        m = 1
        for n in medical:
            dict_in = {}
            dict_in['name'] = n.name
            dict_in['category'] = n.category
            dict_in['introduce'] = n.introduce
            dict_in['creat_data'] = n.creat_data
            dict_in['suit'] = n.suit
            dict_in['bad'] = n.bad
            dict_in['life'] = n.life
            dict_in['use'] = n.use
            dict_in['taboo'] = n.taboo
            dict_in['heed'] = n.heed
            dict_in['savemethod'] = n.savemethod
            dict_in['medicalkit'] = n.medicalkit

            data_dict[m] = dict_in
            m += 1

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'data': data_dict})


class PeopleliveView(View):
    def put(self, request):
        data = json.loads(request.body.decode())

        token = data.get('token')
        condition = data.get('condition')
        if not token:
            return http.JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '未传入token'})
        else:
            try:
                user = Users.objects.get(token=token)
            except Exception as e:
                return http.JsonResponse({'code': RETCODE.USERERR, 'errmsg': '不存在此用户'})
            if condition == 'login':
                user.live = 1
                user.save()
                return http.JsonResponse({'code': RETCODE.OK, 'errmsg': user.name + '登录成功'})
            elif condition == 'exit':
                user.live = 0
                user.save()
                return http.JsonResponse({'code': RETCODE.OK, 'errmsg': user.name + '登出成功'})
            else:
                return http.JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '未传入condition'})

    def get(self, request):
        token = request.GET.get('token')
        if not token:
            return http.JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '未传入token'})
        else:
            try:
                users = Users.objects.filter(live=1)
            except Exception as e:
                return http.JsonResponse({'code': RETCODE.USERERR, 'errmsg': '暂无登录用户'})

            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'data': len(users)})


class ChinaMap(object):
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
        geo.render("map.html")


class ChinaView(View):
    def get(self, request):
        # a = ChinaMap()
        # a.main()
        return render(request, 'map.html')

