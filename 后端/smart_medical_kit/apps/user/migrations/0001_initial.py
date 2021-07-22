# Generated by Django 3.1.7 on 2021-03-18 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('token', models.CharField(max_length=200, primary_key=True, serialize=False, verbose_name='用户凭证')),
                ('sex', models.SmallIntegerField(choices=[(0, 'man'), (1, 'woman')], default=0, null=True, verbose_name='性别')),
                ('age', models.IntegerField(null=True, verbose_name='年龄')),
                ('weight', models.IntegerField(null=True, verbose_name='体重')),
                ('height', models.DecimalField(decimal_places=2, max_digits=3, null=True, verbose_name='身高')),
                ('health', models.CharField(max_length=200, null=True, verbose_name='健康描述')),
                ('contacts', models.IntegerField(null=True, verbose_name='应急联系人')),
                ('creat_data', models.DateField(auto_now=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '药箱用户表',
                'db_table': 'User',
            },
        ),
    ]
