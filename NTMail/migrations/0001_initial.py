# Generated by Django 2.0.6 on 2022-04-18 11:32

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MailBody',
            fields=[
                ('Scene', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='发送场景')),
                ('Title', models.CharField(max_length=50, verbose_name='邮件标题')),
                ('Message', models.CharField(max_length=100, verbose_name='邮件内容')),
                ('Html', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='邮件HTML')),
            ],
            options={
                'verbose_name': '邮件模板',
                'verbose_name_plural': '邮件模板',
            },
        ),
    ]