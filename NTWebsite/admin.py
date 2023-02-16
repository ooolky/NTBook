from .improtFiles.models_import_head import *

# Register your models here.

# -----------------Comment------------------


@admin.register(CommentInfo)
class CommentInfoAdminView(admin.ModelAdmin):
    """docstring for CommentInfo"""
    list_display = ('Content', 'Publisher',
                    'EditDate', 'Type')
# --------------Configuration-----------------


@admin.register(FilterQueryString)
class FilterQueryStringAdminView(admin.ModelAdmin):
    """docstring for FilterQueryString"""
    hide = True
    # list_display = ('Name',)


@admin.register(PreferredConfigName)
class PreferredConfigNameAdminView(admin.ModelAdmin):
    """docstring for PreferredConfigName"""
    hide = True
    # list_display = ('Name',)


@admin.register(ConfigParams)
class ConfigParamsAdminView(admin.ModelAdmin):
    """docstring for ConfigParams"""
    hide = True
    # list_display = ('Name',)

# -------------------Opreation------------


@admin.register(BlackList)
class BlackListAdminView(admin.ModelAdmin):
    hide = True
    # list_display = ('Enforceder', 'Handler',)


@admin.register(PublisherList)
class PublisherListAdminView(admin.ModelAdmin):
    list_display = ('Order',)


@admin.register(Notification)
class NotificationAdminView(admin.ModelAdmin):
    hide = True
    # list_display = ('TargetUser',)


@admin.register(TopicAttitude)
class TopicAttitudeAdminView(admin.ModelAdmin):
    """docstring for Attitude"""
    list_display = ('Publisher',)

@admin.register(CommentAttitude)
class CommentAttitudeAdminView(admin.ModelAdmin):
    """docstring for Attitude"""
    hide = True
    # list_display = ('Publisher',)

@admin.register(UserLink)
class UserLinkAdminView(admin.ModelAdmin):
    """docstring for ArticleComment"""
    list_display = ('UserBeLinked', 'UserLinking', 'LinkTime')


@admin.register(Collect)
class CollectionAdminView(admin.ModelAdmin):
    """docstring for Collection"""
    list_display = ('Publisher', 'ObjectID', 'CollectTime')

@admin.register(Concern)
class ConcernAdminView(admin.ModelAdmin):
    """docstring for Collection"""
    hide = True
    # list_display = ('Publisher', 'ObjectID', 'CollectTime')

@admin.register(Circusee)
class CircuseeAdminView(admin.ModelAdmin):
    """docstring for Collection"""
    hide = True
    # list_display = ('Publisher', 'ObjectID', 'CollectTime')

@admin.register(ReadsIP)
class ReadsIPAdminView(admin.ModelAdmin):
    """docstring for ReadsIP"""
    list_display = ('IP', 'Type')


@admin.register(TipOffBox)
class TipOffBoxAdminView(admin.ModelAdmin):
    """docstring for TipOffBox"""
    hide = True
    # list_display = ('Type', 'ObjectID')

#----------------RollCall-------------------


@admin.register(RollCallInfo)
class RollCallInfoAdminView(admin.ModelAdmin):
    """docstring for RollCallInfo"""
    hide = True
    # list_display = ('Title', 'Publisher', 'Target',)
    # search_fields = ['Publisher__Nick','Title']

@admin.register(RollCallDialogue)
class RollCallDialogueAdminView(admin.ModelAdmin):
    hide = True
    # list_display = ('RollCallID', 'EditDate',)
    # search_fields = ['Publisher__Nick','RollCallID__Title','Content']
#-----------------Search-------------------


@admin.register(SearchIndex)
class SearchIndexAdminView(admin.ModelAdmin):
    list_display = ('Content', 'Type',)

# ------------------Topic--------------------


@admin.register(TopicThemeInfo)
class TopicThemeInfoAdminView(admin.ModelAdmin):
    """docstring for TopicThemeInfo"""
    list_display = ('Name',)


@admin.register(TopicCategoryInfo)
class TopicCategoryInfoAdminView(admin.ModelAdmin):
    """docstring for TopicCategoryInfo"""
    list_display = ('Name',)


@admin.register(TopicInfo)
class TopicInfoAdminView(admin.ModelAdmin):
    """docstring for TopicInfo"""
    readonly_fields = ('EditTime',)
    list_display = ('Title','Publisher_id','Recommend','EditTime')
    search_fields = ['Title','Publisher__Nick'] 


@admin.register(User)
class UserAdminView(admin.ModelAdmin):
    """docstring for UserTable"""
    list_display = ('username', 'date_joined',)
