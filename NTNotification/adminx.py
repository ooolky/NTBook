from NTNotification.models import *
import xadmin
# Register your models here.



class NoticeAdminView(object):
    """docstring for PublishNotification"""
    list_display = ('ID',)

# xadmin.site.register(Notice, NoticeAdminView)
