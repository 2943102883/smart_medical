from django.db import models

# Create your models here.
from apps.user.models import Users


class Medicine_self(models.Model):
    """程序自带药库"""
    name = models.CharField(max_length=200, verbose_name='药品名称')
    category = models.CharField(max_length=200, verbose_name='药品类别', null=True)
    introduce = models.CharField(max_length=200, verbose_name='简介', null=True)
    creat_data = models.DateField(auto_now=True, verbose_name='创建时间')  # auto_now表示每次保存对象时，自动设置该字段为当前时间
    suit = models.CharField(max_length=400, verbose_name='适应症状', null=True)
    bad = models.CharField(max_length=400, verbose_name='不良症状', null=True)
    life = models.IntegerField(verbose_name='保质期')
    usemethod = models.CharField(max_length=400, verbose_name='使用方法', null=True)
    taboo = models.CharField(max_length=200, verbose_name='禁忌', null=True)
    heed = models.CharField(max_length=200, verbose_name='注意事项', null=True)
    savemethod = models.CharField(max_length=200, verbose_name='保存方法', null=True)

    class Meta:
        db_table = 'medicine_self'
        verbose_name = '程序自带药库'

    def __str__(self):
        return self.name


class Medicine_user(models.Model):
    """用户自己添加的药品
    阿昔洛韦
    """
    name = models.CharField(max_length=200, verbose_name='药品名称')
    category = models.CharField(max_length=200, verbose_name='药品类别', null=True)
    introduce = models.CharField(max_length=200, verbose_name='简介', null=True)
    creat_data = models.DateField(auto_now_add=True, verbose_name='创建时间')  # auto_now表示每次保存对象时，自动设置该字段为当前时间
    suit = models.CharField(max_length=200, verbose_name='适应症状', null=True)
    bad = models.CharField(max_length=200, verbose_name='不良症状', null=True)
    life = models.IntegerField(verbose_name='保质期', null=True)
    use = models.CharField(max_length=200, verbose_name='使用方法', null=True)
    taboo = models.CharField(max_length=200, verbose_name='禁忌', null=True)
    heed = models.CharField(max_length=200, verbose_name='注意事项', null=True)
    savemethod = models.CharField(max_length=200, verbose_name='保存方法', null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='medicine',
                             verbose_name='关联用户')  # 后面子表调用父表，用User.medicine就行

    # user = models.CharField(max_length=200, verbose_name='关联用户')

    class Meta:
        db_table = 'medicine_user'
        verbose_name = '用户自己添加的药品'

    def __str__(self):
        return self.name


# 下面这两个分别是爬虫爬下来的数据
class Medicals(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name='药品名称')

    class Meta:
        db_table = 'medicals'
        verbose_name = '药品存储'

    def __str__(self):
        return self.name


class Medical_loads(models.Model):
    name = models.CharField(max_length=64, verbose_name='药品具体名字', null=True)
    num = models.IntegerField(verbose_name='爬虫顺序', null=True)  # 爬虫爬下来后，是有顺序的，这个就是标记这个顺序
    img_url = models.CharField(max_length=200, verbose_name='图片地址', null=True)
    suit = models.CharField(max_length=1000, verbose_name='适应症状', null=True)
    usemethod = models.CharField(max_length=1000, verbose_name='使用方法', null=True)
    lelment = models.CharField(max_length=200, verbose_name='成分', null=True)
    bad = models.CharField(max_length=1000, verbose_name='不良反应', null=True)
    err = models.CharField(max_length=200, verbose_name='禁忌', null=True)
    heed = models.CharField(max_length=1000, verbose_name='注意事项', null=True)
    savemethod = models.CharField(max_length=200, verbose_name='保存方法', null=True)
    medical = models.ForeignKey(Medicals, on_delete=models.CASCADE, related_name='medical', verbose_name='关联药品')

    class Meta:
        db_table = 'medical_loads'
        verbose_name = '存储的药品们'

    def __str__(self):
        return self.img_url


class Image_Urls(models.Model):
    name = models.CharField(max_length=64, verbose_name='图片链接')
    url1 = models.CharField(max_length=200, verbose_name='url1')
    url2 = models.CharField(max_length=200, verbose_name='url2')
    url3 = models.CharField(max_length=200, verbose_name='url3')

    class Meta:
        db_table = 'img_urls'
        verbose_name = '图片链接'

    def __str__(self):
        return self.name
