# Generated by Django 2.0.6 on 2022-04-18 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('ID', models.CharField(default='', max_length=12, primary_key=True, serialize=False, verbose_name='通知ID')),
                ('Type', models.CharField(max_length=15, verbose_name='通知类型')),
            ],
            options={
                'verbose_name': '通知信息',
                'verbose_name_plural': '通知信息',
            },
        ),
    ]