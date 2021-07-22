import json
import logging

import jwt
import requests
from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View
# from ..user.models import Users
from apps.user.models import Users
from utils.response_code import RETCODE

logger = logging.getLogger('django')


class GetToken(object):
    """
    测试代码在test2.py中
    """
    def __init__(self, code):
        self.url = 'https://api.weixin.qq.com/sns/jscode2session'
        self.app_id = 'wxc10b4a6db7c76cfc'
        self.app_secret = 'f811dca34840dfcb3b85af17fb2c60f5'
        self.code = code

    def get_openid(self):
        url = self.url + "?appid=" + self.app_id + "&secret=" + self.app_secret + "&js_code=" + self.code + "&grant_type=authorization_code"
        res = requests.get(url)
        try:
            # 文档说unionid可以不用，就先对openid和session_key进行JWT加密生成token
            openid = res.json()['openid']  # 用户唯一标识
            session_key = res.json()['session_key']  # 会话密钥
            unionid = res.json()['unionid']  # 用户在开放平台的唯一标识符，在满足 UnionID 下发条件的情况下会返回，详见 UnionID 机制说明。

            token_dict = {
                'openid': openid,
                'session_key': session_key
            }
            headers = {
                'alg': "HS256",  # 声明所使用的算法
            }
            jwt_token = jwt.encode(token_dict,  # payload, 有效载体
                                   "zhananbudanchou9527269",  # 进行加密签名的密钥
                                   algorithm="HS256",  # 指明签名算法方式, 默认也是HS256
                                   headers=headers  # json web token 数据结构包含两部分, payload(有效载体), headers(标头)
                                   ).decode('utf-8')  # python3 编码后得到 bytes, 再进行解码(指明解码的格式), 得到一个str
            return jwt_token
        except KeyError as key:
            # return 'fail'
            logger.error(key)
            return 'fail'


# class CreateUser(View):
#     def get(self, request, token):
#         """创建用户"""
#         # token = request.GET.get('token')
#         name = request.GET.get('name')
#         sex = request.GET.get('sex')
#         age = request.GET.get('age')
#         weight = request.GET.get('weight')
#         height = request.GET.get('height')
#         health = request.GET.get('health')
#         contacts = request.GET.get('contacts')
#         try:
#             Users.objects.create(
#                 token=token,
#                 name=name,
#                 sex=sex,
#                 age=age,
#                 weight=weight,
#                 height=height,
#                 health=health,
#                 contacts=contacts,
#             )
#         except Exception as e:
#             logger.error(e)
#             return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '数据库操作错误'})
#         return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})
#
#     def put(self, request, token):
#         """
#         修改用户信息
#         要JSON格式在请求体中
#         """
#         data = json.loads(request.body.decode('utf-8'))
#         name = data.get('name')
#         sex = data.get('sex')
#         age = data.get('age')
#         weight = data.get('weight')
#         height = data.get('height')
#         health = data.get('health')
#         contacts = data.get('contacts')
#
#         try:
#             Users.objects.filter(token=token).update(
#                 name=name,
#                 sex=sex,
#                 age=age,
#                 weight=weight,
#                 height=height,
#                 health=health,
#                 contacts=contacts
#             )
#             return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '修改成功'})
#         except Exception as e:
#             logger.error(e)
#             return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '数据库错误'})


class Create_or_LoginView(View):
    """创建或者登录用户"""

    def get(self, request):
        """
        """
        # data = json.loads(request.body.decode('utf-8'))
        data = request.GET
        code = data.get('code')
        token = data.get('token')
        name = data.get('name')
        sex = data.get('sex')
        age = data.get('age')
        weight = data.get('weight')
        height = data.get('height')
        health = data.get('health')
        contacts = data.get('contacts')
        if not token:
            # 如果没有传token的话，就是创建用户
            # token = GetToken(code).get_openid()
            token = '1840707266'
            try:
                Users.objects.create(
                    token=token,
                    name=name,
                    sex=sex,
                    age=age,
                    weight=weight,
                    height=height,
                    health=health,
                    contacts=contacts,
                )
                return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '创建成功'})
            except Exception as e:
                logger.error(e)
                return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '该用户已存在'})

        else:
            # 如果传了token，则验证是否有这个用户(传入值为token和code，通过code获取token，进行比对验证)  这下面的逻辑写错了，要重写
            try:
                # 有这个用户，返回登录成功信息
                user = Users.objects.get(token=token)
                return http.JsonResponse({'code': RETCODE.OK, 'token': token, 'errmsg': '登录成功'})


            except:
                # 没有这个用户，返回登录失败信息
                return http.JsonResponse({'code': RETCODE.USERERR, 'token': token, 'errmsg': '登录失败'})

    def put(self, request):
        """
        修改用户信息
        要JSON格式在请求体中
        """
        data = json.loads(request.body.decode('utf-8'))
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


class ShowUserMessage(View):
    """展示用户信息"""

    def get(self, request, token):
        try:
            user = Users.objects.get(token=token)
            name = user.name  # 姓名
            sex = user.sex  # 性别(0:man, 1woman)
            age = user.age  # 年龄
            weight = user.weight  # 体重
            height = user.height  # 身高
            health = user.health  # 健康状况
            contacts = user.contacts  # 紧急联系人
            message_dict = {
                'name': name,
                'sex': sex,
                'age': age,
                'weight': weight,
                'height': height,
                'health': health,
                'contacts': contacts,
            }
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'message': message_dict})

        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.USERERR, 'errmsg': '没有该用户'})
