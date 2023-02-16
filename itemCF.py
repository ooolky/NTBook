import numpy as np
import pandas as pd
from surprise import Reader, Dataset
from surprise.model_selection import train_test_split

# 第1步：引入ML-100k数据集并建立物品-用户表：user_data
reader = Reader(line_format='item user rating ', sep='\t')
raw_data = Dataset.load_from_file(file_path='.data/ml-100k/u.data', reader=reader)
item_data = item_user(raw_data)
# 第2步:计算用户相似矩阵：similarity_matrix
similarity_matrix = pd.DataFrame(np.identity(len(user_data)),index=user_data.keys(),columns=user_data.keys(),)
# 遍历每条用户-物品评分数据
similarity_matrix = pd.DataFrame(np.identity(len(item_data)),index=item_data.keys(),columns=item_data.keys(),)
# 遍历每条物品-用户评分数据
for i1, users1 in item_data.items():
    for i2, users2 in item_data.items():
        if i1 == i2:
            continue
        vec1, vec2 = [], []
        for user, rating1 in users1.items():
            rating2 = users2.get(user, -1)
            if rating2 == -1:
                continue
            vec1.append(rating1)
            vec2.append(rating2)
        similarity_matrix[i1][i2] = np.corrcoef(vec1, vec2)[0][1]
# 第3步：从target_user购买过的物品中，选出与物品target_item最相似的num件物品：sim_users
sim_items = []
sim_items_list = similarity_matrix[target_item].sort_values(ascending=False).index.tolist()
for item in sim_items_list:
    # 如果target_user对物品item评分过
    if target_user in item_data[item]:
        sim_items.append(item)
    if len(sim_items) == num:
        break
# 第4步：预测用户（target_user）对物品（target_item）的评分:target_item_pred
target_user_mean_rating = np.mean(list(item_data[target_item].values()))
weighted_scores = 0.
corr_values_sum = 0.
for item in sim_items:
    corr_value = similarity_matrix[target_item][item]
    user_mean_rating = np.mean(list(item_data[item].values()))
    weighted_scores += corr_value * (item_data[item][target_user] - user_mean_rating)
    corr_values_sum += corr_value
target_item_pred = target_user_mean_rating + weighted_scores / corr_values_sum