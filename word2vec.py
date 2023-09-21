from gensim.models import Word2Vec
import pandas as pd


s = open('./data/去除停用词并分词（合并）.csv', 'r', encoding='gb18030')  # 分词
words = []
for i in s.readlines():
    words.append(i.split(','))

n_dim = 300
w2v_model = Word2Vec(vector_size=n_dim, sg=1, min_count=10)
w2v_model.build_vocab(words)  # 生成词表
w2v_model.train(words, total_examples=w2v_model.corpus_count, epochs=10)  # 在训练集数据上进行建模

def m_avgvec(words, w2vmodel):  # 各个词向量直接平均的方式生成整句所对应的词向量
    return pd.DataFrame([w2vmodel.wv[w] for w in words if w in w2vmodel.wv]).agg('mean')

train_vec = pd.DataFrame([m_avgvec(a, w2v_model) for a in words])  # 此处a没有实际意义，单纯为了循环
print(train_vec.head())
# # 显示词向量矩阵前五条，这里为最终得到的建模需用数据集的词向量矩阵

embedding_path = './data/word2vec.csv'
w2v_model.wv.save_word2vec_format(embedding_path)



