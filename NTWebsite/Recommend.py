import sqlite3

import pandas as pd
from surprise import Dataset, KNNBasic ,Reader
from surprise.model_selection import train_test_split

class Recommend():
    def __init__(self, algo='KNNBasic', sim_options='pearson_baseline', user_based=False):
        '''
        初始化
        :param algo:  协同过滤具体算法
        :param sim_options: 计算相似度方式
        :param user_based: 基于用户/item的协同过滤
        '''
        self.user_based = user_based
        self.algo = algo
        self.sim_options = sim_options

    def fit(self, train_set):

        sim_options = {'name': self.sim_options, 'user_based': self.user_based}
        self.algo = KNNBasic(sim_options=sim_options)
        self.algo.fit(trainset=train_set)

    def get_k_nearest(self, inner_id, k_nearest):

        '''
        :return: 返回最近的k个邻居
        '''

        if self.algo.sim_options['user_based']:
            all_instances = self.algo.trainset.all_users
        else:
            all_instances = self.algo.trainset.all_items

        others = [(x, self.algo.sim[inner_id][x]) for x in all_instances() if x != inner_id]
        sorted_others = sorted(others, key=lambda x: x[1], reverse=True)
        return sorted_others[:k_nearest]

    def recommend(self, id, k_nearest, n_items):
        '''
        默认采用item-based
        :param id: 原始user_id
        :param k_nearest: 最近的k个邻居
        :param n_items: 最终推荐的n条item
        :return:
        '''
        user_based = self.user_based
        if user_based:
            recommend_dict = {}
            inner_id = self.algo.trainset.to_inner_uid(ruid=id)
            cur_user_like_and_rating = self.algo.trainset.ur[inner_id]
            cur_user_like_item = [ele[0] for ele in cur_user_like_and_rating]

            user_neighbors = self.get_k_nearest(inner_id, k_nearest)
            for neighbor, similarity in user_neighbors:
                neighbor_user_like_and_rating = self.algo.trainset.ur[neighbor]
                for item, rating in neighbor_user_like_and_rating:
                    if item in cur_user_like_item:
                        continue
                    else:
                        recommend_dict.setdefault(item, 0)
                        recommend_dict[item] += similarity * rating
            sorted_recommend_dict = sorted(recommend_dict.items(), key=lambda x: x[1], reverse=True)
            selected_item_list = [ele[0] for ele in sorted_recommend_dict[:n_items]]
            return selected_item_list
        else:
            recommend_dict = {}
            inner_id = self.algo.trainset.to_inner_uid(ruid=id)
            cur_user_like_and_rating = self.algo.trainset.ur[inner_id]
            cur_user_like_item = [ele[0] for ele in cur_user_like_and_rating]

            for item, rating in cur_user_like_and_rating:
                item_neighbors = self.get_k_nearest(item, k_nearest)
                for similar_item, similarity in item_neighbors:
                    if similar_item in cur_user_like_item:
                        continue
                    else:
                        recommend_dict.setdefault(similar_item, 0)
                        recommend_dict[similar_item] += rating * similarity
            sorted_recommend_dict = sorted(recommend_dict.items(), key=lambda x: x[1], reverse=True)
            selected_item_list = [ele[0] for ele in sorted_recommend_dict[:n_items]]
            return selected_item_list

    def recall_and_precision(self, test, k_nearest, n_items):
        '''
        :param test: 结构为[(user, item, rating)] 三元组组成的列表
        :param k_nearest:
        :param n_items:
        :return:
        '''
        hit = 0
        precison = 0
        recall = 0
        test_user_like = self.get_test_user_like(test)
        for user, item, rating in test:
            recommend_like = self.recommend(id=user, k_nearest=k_nearest, n_items=n_items)
            true_like = test_user_like[user]
            hit += len(set(recommend_like) & set(true_like))
            precison += len(recommend_like)
            recall += len(true_like)
        return hit / float(recall), hit / float(precison)

    def coverage(self, test, k_nearest, n_items):
        '''
        覆盖率: 推荐条目数/总条目数
        :param test:
        :param k_nearest:
        :param n_items:
        :return:
        '''
        test_user_like = self.get_test_user_like(test)
        all_items = set()
        recommend_items = set()
        for user, item, rating in test:
            recommend_like = self.recommend(id=user, k_nearest=k_nearest, n_items=n_items)
            true_like = test_user_like[user]
            for ele in true_like:
                all_items.add(ele)
            for ele in recommend_like:
                recommend_items.add(ele)

        return len(recommend_items) / float(all_items)

    def get_test_user_like(self, test):
        res = {}
        for user, item, rating in test:
            if user in res.keys():
                try:
                    res[user] = res[user].append(self.algo.trainset.to_inner_iid(item))
                except:
                    res[user] = res[user].append('no-exists')
            else:
                try:
                    res[user] = []
                    res[user].append(self.algo.trainset.to_inner_iid(item))
                except:
                    res[user] = []
                    res[user] = res[user].append('no-exists')
            # res[user] = res.setdefault(user,[]).append(self.algo.trainset.to_inner_iid(item))
        return res

    def run(self):
        # 建立数据库连接
        con = sqlite3.connect(r'C:\Users\LiKai\PycharmProjects\Django-Python-NagetiveWeb-Beta\db.sqlite3')
        # 从数据库获取数据
        raw_like = pd.read_sql_query("SELECT ObjectID_id,Publisher_id,Point from NTWebsite_topicattitude", con)
        raw_like.columns = ['objectID', 'userID', 'rating']
        raw_collect = pd.read_sql_query("SELECT ObjectID_id,Publisher_id from NTWebsite_collect", con)
        raw_collect.columns = ['objectID', 'userID']
        raw_collect.insert(loc=2, column='rating', value=1)
        # 合并数据，点踩=0、点踩=1、收藏=2
        df = pd.DataFrame(columns=['objectID', 'userID', 'rating'])
        df = raw_like.append(raw_collect)
        df['sum'] = df.groupby(['objectID', 'userID'])['rating'].transform('sum')
        df = df.drop(columns='rating')
        df = df.drop_duplicates()
        df.columns = ['objectID', 'userID', 'rating']
        # pandas数据集转换成surprise数据集
        reader = Reader(rating_scale=(0, 2))
        data = Dataset.load_from_df(df[['objectID', 'userID', 'rating']], reader)
        train, test = train_test_split(data, test_size=.2, random_state=1)
        # 执行算法
        self.fit(train_set=train)
        users = pd.read_sql_query("SELECT id,Recommend from NTWebsite_user", con)
        for user in users:
            recommend_res = self.recommend(id=user['id'], k_nearest=8, n_items=30)
            original_id_res = [str(self.algo.trainset.to_raw_iid(id)) for id in recommend_res]
            # 储存数据
            update_sql = "update NTWebsite_user Recommend=? where id=?"
            con.execute(update_sql, (','.join(original_id_res), user['id']))