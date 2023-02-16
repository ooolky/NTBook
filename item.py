#构建物品-用户评分表items
for item in data:
    for user in data:
        if user.item == item:
            items.add(user)
#计算物品相似度矩阵sims
for user1, items1 in users:
    for user2, items2 in users:
        vec1, vec2 = {}
        for user1, rating1, in users1:
            vec1.add(rating1)
            for user2, rating2 in users2:
                if item1 == item2:
                    vec2.add(rating2)
            sims[item1][item2]=corrcoef_pearson(vec1,vec2)
#预测target对所有未评分过的物品的评分predicts
for item in data
    if item not in target:
       #从target评过分的物品中选择与item最相似的k件物品
       sims_item=sims.[item].topN(k)
       for user,item,sim in sims_item:
           weight+=sims_item[target][item]*(target.item.rating-user.ratings.average)
           corr_sum+=sims_item[target][item]
       predicts.add(target.rating.averages+weigh/corr_sum)
#选择预测评分最高的n项
items=predicts.quicksot().topN(n)