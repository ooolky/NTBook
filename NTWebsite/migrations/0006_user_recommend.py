# Generated by Django 3.0.6 on 2022-05-18 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NTWebsite', '0005_auto_20220419_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Recommend',
            field=models.TextField(blank=True, max_length=1000, verbose_name='推荐列表'),
        ),
    ]
