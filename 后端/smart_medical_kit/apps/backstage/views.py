from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.user.models import Users
from utils.response_code import RETCODE


class RegisterUser(View):
    """
    注册人数
    """
    def get(self, request):
        user = Users.objects.filter()
        num = len(user)
        return http.JsonResponse({'code': RETCODE.OK, 'num': num})


