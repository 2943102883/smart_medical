import json
import logging
import threading

import requests
from django.core.files.base import ContentFile
from django.forms import model_to_dict
from lxml import etree
from datetime import datetime
import re

from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.medicine.models import Medicine_user, Medical_loads, Medicals
from apps.user.models import Users
from utils.response_code import RETCODE

logger = logging.getLogger('django')


class CreateMedical(View):
    """新增药品、修改药品信息
    阿司匹林
    """

    def get(self, request, name, token, num):
        """新增药品"""
        category = request.GET.get('category')
        introduce = request.GET.get('introduce')
        suit = request.GET.get('suit')
        bad = request.GET.get('bad')
        life = request.GET.get('life')
        use = request.GET.get('use')
        taboo = request.GET.get('taboo')
        heed = request.GET.get('heed')
        savemethod = request.GET.get('savemethod')

        try:
            usertem = Users.objects.get(token=token)
            medtem = Medicine_user.objects.get(user=usertem, name=name)
            # medtem = Medicine_user.objects.get(user=usertem)
            if medtem:
                return http.JsonResponse({'code': RETCODE.USERERR, 'errmsg': '已存在同名药品'})
        except:
            try:

                user = Users.objects.get(token=token)
                Medicine_user.objects.create(
                    name=name,
                    category=category,
                    introduce=introduce,
                    suit=suit,
                    bad=bad,
                    life=life,
                    use=use,
                    taboo=taboo,
                    heed=heed,
                    savemethod=savemethod,
                    medicalkit=num,
                    user=user,
                )
            except Exception as e:
                logger.error(e)
                return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '数据库问题'})

            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})

    def put(self, request, name, token, num):
        """
        修改药品
            如果传了newname，那么就是可以修改药品名
            如果newname传了0，那么就是不改变药品名，而是修改其他信息
        """
        data = json.loads(request.body.decode())
        newname = data.get('newname')
        category = data.get('category')
        introduce = data.get('introduce')
        suit = data.get('suit')
        bad = data.get('bad')
        life = data.get('life')
        use = data.get('use')
        taboo = data.get('taboo')
        heed = data.get('heed')
        savemethod = data.get('savemethod')
        newnum = data.get('newnum')
        if newnum is None:
            newnum = num
        else:
            newnum = newnum
        # newname为必传参数，如果newname为0，则说明不改名字
        if newname == "0":
            newname = name
        elif newname == 0:
            newname = name
        elif newname is None:
            return http.JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '缺少新药的名字'})

        try:
            user = Users.objects.get(token=token)
            Medicine_user.objects.filter(user=user, name=name).update(
                name=newname,
                category=category,
                introduce=introduce,
                suit=suit,
                bad=bad,
                life=life,
                use=use,
                taboo=taboo,
                heed=heed,
                medicalkit=newnum,
                savemethod=savemethod,
            )
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '数据库问题'})

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})


class ShowUserMedical(View):
    """展示用户药品"""

    def get(self, request, token):
        user = Users.objects.get(token=token)
        medicines = Medicine_user.objects.filter(user=user)
        medicines_list = []
        numbers = []  # 数字

        # 这里列表转字典需要两个列表的合并
        for m in medicines:
            medicines_list_in = []  # 循环内临时的元祖
            medicines_dict_in = {}  # 循环内临时的字典
            medicines_dict_in['name'] = m.name
            medicines_dict_in['category'] = m.category
            medicines_dict_in['introduce'] = m.introduce
            medicines_dict_in['suit'] = m.suit
            medicines_dict_in['bad'] = m.bad
            medicines_dict_in['life'] = m.life
            medicines_dict_in['use'] = m.use
            medicines_dict_in['taboo'] = m.taboo
            medicines_dict_in['heed'] = m.heed
            medicines_dict_in['savemethod'] = m.savemethod
            medicines_dict_in['num'] = m.medicalkit
            medicines_list_in.append(medicines_dict_in)
            medicines_list.append(medicines_list_in)
        num = len(medicines_list)
        for n in range(num):
            numbers.append(n)
        medicines_dict = dict(zip(numbers, medicines_list))  # 字典格式返回
        jsons = json.dumps(medicines_dict, ensure_ascii=False)  # json格式返回
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'data': medicines_dict})


class SearchMedicine:
    def __init__(self, name):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'cookie': '__finger=8c6cf3c4db94a8d5b1ea65208b7a06eb; Hm_lvt_f46dd4cc550b93aefde9b00265bb533d=1616479087; UM_distinctid=1785da96b84b0d-0b10b9c44101e6-5771031-1fa400-1785da96b85be5; CNZZDATA899409=cnzz_eid%3D1562633242-1616475837-https%253A%252F%252Fwww.sogou.com%252F%26ntime%3D1616475837; Hm_lvt_efd3be6e24f6aa90edbcdea9b260aac6=1616479088; CNZZDATA953100=cnzz_eid%3D1999569600-1616478788-https%253A%252F%252Fwww.sogou.com%252F%26ntime%3D1616478788; __asc=51716daf1785da96fd25a0658ef; __auc=51716daf1785da96fd25a0658ef; Hm_lpvt_f46dd4cc550b93aefde9b00265bb533d=1616479172; Hm_lpvt_efd3be6e24f6aa90edbcdea9b260aac6=1616479172'
        }
        self.base_url = url = 'https://ypk.familydoctor.com.cn/search/so/?KeyWord={}'
        self.name = name

    # 请求网页
    def connect_url(self, url):
        response = requests.get(url, headers=self.headers)
        text = response.content.decode('utf-8')
        html = etree.HTML(text)
        return html

    # 返回具体信息的网址
    def msgurl(self, url):
        html = self.connect_url(url)
        msg_url = html.xpath('//div[@class="search-result"]//dl[1]/dd/h4/a/@href')[0].strip()
        return ''.join([msg_url, 'instructions/'])

    def messages(self, url):
        # url = https://ypk.familydoctor.com.cn/265257/instructions/
        html = self.connect_url(url)
        data_dict = {}
        # xpath
        try:
            # name = html.xpath('//table[@class="table-1"]//tr[1]/td/text()')[0].strip()  # 药品名
            name = html.xpath('//tr/th[contains(text(),"名称")]/../td/text()')[0].strip()  # 药品名
            data_dict['name'] = name
        except:
            data_dict['name'] = 'null'
        #################################################################################################
        try:
            # suit = html.xpath('//table[@class="table-1"]//tr[2]/td//text()')  # 适应症状
            suit = html.xpath('//tr/th[contains(text(),"适 ")]/../td//text()')  # 适应症状
            suits = []
            for b in suit:
                suits.append(b)
            data_dict['suit'] = suits
        except:
            data_dict['suit'] = 'null'
        #################################################################################################
        try:
            # usemethod = html.xpath('//table[@class="table-1"]//tr[3]/td/p')  # 使用方法
            # for i in usemethod:
            #     usemethod = " ".join(i.xpath('text()'))
            usemethod = html.xpath('//tr/th[contains(text(),"用量")]/../td//text()')  # 使用方法
            usemethods = []
            for b in usemethod:
                usemethods.append(b)

            data_dict['usemethod'] = usemethods
        except:
            data_dict['usemethod'] = 'null'
        #################################################################################################
        try:
            # lelment = html.xpath('//table[@class="table-1"]//tr[4]/td/text()')[0].strip()  # 成分
            lelment = html.xpath('//tr/th[contains(text(),"份")]/../td/text()')[0].strip()  # 成分
            data_dict['lelment'] = lelment
        except:
            data_dict['lelment'] = 'null'
        #################################################################################################
        try:
            # bad = html.xpath('//table[@class="table-1"]//tr[6]/td/p/text()')  # 不良反应
            bad = html.xpath('//tr/th[contains(text(),"不良")]/../td//text()')  # 不良反应
            bads = []
            for b in bad:
                bads.append(b)
            data_dict['bad'] = bads
        except:
            data_dict['bad'] = 'null'
        #################################################################################################
        try:
            # err = html.xpath('//table[@class="table-1"]//tr[7]/td//text()')  # 禁忌
            err = html.xpath('//tr/th[contains(text(),"禁")]/../td//text()')  # 禁忌
            errs = []
            for e in err:
                errs.append(e)
            data_dict['err'] = errs
        except:
            data_dict['err'] = 'null'
        #################################################################################################
        try:
            # heed = html.xpath('//table[@class="table-1"]//tr[8]/td/p/text()')  # 注意事项
            heed = html.xpath('//tr/th[contains(text(),"注意事")]/../td//text()')  # 注意事项
            # for i in heed:
            #     heed = " ".join(i.xpath('text()'))
            heeds = []
            for e in heed:
                heeds.append(e)
            data_dict['heed'] = heeds
        except:
            data_dict['heed'] = 'null'
        #################################################################################################
        try:
            # savemethod = html.xpath('//table[@class="table-1"]//tr[11]/td/text()')[0].strip()  # 保存方法
            savemethod = html.xpath('//tr/th[contains(text(),"贮")]/../td//text()')[0].strip()  # 保存方法
            data_dict['savemethod'] = savemethod
        except:
            data_dict['savemethod'] = 'null'
        #################################################################################################
        return data_dict

    def data(self):
        url = self.base_url.format(self.name)
        msg_url = self.msgurl(url)
        data_dict = self.messages(msg_url)
        return data_dict


class SearchMedicine2:
    def __init__(self, name):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'cookie': '__finger=8c6cf3c4db94a8d5b1ea65208b7a06eb; Hm_lvt_f46dd4cc550b93aefde9b00265bb533d=1616479087; UM_distinctid=1785da96b84b0d-0b10b9c44101e6-5771031-1fa400-1785da96b85be5; CNZZDATA899409=cnzz_eid%3D1562633242-1616475837-https%253A%252F%252Fwww.sogou.com%252F%26ntime%3D1616475837; Hm_lvt_efd3be6e24f6aa90edbcdea9b260aac6=1616479088; CNZZDATA953100=cnzz_eid%3D1999569600-1616478788-https%253A%252F%252Fwww.sogou.com%252F%26ntime%3D1616478788; __asc=51716daf1785da96fd25a0658ef; __auc=51716daf1785da96fd25a0658ef; Hm_lpvt_f46dd4cc550b93aefde9b00265bb533d=1616479172; Hm_lpvt_efd3be6e24f6aa90edbcdea9b260aac6=1616479172'
        }
        self.base_url = url = 'https://ypk.familydoctor.com.cn/search/so/?KeyWord={}'
        self.name = name

    # 请求网页
    def connect_url(self, url):
        response = requests.get(url, headers=self.headers)
        text = response.content.decode('utf-8')
        html = etree.HTML(text)
        return html

    # 返回具体信息的网址
    def msgurl(self, url, num):
        html = self.connect_url(url)
        msg_url = html.xpath('//div[@class="search-result"]//dl[{}]/dd/h4/a/@href'.format(num))[0].strip()
        return ''.join([msg_url, 'instructions/'])

    # 传入网址，返回具体信息
    def messages(self, url):
        # url = https://ypk.familydoctor.com.cn/265257/instructions/
        html = self.connect_url(url)
        data_dict = {}
        # xpath
        try:
            # name = html.xpath('//table[@class="table-1"]//tr[1]/td/text()')[0].strip()  # 药品名
            name = html.xpath('//tr/th[contains(text(),"名称")]/../td/text()')[0].strip()  # 药品名
            data_dict['name'] = name
        except:
            data_dict['name'] = ''
        #################################################################################################
        try:
            # suit = html.xpath('//table[@class="table-1"]//tr[2]/td//text()')  # 适应症状
            suit = html.xpath('//tr/th[contains(text(),"适 ")]/../td//text()')  # 适应症状
            suits = []
            for b in suit:
                suits.append(b)
            data_dict['suit'] = suits
        except:
            data_dict['suit'] = ''
        #################################################################################################
        try:
            # usemethod = html.xpath('//table[@class="table-1"]//tr[3]/td/p')  # 使用方法
            # for i in usemethod:
            #     usemethod = " ".join(i.xpath('text()'))
            usemethod = html.xpath('//tr/th[contains(text(),"用量")]/../td//text()')  # 使用方法
            usemethods = []
            for b in usemethod:
                usemethods.append(b)

            data_dict['usemethod'] = usemethods
        except:
            data_dict['usemethod'] = ''
        #################################################################################################
        try:
            # lelment = html.xpath('//table[@class="table-1"]//tr[4]/td/text()')[0].strip()  # 成分
            lelment = html.xpath('//tr/th[contains(text(),"份")]/../td/text()')[0].strip()  # 成分
            data_dict['lelment'] = lelment
        except:
            data_dict['lelment'] = ''
        #################################################################################################
        try:
            # bad = html.xpath('//table[@class="table-1"]//tr[6]/td/p/text()')  # 不良反应
            bad = html.xpath('//tr/th[contains(text(),"不良")]/../td//text()')  # 不良反应
            bads = []
            for b in bad:
                bads.append(b)
            data_dict['bad'] = bads
        except:
            data_dict['bad'] = ''
        #################################################################################################
        try:
            # err = html.xpath('//table[@class="table-1"]//tr[7]/td//text()')  # 禁忌
            err = html.xpath('//tr/th[contains(text(),"禁")]/../td//text()')  # 禁忌
            errs = []
            for e in err:
                errs.append(e)
            data_dict['err'] = errs
        except:
            data_dict['err'] = ''
        #################################################################################################
        try:
            # heed = html.xpath('//table[@class="table-1"]//tr[8]/td/p/text()')  # 注意事项
            heed = html.xpath('//tr/th[contains(text(),"注意事")]/../td//text()')  # 注意事项
            # for i in heed:
            #     heed = " ".join(i.xpath('text()'))
            heeds = []
            for e in heed:
                heeds.append(e)
            data_dict['heed'] = heeds
        except:
            data_dict['heed'] = ''
        #################################################################################################
        try:
            # savemethod = html.xpath('//table[@class="table-1"]//tr[11]/td/text()')[0].strip()  # 保存方法
            savemethod = html.xpath('//tr/th[contains(text(),"贮")]/../td//text()')[0].strip()  # 保存方法
            data_dict['savemethod'] = savemethod
        except:
            data_dict['savemethod'] = ''
        #################################################################################################
        return data_dict

    # 传入网址，返回结果列表
    def list(self, url, num):
        # https://ypk.familydoctor.com.cn/search/so/?KeyWord=阿莫西林
        html = self.connect_url(url)
        data_dict = {}
        # imgs = '{}.img'.format(num)
        # names = '{}.name'.format(num)
        img = html.xpath('//div[@class="search-result"]//dl[{}]//img/@src'.format(num))[0].strip()
        name = html.xpath('//div[@class="search-result"]//dl[{}]//dd//h4//text()'.format(num))[0].strip()
        # data_dict['{}.img'.format(num)] = img
        # data_dict['{}.name'.format(num)] = name
        data_dict['img'] = img
        data_dict['name'] = name

        return data_dict

    def data(self):
        dict = {}
        for i in range(20):
            url = self.base_url.format(self.name)
            msg_url = self.msgurl(url, i + 1)
            msg_dict = self.messages(msg_url)
            show_dict = self.list(url, i + 1)

            # tem_dict = {}
            # tem_dict['show'] = show_dict
            # tem_dict['msg'] = msg_dict
            # dict[i + 1] = tem_dict

            msg_dict['img_url'] = show_dict['img']
            # dict[i + 1] = msg_dict
            dict[i] = msg_dict

        return dict


class SearchMedicine3:
    def __init__(self, name, num):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'cookie': '__finger=8c6cf3c4db94a8d5b1ea65208b7a06eb; Hm_lvt_f46dd4cc550b93aefde9b00265bb533d=1616479087; UM_distinctid=1785da96b84b0d-0b10b9c44101e6-5771031-1fa400-1785da96b85be5; CNZZDATA899409=cnzz_eid%3D1562633242-1616475837-https%253A%252F%252Fwww.sogou.com%252F%26ntime%3D1616475837; Hm_lvt_efd3be6e24f6aa90edbcdea9b260aac6=1616479088; CNZZDATA953100=cnzz_eid%3D1999569600-1616478788-https%253A%252F%252Fwww.sogou.com%252F%26ntime%3D1616478788; __asc=51716daf1785da96fd25a0658ef; __auc=51716daf1785da96fd25a0658ef; Hm_lpvt_f46dd4cc550b93aefde9b00265bb533d=1616479172; Hm_lpvt_efd3be6e24f6aa90edbcdea9b260aac6=1616479172'
        }
        self.base_url = url = 'https://ypk.familydoctor.com.cn/search/so/?KeyWord={}'
        self.name = name
        self.num = num

    # 请求网页
    def connect_url(self, url):
        response = requests.get(url, headers=self.headers)
        text = response.content.decode('utf-8')
        html = etree.HTML(text)
        return html

    # 返回具体信息的网址
    def msgurl(self, url, num):
        html = self.connect_url(url)
        msg_url = html.xpath('//div[@class="search-result"]//dl[{}]/dd/h4/a/@href'.format(num))[0].strip()
        return ''.join([msg_url, 'instructions/'])

    # 传入网址，返回具体信息
    def messages(self, url):
        # url = https://ypk.familydoctor.com.cn/265257/instructions/
        html = self.connect_url(url)
        data_dict = {}
        # xpath
        try:
            # name = html.xpath('//table[@class="table-1"]//tr[1]/td/text()')[0].strip()  # 药品名
            name = html.xpath('//tr/th[contains(text(),"名称")]/../td/text()')[0].strip()  # 药品名
            data_dict['name'] = name
        except:
            data_dict['name'] = ''
        #################################################################################################
        try:
            # suit = html.xpath('//table[@class="table-1"]//tr[2]/td//text()')  # 适应症状
            suit = html.xpath('//tr/th[contains(text(),"适 ")]/../td//text()')  # 适应症状
            suits = []
            for b in suit:
                suits.append(b)
            data_dict['suit'] = suits
        except:
            data_dict['suit'] = ''
        #################################################################################################
        try:
            # usemethod = html.xpath('//table[@class="table-1"]//tr[3]/td/p')  # 使用方法
            # for i in usemethod:
            #     usemethod = " ".join(i.xpath('text()'))
            usemethod = html.xpath('//tr/th[contains(text(),"用量")]/../td//text()')  # 使用方法
            usemethods = []
            for b in usemethod:
                usemethods.append(b)

            data_dict['usemethod'] = usemethods
        except:
            data_dict['usemethod'] = ''
        #################################################################################################
        try:
            # lelment = html.xpath('//table[@class="table-1"]//tr[4]/td/text()')[0].strip()  # 成分
            lelment = html.xpath('//tr/th[contains(text(),"份")]/../td/text()')[0].strip()  # 成分
            data_dict['lelment'] = lelment
        except:
            data_dict['lelment'] = ''
        #################################################################################################
        try:
            # bad = html.xpath('//table[@class="table-1"]//tr[6]/td/p/text()')  # 不良反应
            bad = html.xpath('//tr/th[contains(text(),"不良")]/../td//text()')  # 不良反应
            bads = []
            for b in bad:
                bads.append(b)
            data_dict['bad'] = bads
        except:
            data_dict['bad'] = ''
        #################################################################################################
        try:
            # err = html.xpath('//table[@class="table-1"]//tr[7]/td//text()')  # 禁忌
            err = html.xpath('//tr/th[contains(text(),"禁")]/../td//text()')  # 禁忌
            errs = []
            for e in err:
                errs.append(e)
            data_dict['err'] = errs
        except:
            data_dict['err'] = ''
        #################################################################################################
        try:
            # heed = html.xpath('//table[@class="table-1"]//tr[8]/td/p/text()')  # 注意事项
            heed = html.xpath('//tr/th[contains(text(),"注意事")]/../td//text()')  # 注意事项
            # for i in heed:
            #     heed = " ".join(i.xpath('text()'))
            heeds = []
            for e in heed:
                heeds.append(e)
            data_dict['heed'] = heeds
        except:
            data_dict['heed'] = ''
        #################################################################################################
        try:
            # savemethod = html.xpath('//table[@class="table-1"]//tr[11]/td/text()')[0].strip()  # 保存方法
            savemethod = html.xpath('//tr/th[contains(text(),"贮")]/../td//text()')[0].strip()  # 保存方法
            data_dict['savemethod'] = savemethod
        except:
            data_dict['savemethod'] = ''
        #################################################################################################
        return data_dict

    # 传入网址，返回结果列表
    def list(self, url, num):
        # https://ypk.familydoctor.com.cn/search/so/?KeyWord=阿莫西林
        html = self.connect_url(url)
        data_dict = {}
        img = html.xpath('//div[@class="search-result"]//dl[{}]//img/@src'.format(num))[0].strip()
        name = html.xpath('//div[@class="search-result"]//dl[{}]//dd//h4//text()'.format(num))[0].strip()
        data_dict['img'] = img
        data_dict['name'] = name

        return data_dict

    def data(self):
        dict = {}
        url = self.base_url.format(self.name)
        i = int(self.num) - 1
        msg_url = self.msgurl(url, i + 1)
        msg_dict = self.messages(msg_url)
        show_dict = self.list(url, i + 1)

        msg_dict['img_url'] = show_dict['img']

        # 为了格式统一，这个废弃
        # tem_dict = {}
        # tem_dict['show'] = show_dict
        # tem_dict['msg'] = msg_dict
        # dict[i + 1] = tem_dict
        dict[i + 1] = msg_dict
        # return dict
        return dict


# 多线程如何返回值
class MyThread(threading.Thread):

    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


def search2(name):
    search = SearchMedicine2(name)
    data = search.data()
    return data


class SearchMedicineView(View):
    """
    传入num，搜索第几条消息（单条查询）
    """

    def get(self, request, name):
        num = request.GET.get('num')
        search = SearchMedicine3(name, num)
        try:
            data = search.data()

        except Exception as e:
            return http.JsonResponse({'code': RETCODE.NODATAERR, 'errmsg': '缺少参数'})

        return http.JsonResponse({'code': RETCODE.OK, 'data': data})


class SearchMedicineView2(View):
    """
    直接返回20条消息，多条查询
    """

    def get(self, request, name):
        search = SearchMedicine2(name)
        # data = search.data()
        try:
            data = search.data()
        except Exception as e:
            return http.JsonResponse({'code': RETCODE.NODATAERR})
        return http.JsonResponse({'code': RETCODE.OK, 'data': data})


class SearchMedicineView3(View):
    """
    查询并保存单个药品
    查询药品并存储到数据库中
    需传入num来确定保存那个数据
    """

    def get(self, request, name):
        num = request.GET.get('num')
        search = SearchMedicine3(name, num)
        try:
            data = search.data()
            num = int(num)
            # name_in = data[num]['show']['name']
            # img = data[num]['show']['img']
            # suit = data[num]['msg']['suit']
            # usemethod = data[num]['msg']['usemethod']
            # lelment = data[num]['msg']['lelment']
            # bad = data[num]['msg']['bad']
            # err = data[num]['msg']['err']
            # heed = data[num]['msg']['heed']
            # savemethod = data[num]['msg']['savemethod']
            name_in = data[num]['name']
            img = data[num]['img_url']
            suit = data[num]['suit']
            usemethod = data[num]['usemethod']
            lelment = data[num]['lelment']
            bad = data[num]['bad']
            err = data[num]['err']
            heed = data[num]['heed']
            savemethod = data[num]['savemethod']
        except Exception  as e:
            return http.JsonResponse({'code': RETCODE.NODATAERR})

        try:
            a = Medicals.objects.get(name='阿莫西林')
            Medical_loads.objects.create(
                img_url=img,
                suit=suit,
                usemethod=usemethod,
                lelment=lelment,
                bad=bad,
                err=err,
                heed=heed,
                savemethod=savemethod,
                num=num,
                medical=a
            )
        except Exception as e:
            return http.JsonResponse({'code': RETCODE.DBERR, 'msg': '数据库存储错误'})
        return http.JsonResponse({'code': RETCODE.OK, 'data': data})


class SearchMedicineView4(View):
    """
    查询药品并存储到数据库中
    这个是3的改进，增加循环20次的功能
    test:1已在数据库里了，无须存储。data=null
        2不在数据库里，刚刚存完    data={......}
    """

    def get(self, request, name):
        t = MyThread(search2, args=(name,))
        t.start()  ##启动线程
        # 判断是否有这个药品
        try:
            # 有这个药品，则保存20条数据到数据库
            a = Medicals.objects.get(name=name)
        except:
            # 没有这个药品则创建药品
            Medicals.objects.create(
                name=name
            )
            a = Medicals.objects.get(name=name)

        # 判断是否已经存储过数据了
        try:
            # 随便查一条数据，如果不报错，则说明里面有数据
            # Medical_loads.objects.filter(medical=a, num=18)
            Medical_loads.objects.get(medical=a, num=18)
            b = 1
        except:
            # 如果报错了，则说明里面没有数据
            b = 0
        if b == 1:
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '请勿重复存储', 'data': t.get_result(), 'test': 1})
        elif b == 0:
            try:
                for num in range(20):
                    num += 1
                    search = SearchMedicine3(name, num)
                    data = search.data()
                    num = int(num)
                    # name_in = data[num]['show']['name']
                    # img = data[num]['show']['img']
                    # suit = data[num]['msg']['suit']
                    # usemethod = data[num]['msg']['usemethod']
                    # lelment = data[num]['msg']['lelment']
                    # bad = data[num]['msg']['bad']
                    # err = data[num]['msg']['err']
                    # heed = data[num]['msg']['heed']
                    # savemethod = data[num]['msg']['savemethod']
                    name_in = data[num]['name']
                    img = data[num]['img_url']
                    suit = data[num]['suit']
                    usemethod = data[num]['usemethod']
                    lelment = data[num]['lelment']
                    bad = data[num]['bad']
                    err = data[num]['err']
                    heed = data[num]['heed']
                    savemethod = data[num]['savemethod']
                    a = Medicals.objects.get(name=name)
                    Medical_loads.objects.create(
                        img_url=img,
                        suit=suit,
                        usemethod=usemethod,
                        lelment=lelment,
                        bad=bad,
                        err=err,
                        heed=heed,
                        savemethod=savemethod,
                        num=num,
                        name=name_in,
                        medical=a
                    )
            except Exception as e:
                return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': 'search4查询出错'})
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '已存储到数据库', 'data': t.get_result(), 'test': 0})
        else:
            pass


class ShowMedical(View):
    """
    展示爬虫爬下来存到数据库中的数据
    Anny1111125
    """

    def get(self, request, name):
        try:
            n = Medicals.objects.get(name=name)
            medicals = n.medical.all()
            data = json.loads(json.dumps(list(medicals.values())))
        except Exception as e:
            return http.JsonResponse({'code': RETCODE.NODATAERR, 'errmsg': '药品不在数据库中'})
        return http.JsonResponse({'data': data})


class ShowMedical2(View):
    def get(self, request, name):
        try:
            # 随便查一条数据，如果不报错，则说明里面有数据
            a = Medicals.objects.get(name=name)
            Medical_loads.objects.get(medical=a, num=18)
            m = 1
        except:
            # 如果报错了，则说明数据库中没有这个药品，需要爬取到数据库中
            m = 0

        if m == 0:
            # 爬取数据到数据库中
            t = MyThread(search2, args=(name,))
            t.start()  ##启动线程
            # 判断是否有这个药品
            try:
                # 有这个药品，则保存20条数据到数据库
                a = Medicals.objects.get(name=name)
            except:
                # 没有这个药品则创建药品
                Medicals.objects.create(
                    name=name
                )
                a = Medicals.objects.get(name=name)

            # 判断是否已经存储过数据了
            try:
                # 随便查一条数据，如果不报错，则说明里面有数据
                Medical_loads.objects.get(medical=a, id=18)
                b = 1
            except:
                # 如果报错了，则说明里面没有数据
                b = 0
            if b == 1:
                return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '请勿重复存储'})
            else:
                try:
                    for num in range(20):
                        num += 1
                        search = SearchMedicine3(name, num)
                        data = search.data()
                        num = int(num)
                        name_in = data[num]['name']
                        img = data[num]['img_url']
                        suit = data[num]['suit']
                        usemethod = data[num]['usemethod']
                        lelment = data[num]['lelment']
                        bad = data[num]['bad']
                        err = data[num]['err']
                        heed = data[num]['heed']
                        savemethod = data[num]['savemethod']
                        a = Medicals.objects.get(name=name)
                        Medical_loads.objects.create(
                            img_url=img,
                            suit=suit,
                            usemethod=usemethod,
                            lelment=lelment,
                            bad=bad,
                            err=err,
                            heed=heed,
                            savemethod=savemethod,
                            num=num,
                            name=name_in,
                            medical=a
                        )
                except Exception as e:
                    return http.JsonResponse({'code': 'err'})
                return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '已存储到数据库', 'data': t.get_result()})
        elif m == 1:
            # 从数据库中查询出药品信息
            try:
                n = Medicals.objects.get(name=name)
                medicals = n.medical.all()
                data = json.loads(json.dumps(list(medicals.values())))
            except Exception as e:
                return http.JsonResponse({'code': RETCODE.NODATAERR, 'errmsg': '药品不在数据库中'})
            return http.JsonResponse({'data': data})
        else:
            pass


class DeleteMedicineView(View):
    """"删除用户药品"""

    def get(self, request, name, token):
        user = Users.objects.get(token=token)
        medicines = Medicine_user.objects.filter(user=user, name=name)
        if not medicines:
            return http.JsonResponse({'code': RETCODE.NODATAERR, 'errmsg': '没有此药品'})
        else:
            medicines.delete()
            return http.JsonResponse({'code': 'ok'})


class ShowTime(View):
    """
    计算过期时间
    """

    def get(self, request, token):
        try:
            user = Users.objects.get(token=token)
            medical = Medicine_user.objects.filter(user=user)
            data_time = {}
            for n in range(len(medical)):
                data_time_in = {}  # 存储本次循环的结果
                # 循环看有该用户下有多少药品
                life = medical[n].life
                create_time = medical[n].creat_data  # datetime.date
                now_time = datetime.date(datetime.now())  # datetime.datetime-->datetime.date
                # time = now_time - create_time  # 已经在药箱里存多久了(datetime)
                time = create_time - now_time  # 已经在药箱里存多久了(datetime)
                live_time = time.days  # 已经在药箱里存多久了(int)
                """
                                live_time = 2   在药箱多少天了
                                life = 5        保质期是几天
                                life - live_time
                                    =0  今天过期
                                    >0  还有life天过期
                                    <0  已经过期life天了

                """
                a = life * 31 + live_time
                if a == 0:
                    pass
                    # data_time_in['msg'] = '今天过期'
                elif a > 0:
                    pass
                    # data_time_in['msg'] = '还有%d天过期' % a
                elif a < 0:
                    data_time_in['msg'] = '已经过期%d天了' % abs(a)
                    data_time_in['name'] = medical[n].name
                    data_time_in['data'] = a
                    data_time[n] = data_time_in
                else:
                    pass
                # data_time_in['name'] = medical[n].name
                # data_time_in['data'] = a
                # data_time[n] = data_time_in
            if len(data_time) == 0:
                return http.JsonResponse({'code': '1', 'errmsg': '没有过期的药品'})
            else:
                return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'data': data_time})


        except Exception as e:
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '该用户未存储药品'})


class ShowTime2(View):
    """
    计算过期时间
    """

    def get(self, request, token):
        try:
            user = Users.objects.get(token=token)
            medical = Medicine_user.objects.filter(user=user)
            data_time = {}
            for n in range(len(medical)):
                data_time_in = {}  # 存储本次循环的结果
                # 循环看有该用户下有多少药品
                life = medical[n].life
                create_time = medical[n].creat_data  # datetime.date
                now_time = datetime.date(datetime.now())  # datetime.datetime-->datetime.date
                time = now_time - create_time  # 已经在药箱里存多久了(datetime)
                live_time = time.days  # 已经在药箱里存多久了(int)
                """
                                live_time = 2   在药箱多少天了
                                life = 5        保质期是几天
                                life - live_time
                                    =0  今天过期
                                    >0  还有life天过期
                                    <0  已经过期life天了

                """
                a = life * 31 - live_time
                if a == 0:
                    data_time_in['msg'] = '今天过期'
                elif a > 0:
                    data_time_in['msg'] = '还有%d天过期' % a
                elif a < 0:
                    data_time_in['msg'] = '已经过期%d天了' % abs(a)
                else:
                    pass
                data_time_in['name'] = medical[n].name
                data_time_in['data'] = a
                data_time[n] = data_time_in
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'data': data_time})


        except Exception as e:
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '该用户未存储药品'})


class ImgageView(View):
    """
    test
    """

    def post(self, request):
        picture = request.FILES.get("picture", "")
        file_content = ContentFile(request.FILES['picture'].read())
        picture2 = request.FILES
        file = ContentFile(request.POST.get('picture'))
        data = json.loads(request.body.decode())

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})


class TranslateView(View):
    """
    药品收藏
    """
    def get(self, request):
        name = request.GET.get('name')
        num = request.GET.get('num')
        medical = Medicals.objects.get(name=name)
        medical_searched = Medical_loads.objects.get(num=num, medical=medical)
        medical_searched.translate = 1
        medical_searched.save()

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '收藏成功'})

    def post(self, request):
        medicals = Medical_loads.objects.filter(translate=1)
        data_dict = {}
        for n in range(len(medicals)):
            dict_in = {}
            dict_in['name'] = medicals[n].name
            dict_in['img_url'] = medicals[n].img_url
            dict_in['suit'] = medicals[n].suit
            dict_in['usemethod'] = medicals[n].usemethod
            dict_in['lelment'] = medicals[n].lelment
            dict_in['bad'] = medicals[n].bad
            dict_in['err'] = medicals[n].err
            dict_in['heed'] = medicals[n].heed
            dict_in['savemethod'] = medicals[n].savemethod
            data_dict[n] = dict_in

        return http.JsonResponse({'code': RETCODE.OK, 'data': data_dict})

