# Generated by Django 3.1.7 on 2021-03-18 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210318_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='token',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='用户凭证'),
        ),
    ]
