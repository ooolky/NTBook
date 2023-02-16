users = {}
#构建用户-物品评分表users
for user in data:
    for item in data:
        if item.user == user:
            user.add(item)
        users.add(user)
#计算用户相似度矩阵sims
for user1, items1 in users:
    for user2, items2 in users:
        vec1, vec2 = {}
        for item1, rating1, in items1:
            vec1.add(rating1)
            for item2, rating2 in items2:
                if item1 == item2:
                    vec2.add(rating2)
            sims.add(corrcoef_pearson(vec1,vec2))
#预测target对所有未评分过的物品的评分predicts
for item in data
    if item not in target:
       for user in sims:
           weight+=user.sim*(target.item.rating-user.rating.average)
           corr_sum+=user.sim
       predicts.add(target.rating.average+weigh/sims_len)
#选择预测评分最高的n项
items=predicts.quicksot().topN(n)

