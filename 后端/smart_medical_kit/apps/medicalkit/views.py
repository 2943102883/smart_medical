import json

from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.medicine.models import Medicine_self
from utils.response_code import RETCODE


class TestView(View):
    def get(self, request):
        response = http.JsonResponse({'code': 'ok'})
        # response['Access-Contro1-Allow-origin'] = "*"  # 设置请求头
        return response


class ShowSelfMedical(View):
    """展示程序自带药品"""
    def get(self, request):
        medicines = Medicine_self.objects.all()
        medicines_list = []
        numbers = []
        # 这里列表转字典需要两个列表的合并
        for m in medicines:
            medicines_list.append(m.name)
        num = len(medicines_list)
        for n in range(num):
            numbers.append(n)
        medicines_dict = dict(zip(numbers, medicines_list))  # 字典格式返回
        jsons = json.dumps(medicines_dict, ensure_ascii=False)  # json格式返回
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'data': medicines_dict})
