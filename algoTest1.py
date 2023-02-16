# 可以使用上面提到的各种推荐系统算法
from surprise import KNNBasic, BaselineOnly
from surprise import Dataset
from surprise import evaluate
import pandas as pd

# 载入movielens数据集
data = Dataset.load_builtin('ml-100k')
# k折交叉验证(k=3)
k = 3
data.split(n_folds=k)
# 基于统计的算法
bsl_options = {'method': 'sgd',
               'learning_rate': .00005,
               'n_epochs': 20
               }
algo_sgd = BaselineOnly(bsl_options=bsl_options)
bsl_options = {'method': 'als',
               'n_epochs': 5,
               'reg_u': 12,
               'reg_i': 5
               }
algo_als = BaselineOnly(bsl_options=bsl_options)
# 协同过滤算法
sim_options = {'name': 'pearson',
               'user_based': True  # compute  similarities between items
               }
algo_user = KNNBasic(sim_options=sim_options)
sim_options = {'name': 'pearson',
               'user_based': False  # compute  similarities between items
               }
algo_item = KNNBasic(sim_options=sim_options)
# 测试
perf_sgd = evaluate(algo_sgd, data, measures=['RMSE'])
perf_als = evaluate(algo_als, data, measures=['RMSE'])
perf_user = evaluate(algo_user, data, measures=['RMSE'])
perf_item = evaluate(algo_item, data, measures=['RMSE'])
# 数据处理
result = pd.DataFrame(columns=['sgd', 'als', 'user', 'item'], index=range(k))
for n in range(k):
    result.loc[n, 'sgd'] = perf_sgd['RMSE'][n]
    result.loc[n, 'als'] = perf_als['RMSE'][n]
    result.loc[n, 'user'] = perf_user['RMSE'][n]
    result.loc[n, 'item'] = perf_item['RMSE'][n]
result.to_csv('result1.csv', encoding='utf-8-sig',  index=False)
# 绘图

