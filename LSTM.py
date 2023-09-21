from tensorflow.keras.preprocessing import sequence
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense,  Dropout, Activation, Embedding, LSTM, Conv1D, MaxPooling1D
import re
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
# import keras
# from tensorflow.python.keras.datasets import imdb

# embedding 参数
maxlen = 100    # 最大样本长度，不足进行Padding，超过进行截取
embedding_size = 200   # 词向量维度

# 卷积参数
kernel_size = 5
filters = 128
pool_size = 4

# LSTM参数
lstm_output_size = 100     # LSTM层的输出维度

# 训练参数
batch_size = 128
epochs = 20


def textToChars(filePath):
  """
  读取文本文件并进行处理,只保留中文字符，去掉所有非中文字符
  :param filePath:文件路径
  :return:
  """
  lines = []
  df = pd.read_excel(filePath, header=None)
  df.columns = ['content']
  for index, row in df.iterrows():
    row = row['content']
    row = re.sub("[^\u4e00-\u9fa5]", "", str(row))  # 只保留中文
    lines.append(list(str(row)))
  return lines


def getWordIndex(vocabPath):
  """
  获取word2Index,index2Word
  :param vocabPath:词汇文件，使用的是BERT里的vocab.txt文件
  :return:
  """
  word2Index = {}
  with open(vocabPath, encoding="utf-8") as f:
    for line in f.readlines():
      word2Index[line.strip()] = len(word2Index)
  index2Word = dict(zip(word2Index.values(), word2Index.keys()))
  return word2Index, index2Word


def lodaData(posFile, negFile, word2Index):
  """
  获取训练数据
  :param posFile:正样本文件
  :param negFile:负样本文件
  :param word2Index:
  :return:
  """
  posLines = textToChars(posFile)
  negLines = textToChars(negFile)
  textLines = posLines+negLines
  print("正样本数量%d,负样本数量%d"%(len(posLines), len(negLines)))
  posIndexLines = [[word2Index[word] if word2Index.get(word) else 0 for word in line] for line in posLines]
  negIndexLines = [[word2Index[word] if word2Index.get(word) else 0 for word in line] for line in negLines]
  lines = posIndexLines + negIndexLines
  print("训练样本和测试样本共：%d 个"%(len(lines)))
  # lens = [len(line) for line in lines]
  labels = [1] * len(posIndexLines) + [0] * len(negIndexLines)
  padSequences = sequence.pad_sequences(lines, maxlen=maxlen, padding="post", truncating="post")
  X_train, X_test, y_train, y_test = train_test_split(padSequences, np.array(labels), test_size=0.2, random_state=42)  # 按照8:2的比例划分训练集和测试集
  return (textLines, labels), (X_train, X_test, y_train, y_test)

vocabPath = "./data/vocab.txt"
negFilePath = "./data/消极评论.xlsx"
posFilePath = "./data/积极评论.xlsx"
word2Index, index2Word = getWordIndex(vocabPath)
(textLines, labels), (X_train, X_test, y_train, y_test) = lodaData(posFile=posFilePath, negFile=negFilePath, word2Index=word2Index)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)


model = Sequential()
model.add(Embedding(len(word2Index), embedding_size, input_length=maxlen))
model.add(Dropout(0.2))
model.add(Conv1D(filters, kernel_size, padding="valid", activation="relu", strides=1))
model.add(MaxPooling1D(pool_size))
model.add(LSTM(lstm_output_size))
model.add(Dense(1))
model.add(Activation("sigmoid"))
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
print("开始训练")
model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, validation_data=(X_test, y_test))
model.summary()

model.save('./data/Emotional_classification_model.h5')    # 保存模型
# new_model = keras.models.load_model('./data/Emotional_classification_model.h5')   # 加载模型



# def predict_one(sentence,model,word2Index):
#   sentence = re.sub("[^\u4e00-\u9fa5]", "", str(sentence))  # 只保留中文
#   # print(sentence)
#   sentence = [word2Index[word] if word2Index.get(word) else 0 for word in sentence]
#   sentence = sentence+[0]*(maxlen-len(sentence)) if len(sentence) < maxlen else sentence[0:300]
#   # print(sentence)
#   sentence = np.reshape(np.array(sentence), (-1, len(sentence)))
#   pred_prob = model.predict(sentence)
#   label = 1 if pred_prob[0][0] > 0.5 else 0
#   if label == 1:
#     print('这条评论是正面评论。')
#   else:
#     print('这条评论是负面评论。')
#   return label
#
#
# sentence = "腾讯真垃圾，赶紧倒闭吧！"
# predict_one(sentence, model, word2Index)





