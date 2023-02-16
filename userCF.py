import numpy as np
import pandas as pd
from surprise import Reader, Dataset

# 第1步：引入ML-100k数据集并建立用户-物品表：user_data
reader = Reader(line_format='user item rating ', sep='\t')
raw_data = Dataset.load_from_file(file_path='.data/ml-100k/u.data', reader=reader)
user_data = user_item(raw_data)
# 第2步:计算用户相似矩阵：similarity_matrix
similarity_matrix = pd.DataFrame(np.identity(len(user_data)), index=user_data.keys(), columns=user_data.keys(), )
# 遍历每条用户-物品评分数据
for u1, items1 in user_data.items():
    for u2, items2 in user_data.items():
        if u1 == u2: continue
        vec1, vec2 = [], []
        for item, rating1 in items1.items():
            rating2 = items2.get(item, -1)
            if rating2 == -1: continue
            vec1.append(rating1)
            vec2.append(rating2)
        # 计算不同用户之间的皮尔逊相关系数
        similarity_matrix[u1][u2] = np.corrcoef(vec1, vec2)[0][1]
# 第3步：计算与target_user最相似的 num 个用户：sim_users
# 由于最相似的用户为自己，去除本身，
sim_users = similarity_matrix[target_user].sort_values(ascending=False)[1:num + 1].index.tolist()
# 第4步：预测target_user对target_item的评分:target_item_pred
weighted_scores = 0.
corr_values_sum = 0.
# 基于皮尔逊相关系数预测用户评分
for user in sim_users:
    corr_value = similarity_matrix[target_user][user]
    user_mean_rating = np.mean(list(user_data[user].values()))
    weighted_scores += corr_value * (user_data[user][target_item] - user_mean_rating)
    corr_values_sum += corr_value
target_user_mean_rating = np.mean(list(user_data[target_user].values()))
target_item_pred = target_user_mean_rating + weighted_scores / corr_values_sum

