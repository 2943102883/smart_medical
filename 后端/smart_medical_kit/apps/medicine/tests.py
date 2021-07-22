from django.test import TestCase

# Create your tests here.
import threading
from time import ctime, sleep


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



def add(a, b):
    # print ('a+b:', a+b)
    return a + b

t3 = MyThread(add, args=(1, 2,))
t3.start()

print(t3.get_result())

