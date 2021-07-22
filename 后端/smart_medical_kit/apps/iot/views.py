from django.shortcuts import render

# Create your views here.
from django.views import View


class ShowIOTs(View):
    def get(self, request):
        pass


class KTView(View):
    def get(self, request):
        return render(request, 'kt.html')
