# Generated by Django 3.1.7 on 2021-05-21 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0003_medical_loads_translate'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine_user',
            name='medicalkit',
            field=models.IntegerField(default=1, verbose_name='添加到的药箱位置'),
        ),
    ]
