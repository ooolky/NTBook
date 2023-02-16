from NTMail.models import *
import xadmin
# Register your models here.



class MailBodyAdminView(object):
    """docstring for PublishNotification"""
    list_display = ('Scene',)

# xadmin.site.register(MailBody, MailBodyAdminView)