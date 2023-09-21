# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
# import seaborn as sns
from sklearn import metrics
import os
import numpy as np

# 设置环境变量OMP_NUM_THREADS=5
os.environ['OMP_NUM_THREADS'] = "5"

path = './data/word2vec_pca.csv'
df = pd.read_csv(path, header=None)
# print(df)

'''判断最佳聚类数'''
# 方法一：拐点法
def SSE(X, clusters):
    sse = []
    for i in range(1, clusters+1):
        kmeans = KMeans(n_clusters=i, init='k-means++')
        kmeans.fit(X)
        sse.append(kmeans.inertia_)
        '''中文显示'''
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(range(1, clusters+1), sse, 'b*-')
    plt.tick_params(labelsize=14)
    plt.xlabel('Number of clusters', fontsize=16)
    plt.ylabel('SSE', fontsize=16)
    plt.savefig("./result pictures/KMeans_Inflected point method.jpg")
    plt.show()
SSE(df, 12)


# 方法二：轮廓系数法
def k_silhouette(X, clusters):
    key = range(2, clusters+1)
    s = []     # 储存不同簇下的轮廓系数
    for i in key:
        kmeans = KMeans(n_clusters=i)
        kmeans.fit(X)
        labels = kmeans.labels_
        s.append(metrics.silhouette_score(X, labels, metric='euclidean'))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(key, s, 'b*-')
    plt.xlabel('簇的个数')
    plt.ylabel('轮廓系数')
    plt.savefig("./result pictures/KMeans_Contour coefficient method.jpg")
    plt.show()
k_silhouette(df, 15)

'''k-means聚类'''
OMP_NUM_THREADS = 5
kmeans = KMeans(n_clusters=2, max_iter=1000, init='k-means++')
kmeans.fit(df)

label_pred = kmeans.labels_  # 获取聚类标签

x0 = df[label_pred == 0]  # 获取类别是“0”的数据对象
x1 = df[label_pred == 1]  # 获取类别是“1”的数据对象
# “label_pred”的全称应为“label_prediction”

x_data = np.array(x0, type(float))
y_data = np.array(x1, type(float))

# 绘制 k-means 聚类结果
# 补充: plt.scatter()是绘制散点图的函数
# c指的是颜色
# marker指的是散点的形状
# label指的是标签的名称
# alpha指的是散点的透明度，取值为[0, 1]，0表示完全透明，1表示完全不透明
plt.scatter(x_data[:, 0], x_data[:, 1], c="red", marker='H', label='label0', alpha=0.3)
plt.scatter(y_data[:, 0], y_data[:, 1], c="green", marker='*', label='label1', alpha=0.3)


# 给散点图加上标题
plt.title('Clustering results',  # 标题的名称
          fontsize=18,  # 标题的字体大小
          color='white',  # 标题的字体颜色
          backgroundcolor='#334f65',  # 标题的背景
          pad=20)  # 标题的边距

plt.xlabel('sepal length')  # 横坐轴
plt.ylabel('sepal width')  # 纵坐轴

plt.legend(loc=2)  # 显示图例；“loc”为“location”的意思，设置这个
# 英文单词legend: (图片或地图的)文字说明，图例
plt.savefig("./result pictures/KMeans_Cluster point graph.jpg")
plt.show()


# df['cluster'] = kmeans.labels_
# print(df)
# centers = kmeans.cluster_centers_
# print(centers)
#
# df_0 = df['cluster'] == '0'  # 获取类别是“0”的数据对象
# df_1 = df['cluster'] == '1'  # 获取类别是“1”的数据对象
#
# '''结果分析'''
# print(df.groupby(['cluster']).describe())
# # name = ['cluster 1', 'cluster 2']

# '''作图'''
# # kmeans图
# plt.figure(dpi=300, figsize=(10, 8), facecolor='y', edgecolor='g')
# # sns.lmplot(x=df[0], y='情绪化得分', data=df, hue='cluster',
# #            markers=['^', 'o', 's', 'o'],
# #            scatter_kws={'alpha': 0.5})
# plt.scatter(centers[:, 0], centers[:, 1], color='grey', s=25)
# plt.tick_params(labelsize=15)
# # plt.legend(name, loc='upper right', bbox_to_anchor=(1.1, 0.24), font size=14 )
# plt.xlabel('Quantified word count', fontsize=17)
# plt.ylabel('Emotional Factor', fontsize=17)
# # sns.set(font_scale = 15)
# # plt.savefig("1.jpg")
# plt.show()





