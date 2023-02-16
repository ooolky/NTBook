from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.processors import SmartResize
from ckeditor_uploader.fields import RichTextUploadingField
from ..User import *
import uuid
import django.utils.timezone as timezone

class TopicThemeInfo(models.Model):
    """docstring for TopicThemeInfo"""
    Name = models.CharField(max_length=20, default='', null=False,verbose_name='标签名称')

    class Meta:
        verbose_name = '标签统计'
        # 末尾不加s
        verbose_name_plural = '标签统计'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.Name

# 品类信息表


class TopicCategoryInfo(models.Model):

    Name = models.CharField(max_length=50, default='', null=False, verbose_name='名字')
    SVG = models.TextField(max_length=1000, default='', null=False, verbose_name='作者')
    Description = models.TextField(max_length=140, default='', null=False, verbose_name='描述')
    Rating = models.FloatField(max_length=10, default=0, verbose_name='评分')
    RatingNumber = models.IntegerField(default=0, verbose_name='评分人数')

    class Meta:
        verbose_name = '类目'
        # 末尾不加s
        verbose_name_plural = '书籍统计'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.Name


# 书评信息表.

class TopicInfo(models.Model):
    """docstring for TopicInfo"""
    ObjectID = models.CharField(
        primary_key=True, max_length=12, default='', editable=True, verbose_name='书评ID')
    # ID = models.CharField(
    #    primary_key=True, auto_created=True, max_length=12, default=str(uuid.uuid4())[-12:], verbose_name='书评ID')
    Title = models.CharField(
        max_length=35, verbose_name='标题')
    Description = models.TextField(max_length=140, default='', null=False, verbose_name='书评描述')
    Publisher = models.ForeignKey(
        User, to_field='id', default=0, on_delete=models.CASCADE, related_name='Topic_User', verbose_name='用户名')
    Theme = models.ManyToManyField(
        TopicThemeInfo, verbose_name='书评标签', related_name='Topic_Theme')
    Category = models.ForeignKey(
        TopicCategoryInfo,to_field='id', on_delete=models.CASCADE, null=True, related_name='Topic_Category', verbose_name='书评类别')

    Content = RichTextUploadingField(
        null=True, blank=True, config_name='admin', verbose_name='书评正文')
    Type = models.CharField(
        max_length=20, default='Topic', verbose_name='书评类型')
    # SpecialTopic字段
    Cover = models.ImageField(
        upload_to='Cover', blank=True, verbose_name='封面', default='')
    Cover_210x140 = ImageSpecField(processors=[
        SmartResize(210, 140)], format='JPEG', options={'quality': 95})
    Cover_SR965x300 = ImageSpecField(processors=[
        SmartResize(965, 300)], format='JPEG', options={'quality': 95})

    Recommend = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, default=0, verbose_name='推荐度')
    Like = models.IntegerField(verbose_name='赞', default=0)
    Dislike = models.IntegerField(verbose_name='怼', default=0)
    Hot = models.IntegerField(verbose_name='热度', default=10)
    Comment = models.IntegerField(verbose_name='评论数', default=0)
    Share = models.IntegerField(
        default=0, blank=False, verbose_name='分享')
    Collect = models.IntegerField(
        default=0, blank=False, verbose_name='关注或收藏量')
    EditTime = models.DateTimeField(auto_now=True, verbose_name='编辑时间')
    CreateTime = models.DateTimeField(default=timezone.now, editable=True,verbose_name='添加时间')
    Rating = models.FloatField(blank=False, default=0, verbose_name='评分')

    class Meta:
        verbose_name = '书评统计'
        # 末尾不加s
        verbose_name_plural = '书评统计'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.ObjectID
