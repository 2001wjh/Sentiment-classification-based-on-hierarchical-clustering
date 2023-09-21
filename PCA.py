# PCA降维（方法一）
# import numpy as np
# import pandas as pd
#
# filename = r'./data/word2vec.csv'     # 要分析的文件名
# data_mat = pd.DataFrame(pd.read_csv(filename))  # 打开文件
#
# # PCA Algorithm begin
# # 标准化
# mean_values = np.mean(data_mat, axis=0)
# std_mat = (data_mat - mean_values) / np.std(data_mat, axis=0, ddof=1)
#
# # 计算特征值 特征向量
# cov_mat = np.cov(std_mat)
# eig_values, eig_vectors = np.linalg.eig(np.mat(cov_mat))
#
# indices = np.argsort(eig_values)[::-1]     # 将特征值从小到大排序，返回的是特征值对应的数组里的下标
# eig_values = eig_values[indices]
# eig_vectors = eig_vectors[:, indices]
# print(eig_values)
#
# # m = np.dot(std_mat, eig_vectors)
# explained_variance_ratio = eig_values / sum(eig_values)    # 计算贡献率
# explained_variance_ratio_cumulative = np.cumsum(explained_variance_ratio)    # 计算累计贡献率
# # # PCA Algorithm end
# print('贡献率：', explained_variance_ratio)
# print('累计贡献率：', explained_variance_ratio_cumulative)


# PCA降维（方法二）
import numpy as np
from sklearn.decomposition import PCA
import pandas as pd

path = './data/word2vec.csv'
df = pd.read_csv(path, header=None, encoding='utf-8')
data = np.array(df)
pca = PCA(n_components=3)
pca_data = pca.fit_transform(data)
print(data)
print(pca_data)
print(pca.explained_variance_ratio_)

# 将降维后的数据保存为csv文件（ndarray-->DataFrame结构）
df_new = pd.DataFrame(pca_data)
# df数据小数位数过多，为16位，将df数据全部转换为3位小数
df_new = df_new.round(decimals=3)
df_new.to_csv("./data/word2vec_pca.csv")

