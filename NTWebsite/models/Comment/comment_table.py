from django.db import models
from ..User import *
from ..Topic import *
import uuid
# 书评评论表


class CommentInfo(models.Model):
    """docstring for CommentInfo"""

    ObjectID = models.CharField(
        primary_key=True, max_length=12,default='', editable=True, verbose_name='ID')
    TopicID = models.ForeignKey(TopicInfo, to_field='ObjectID', default=0, on_delete=models.CASCADE, verbose_name='书评')
    Content = models.TextField(verbose_name="评论内容")
    Parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    Like = models.IntegerField(verbose_name='赞', default="0")
    Type = models.CharField(
        max_length=30, editable=True, default='T', verbose_name='评论归属')
    Dislike = models.IntegerField(verbose_name='怼', default="0")
    EditDate = models.DateTimeField(auto_now_add=True, verbose_name='编辑时间')
    Publisher = models.ForeignKey(
        User, to_field='id', default=0, on_delete=models.CASCADE, verbose_name='用户名')

    class Meta:
        verbose_name = '评论统计'
        # 末尾不加s
        verbose_name_plural = '评论统计'
        app_label = 'NTWebsite'

    def __str__(self):
        return str(self.ObjectID)
