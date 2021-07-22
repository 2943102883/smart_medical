from django.db import models


# Create your models here.
class Users(models.Model):
    """用户表"""
    SEX_CHOICES = (
        (0, 'man'),
        (1, 'woman')
    )
    token = models.CharField(max_length=150, verbose_name='用户凭证', primary_key=True)
    name = models.CharField(max_length=64, verbose_name='用户名称', null=True)
    sex = models.SmallIntegerField(choices=SEX_CHOICES, default=0, verbose_name='性别', null=True)
    age = models.IntegerField(verbose_name='年龄', null=True)
    weight = models.IntegerField(verbose_name='体重', null=True)
    # height = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='身高', null=True)
    height = models.IntegerField(verbose_name='身高', null=True)
    health = models.CharField(max_length=200, verbose_name='健康描述', null=True)
    birthday = models.CharField(max_length=64, verbose_name='生日', null=True)
    phone = models.CharField(max_length=64, verbose_name='联系电话', null=True)
    contacts = models.IntegerField(verbose_name='应急联系人', null=True)
    creat_data = models.DateField(auto_now=True, verbose_name='创建时间')  # auto_now表示每次保存对 象时，自动设置该字段为当前时间

    class Meta:
        db_table = 'User'
        verbose_name = '药箱用户表'

    def __str__(self):
        return self.token
