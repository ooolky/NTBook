from NTWebsite.improtFiles.views_import_head import *
from NTWebsite.improtFiles.models_import_head import *


def Launcher(request, **URLParams):
    # 获取查询模式中的对应方法String
    DBConf = DC(
        '-'.join([URLParams['Region'], URLParams['Part'], URLParams['Order']]))
    MethodSwitcher = eval(DBConf.MethodString)
    # 执行对应的方法
    return MethodSwitcher(request, DBConf, AC(), URLParams)


def Activate(request, **URLParams):
    return P.UserActive(request, URLParams['UserID'], URLParams['Key'])


def TopicsInfoGet(request, DBConf, APPConf, URLParams):
    # 获取符合条件的书评对象并且获取权限
    TopicObjects = A.Empower(URLParams['Region'], QRC(
        DBConf.QueryString, None, URLParams['Region'], URLParams['FilterValue']), request)
    # 推荐列表
    if URLParams['Order'] == 'RC':
        recommends = request.user.Recommend.split(',')
        recommends.pop()
        for recommend in recommends:
            for TopicObject in TopicObjects:
                if TopicObject[0].ObjectID != int(recommend):
                    TopicObjects.remove(TopicObject)
    # 书评分页器
    PaginatorDict = P.PaginatorInfoGet(
        TopicObjects, APPConf.TopicsPageLimit, URLParams)
    # 返回上下文信息
    return render(request, DBConf.Template, P.ContextConfirm(request, URLParams=URLParams, Object=TopicObjects, PaginatorDict=PaginatorDict, APPConf=APPConf))


def TopicContentInfoGet(request, DBConf, APPConf, URLParams):
    # 分享链入统计
    if URLParams['ExtraParam'] == 'Share':
        mMs.CounterOperate(QRC('TopicInfo.objects.get(ObjectID=%s)',
                               None, URLParams['FilterValue']), 'Share', '+')

    # 阅读量、热度统计
    if not QRC('ReadsIP.objects.filter(IP=%s,ObjectID=%s)', None, mMs.GetUserIP(request), URLParams['FilterValue']):
        P.ReadIPRecord(mMs.GetUserIP(request),
                       URLParams['FilterValue'], URLParams['Region'])
        mMs.CounterOperate(QRC('TopicInfo.objects.get(ObjectID=%s)',
                               0, URLParams['FilterValue']), 'Hot', '+')
    # 获取指定书评对象
    TopicObject = A.Empower(URLParams['Region'], QRC(
        DBConf.QueryString, None, URLParams['FilterValue']), request)

    # 获取评论对象
    CommentObjects = P.CommentPackage(A.Empower('Comment',
                                                QRC("CommentInfo.objects.filter(TopicID=%s).order_by('-EditDate')",
                                                    None,
                                                    TopicObject[0][0]),
                                                request))
    # 评论分页器
    PaginatorDict = P.PaginatorInfoGet(
        CommentObjects, APPConf.CommentsPageLimit, URLParams)

    # 返回上下文信息
    return render(request, DBConf.Template, P.ContextConfirm(request, URLParams=URLParams, Object=TopicObject, PaginatorDict=PaginatorDict, APPConf=APPConf))

def SearchInfoGet(request, DBConf, APPConf, URLParams):
    # 获取符合条件的对象并且获取权限
    ResultObjects = A.Empower(URLParams['Part'] if URLParams['Part'] != 'User' else 'UserProfile',
                              QRC(DBConf.QueryString, None, URLParams['FilterValue'], URLParams['FilterValue'], URLParams['Part'])
                              if URLParams['Part'] in 'SpecialTopic' else QRC(DBConf.QueryString, None, URLParams['FilterValue']), request)
    # 分页器
    PaginatorDict = P.PaginatorInfoGet(
        ResultObjects, APPConf.TopicsPageLimit, URLParams)
    # 返回上下文信息
    return render(request, DBConf.Template, P.ContextConfirm(request, URLParams=URLParams, PaginatorDict=PaginatorDict, APPConf=APPConf))


def RollCallsInfoGet(request, DBConf, APPConf, URLParams):
    RollCallObjects = A.Empower(URLParams['Region'], QRC(
        DBConf.QueryString, None, URLParams['FilterValue']), request)
    PaginatorDict = P.PaginatorInfoGet(
        RollCallObjects, APPConf.TopicsPageLimit, URLParams)
    return render(request, DBConf.Template, P.ContextConfirm(request, URLParams=URLParams, PaginatorDict=PaginatorDict, APPConf=APPConf))


def RollCallInfoContentInfoGet(request, DBConf, APPConf, URLParams):
    # 分享链入统计
    if URLParams['ExtraParam'] == 'Share':
        mMs.CounterOperate(QRC('RollCallInfo.objects.get(ObjectID=%s)',
                               None, URLParams['FilterValue']), 'Share', '+')
    # 阅读量、热度统计
    if not QRC('ReadsIP.objects.filter(IP=%s,ObjectID=%s)', None, mMs.GetUserIP(request), URLParams['FilterValue']):
        P.ReadIPRecord(mMs.GetUserIP(request),
                       URLParams['FilterValue'], URLParams['Region'])
        mMs.CounterOperate(QRC('RollCallInfo.objects.get(ObjectID=%s)',
                               0, URLParams['FilterValue']), 'Hot', '+')
    # 获取指定书评对话对象
    RollCallObject = A.Empower('RollCall', QRC(
        'RollCallInfo.objects.get(ObjectID=%s)', None, URLParams['FilterValue']), request)[0]
    # 获取指定书评对话对象
    DialogueObject = QRC(DBConf.QueryString, None, URLParams['FilterValue'])
    # 分页器
    # 返回上下文信息
    return render(request, DBConf.Template, P.ContextConfirm(request, URLParams=URLParams, Object=DialogueObject, MainObject=RollCallObject, APPConf=APPConf))


def UserProfileInfoGet(request, DBConf, APPConf, URLParams):
    # 获取用户主题信息
    TargetUser = A.Empower('UserProfile', QRC(
        'User.objects.get(id=%s)', None, URLParams['FilterValue']), request)
    # 获取用户Selection内容
    # 直接获取书评
    if URLParams['Part'] in 'SpecialTopic':
        Objects = A.Empower(URLParams['Part'], QRC(DBConf.QueryString, None, URLParams['FilterValue']), request)

    elif URLParams['Part'] in ['Comment']:
        Topics = []
        for item in QRC(DBConf.QueryString, None, URLParams['FilterValue']):
            if item != None:
                Topics.append(item.TopicID)
        Objects = A.Empower('Topic', list(set(Topics)), request)

    elif URLParams['Part'] in ['TopicLike', 'TopicDislike', 'CommentLike', 'CommentDislike']:
        Topics = []
        for item in QRC(DBConf.QueryString, None, URLParams['FilterValue']):
            if item != None:
                Topics.append(item.ObjectID if URLParams['Part'] in [ 'TopicLike', 'TopicDislike'] else item.ObjectID.TopicID)
        Objects = A.Empower('Topic', list(set(Topics)), request)

    elif URLParams['Part'] in ['Collect', 'Concern', 'Circusee']:
        ObjectType = {
            'Collect': 'Topic',
            'Concern': 'SpecialTopic',
            'Circusee': 'RollCall'}
        Topics = []
        for item in QRC(DBConf.QueryString, None, URLParams['FilterValue']):
            if item != None:
                Topics.append(item.ObjectID)
        Objects = A.Empower( ObjectType[URLParams['Part']], list(set(Topics)), request)

    elif URLParams['Part'] in ['Focus', 'Fans']:
        UserObjects = []
        for UserObject in QRC(DBConf.QueryString, None, QRC('User.objects.get(id=%s)', 0, URLParams['FilterValue'])):
            if UserObject != None:
                UserObjects.append(UserObject.UserLinking if URLParams['Part'] == 'Fans' else UserObject.UserBeLinked)
        Objects = A.Empower('User', list(set(UserObjects)), request)
    # 分页器
    PaginatorDict = P.PaginatorInfoGet(
        Objects, APPConf.CommonPageLimit, URLParams)

    return render(request, DBConf.Template, P.ContextConfirm(request, User=TargetUser, PaginatorDict=PaginatorDict, URLParams=URLParams, APPConf=APPConf))

def CategoryContentInfoGet(request, DBConf, APPConf, URLParams):
    # 获取书籍
    TargetCategory = A.Empower('Category', QRC(
        'TopicCategoryInfo.objects.get(id=%s)', None, URLParams['FilterValue']), request)

    # 获取书籍
    Objects = A.Empower('Topic', list(QRC('TopicInfo.objects.filter(Category_id=%s)', None, URLParams['FilterValue'])), request)

    # 分页器
    PaginatorDict = P.PaginatorInfoGet(
        Objects, APPConf.CommonPageLimit, URLParams)

    return render(request, DBConf.Template, P.ContextConfirm
    (request, Category=TargetCategory,PaginatorDict=PaginatorDict, URLParams=URLParams, APPConf=APPConf))

if __name__ == "__main__":
    print('%s')
