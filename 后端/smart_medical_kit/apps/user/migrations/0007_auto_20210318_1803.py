# Generated by Django 3.1.7 on 2021-03-18 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20210318_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='token',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='用户凭证'),
        ),
    ]
