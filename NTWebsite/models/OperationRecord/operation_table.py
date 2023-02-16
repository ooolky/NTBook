from django.db import models
from ..User import *
from ..Topic import *
from ..RollCall import *
from ..Comment import *
import uuid

# 立场统计
class TopicAttitude(models.Model):
    Publisher = models.ForeignKey(
        User, to_field='id', default=0, on_delete=models.CASCADE, verbose_name='用户')
    Point = models.IntegerField(null=True,blank=False, verbose_name='立场代码')
    EditTime = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    ObjectID = models.ForeignKey(TopicInfo,to_field='ObjectID',default=0, on_delete=models.CASCADE, verbose_name='书评')
    Type = models.CharField(max_length=30, blank=True, verbose_name='类型')

    class Meta:
        verbose_name = '书评赞/怼统计'
        # 末尾不加s
        verbose_name_plural = '书评赞/怼统计'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.Publisher.Nick

class CommentAttitude(models.Model):
    Publisher = models.ForeignKey(
        User, to_field='id', default=0, on_delete=models.CASCADE, verbose_name='用户')
    Point = models.IntegerField(null=True,blank=False, verbose_name='立场代码')
    EditTime = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    ObjectID = models.ForeignKey(CommentInfo, to_field='ObjectID',default=0, on_delete=models.CASCADE, verbose_name='评论')
    Type = models.CharField(max_length=30, blank=True, verbose_name='类型')

    class Meta:
        verbose_name = '评论赞/怼统计'
        # 末尾不加s
        verbose_name_plural = '评论赞/怼统计'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.Publisher.Nick

# 阅读IP统计


class ReadsIP(models.Model):
    """docstring for ArticleLikseIP"""
    IP = models.CharField(max_length=100, null=True,
                          blank=True, verbose_name='IP')
    EditDate = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    Type = models.CharField(
        max_length=30, default='T', blank=True, verbose_name='IP归入')
    ObjectID = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='书评ID')

    class Meta:
        verbose_name = '访问统计'
        # 末尾不加s
        verbose_name_plural = '访问统计'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.IP

# 用户关注


class UserLink(models.Model):
    """docstring for UserLink"""
    UserBeLinked = models.ForeignKey(
        User, to_field='id', default='', blank=False, on_delete=models.CASCADE, verbose_name='被关注用户')
    UserLinking = models.ForeignKey(
        User, to_field='id', related_name='NickLinking', default='', blank=False, on_delete=models.CASCADE, verbose_name='关注用户')
    LinkTime = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    class Meta:
        verbose_name = '用户链接统计'
        verbose_name_plural = '用户链接统计'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.UserBeLinked.Nick

# 收藏、关注、围观
class Collect(models.Model):
    """docstring for Collect"""
    Publisher = models.ForeignKey(
        User, to_field='id', default=0, on_delete=models.CASCADE, verbose_name='用户名')
    ObjectID = models.ForeignKey(TopicInfo, to_field='ObjectID', default=0, on_delete=models.CASCADE,verbose_name='书评ID')
    CollectTime = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    class Meta:
        verbose_name = '收藏统计'
        verbose_name_plural = '收藏统计'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.Publisher.Nick

class Concern(models.Model):
    """docstring for Concern"""
    Publisher = models.ForeignKey(
        User, to_field='id', default=0, on_delete=models.CASCADE, verbose_name='用户名')
    ObjectID = models.ForeignKey(TopicInfo, to_field='ObjectID', default=0, on_delete=models.CASCADE,verbose_name='专题ID')
    CollectTime = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    class Meta:
        verbose_name = '关注统计'
        verbose_name_plural = '关注统计'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.Publisher.Nick

class Circusee(models.Model):
    """docstring for Circusee"""
    Publisher = models.ForeignKey(
        User, to_field='id', default=0, on_delete=models.CASCADE, verbose_name='用户名')
    ObjectID = models.ForeignKey(RollCallInfo, to_field='ObjectID', default=0, on_delete=models.CASCADE,verbose_name='点名ID')
    CollectTime = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    class Meta:
        verbose_name = '围观统计'
        verbose_name_plural = '围观统计'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.Publisher.Nick

class PublisherList(models.Model):
    Publisher = models.ForeignKey(
        User, to_field='id', default=0, on_delete=models.CASCADE, verbose_name='用户名')
    Order = models.IntegerField(
        default=0, blank=False, verbose_name='顺序')

    class Meta:
        verbose_name = '推荐用户'
        # 末尾不加s
        verbose_name_plural = '推荐用户表'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.Publisher.Nick


class Notification(models.Model):

    ID = models.CharField(
        primary_key=True, max_length=12,default='', editable=True, verbose_name='通知ID')
    Region = models.CharField(
        max_length=100, blank=False, default='', verbose_name='目标区域')
    ObjectID = models.CharField(
        max_length=100, blank=False, default='', verbose_name='目标ID')
    AnchorID = models.CharField(
        max_length=100, blank=False, default='', verbose_name='定位ID')
    SourceUser = models.ForeignKey(
        User, to_field='id', related_name='SourceUser', default=0, on_delete=models.CASCADE, verbose_name='通知者')
    TargetUser = models.ForeignKey(
        User, to_field='id', related_name='TargetUser', default=0, on_delete=models.CASCADE, verbose_name='被通知者')

    class Meta:
        verbose_name = '通知'
        # 末尾不加s
        verbose_name_plural = '通知中心'
        app_label = 'NTWebsite'

    def __str__(self):
        return str(self.ID)


class BlackList(models.Model):
    """docstring for blacklist"""

    ID = models.CharField(
        primary_key=True, max_length=12,default='', editable=True, verbose_name='黑名单ID')
    Enforceder = models.ForeignKey(User, to_field='id', related_name='BlackList_User',
                                   on_delete=models.CASCADE, default=0, verbose_name='被添加用户')
    Handler = models.ForeignKey(
        User, to_field='id', related_name='Handler', null=True, on_delete=models.CASCADE, verbose_name='操作用户')

    class Meta:
        verbose_name = '黑名单记录'
        # 末尾不加s
        verbose_name_plural = '黑名单'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.ID


class TipOffBox(models.Model):
    """docstring for ComplaintBox"""

    ObjectID = models.CharField(
        max_length=100, blank=False, default='', verbose_name='对象ID')
    Type = models.CharField(
        max_length=30, blank=False, default='', verbose_name='对象类型')
    Content = models.CharField(
        max_length=100, blank=False, default='', verbose_name='举报内容')
    Publisher = models.ForeignKey(
        User, to_field='id', related_name='TipOffUser', null=True, on_delete=models.CASCADE, verbose_name='举报用户')
    EditDate = models.DateTimeField(auto_now_add=True, verbose_name='编辑时间')

    class Meta:
        verbose_name = '举报统计'
        # 末尾不加s
        verbose_name_plural = '举报统计'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.Type + self.ObjectID
